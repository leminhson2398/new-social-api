from social_api.utils.function import slugify
import typing


def set_slug_from_given_field(context: typing.Any, name: str) -> str:
    """
    returns sluggified version of a string value
    refer to sqlalchemy doc on setting default parameter in Column
    """
    return slugify(
        context.get_current_parameters()[name]
    )
