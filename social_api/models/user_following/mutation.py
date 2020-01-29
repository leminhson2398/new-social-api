from graphene import (
    Mutation as ObjectMutation,
    ObjectType,
    Int,
    Boolean,
    List,
    String,
    NonNull
)
from graphql.execution import ResolveInfo
from starlette.authentication import BaseUser
import typing
from sqlalchemy.sql.selectable import Select
from .model import UserFollowingTable
from sqlalchemy import select, and_, delete, update
from social_api.db.common import fetch_one_record_with_query
from social_api.db.base import database
from starlette.background import BackgroundTasks
from ..user.model import UserTable
from databases.core import Transaction
from sqlalchemy.exc import IntegrityError
import logging


async def update_user_following(toUserId: int = None, fromUserId: int = None, existingRecord: typing.Any = None) -> None:
    """
    existingRecord decides whether to remove or add following relationship.
    also, takes care of 'number_of_followers' of an user.
    """
    if toUserId is None or fromUserId is None:
        raise ValueError(
            "Both 'toUserId' and 'fromUserId' have to be integers.")

    toggleFollowQuery: typing.Any = None
    # query for updating user table:
    updateUserQuery: typing.Any = update(UserTable).where(
        UserTable.c.id == toUserId
    ).values(
        number_of_followers=(
            # python comprehension
            UserTable.c.number_of_followers +
            1 if existingRecord is None else UserTable.c.number_of_followers - 1
        )
    )

    if existingRecord is not None:
        # record does exist, have to remove this record
        toggleFollowQuery = delete(UserFollowingTable).where(
            UserFollowingTable.c.id == existingRecord['id']
        )
    else:
        # have to add one record
        toggleFollowQuery = UserFollowingTable.insert().values(
            from_user_id=fromUserId, to_user_id=toUserId
        )

    # create db transaction
    transaction: Transaction = await database.transaction()
    try:
        toggleFollowResult: typing.Any = await database.execute(query=toggleFollowQuery)
        updateUserResult: typing.Any = await database.execute(query=updateUserQuery)

    except IntegrityError as e:
        logging.error(f"Error update user following relation: {e}.")
        await transaction.rollback()
    else:
        await transaction.commit()


class ToggleFollowUser(ObjectMutation):
    ok = Boolean(required=True)
    errors = NonNull(
        List(String, required=False)
    )

    class Arguments:
        toUserId = Int(required=True)

    async def mutate(self, info: ResolveInfo, **kwargs):
        ok: bool = False
        errors: typing.List[str] = []

        existingFollowingRecord: typing.Union[None, typing.Mapping]

        user: BaseUser = info.context['request'].user

        # check user authenticated or not:
        if user.is_authenticated:
            # get toUserId:
            toUserId: typing.Union[int, None] = kwargs.get('toUserId', None)
            if toUserId and isinstance(toUserId, int):
                # checking if this following relation ship does exist or not:
                if toUserId != user.id:
                    query: Select = select([
                        UserFollowingTable
                    ]).where(
                        and_(
                            UserFollowingTable.c.from_user_id == user.id,
                            UserFollowingTable.c.to_user_id == toUserId
                        )
                    )
                    existingFollowingRecord = await fetch_one_record_with_query(query=query)
                    ok = True
                else:
                    errors.append('You cannot follow yourself.')
            else:
                errors.append('Invalid id of user.')
        else:
            errors.append('You have to log in to follow people.')

        if ok and len(errors) == 0:
            # add background task
            background: BackgroundTasks = info.context['background']
            background.add_task(
                update_user_following,
                toUserId,
                user.id,
                existingFollowingRecord
            )

        return ToggleFollowUser(
            ok=ok,
            errors=errors
        )


class Mutation(ObjectType):
    toggle_follow_user = ToggleFollowUser.Field()
