"""
event listener for database operations
e.g:
    -object creation
    -objet update
"""

from sqlalchemy import event
from social_api.models.user.model import UserTable


@event.listens_for(UserTable, 'after_insert')
def create_shop_after_user_creation(mapper, connection, target):
    print(mapper)
    print(connection)
    print(target)
