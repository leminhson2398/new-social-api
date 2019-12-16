from ..base import database
from .model import UserTable
from sqlalchemy import select, or_
from sqlalchemy.sql.schema import Table
from sqlalchemy.sql.selectable import Select
import typing
from validate_email import validate_email
import re

MALE: str = 'male'
FEMALE: str = 'female'
OTHER: str = 'other'
USE_EMAIL: str = 'email'
USE_PHONE_NUMBER: str = 'phone_number'


async def fetch_user_with_field(email: str = None, phone: str = None, username: str = None) -> typing.Union[None, typing.Mapping]:
    """
    email: string type\n
    phone: string type\n
    username: string type\n
    NOTE: only pass in one (1) argument per call to me\n
    either email || phone || username
    """
    query: typing.Union[Select, None] = None
    if bool(email) and isinstance(email, str):
        query = select([UserTable]).where(
            UserTable.c['email'] == email
        )
    elif bool(phone) and isinstance(phone, str):
        query = select([UserTable]).where(
            UserTable.c.phone_number == phone
        )
    elif bool(username) and isinstance(username, str):
        query = select([UserTable]).where(
            UserTable.c.username == username
        )
    else:
        return None
    return await database.fetch_one(query)


def validate_password(password: str) -> typing.List[str]:
    """
        password must be at least 8 characters long, one uppercase, one lowercase,
        one digit, one special character.
        validate your password, whether it satisfies the system standard password or not
        if the returned is an empty list, the password satisfies, otherwise, not.
    """
    if isinstance(password, str) and password != "":
        password = password.strip()
        # password fullcase:
        PASSWORD_FULLCASE = r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]{8,}$"
        # one uppercase:
        ONE_UPPERCASE = r"[A-Z]+"
        # one lowercase:
        ONE_LOWERCASE = r"[a-z]+"
        # one digit:
        ONE_DIGIT = r"[0-9]+"
        # one special character:
        ONE_SPECIAL_CHARACTER = r"[!$%&'()*+,-.:;<=>?@[\]^_`{|}~]"
        # eight characters:
        EIGHT_CHARACTERS = r"(.){8,}"

        matchDict = {
            "Password must has at least 1 lowercase character": ONE_LOWERCASE,
            "Password must has at least 1 uppercase character": ONE_UPPERCASE,
            "Password must has at least 1 digit": ONE_DIGIT,
            "Password must has at least 1 special character": ONE_SPECIAL_CHARACTER,
            "Password must has at least 8 characters": EIGHT_CHARACTERS
        }

        if not re.compile(PASSWORD_FULLCASE).match(password) is None:
            return []
        # otherwise:
        return [
            message for message in matchDict.keys() if re.compile(
                matchDict[message]
            ).search(password) is None
        ]
    else:
        return ["Please enter a valid password."]


async def insert_new_user(userData: dict) -> None:
    """
    async function to add new user into the database\n
    :userData must be a dictionary of all validaed and valid data that is necessary for creating new user
    """
    query: typing.Any = UserTable.insert().values(**userData)
    await database.execute(query=query)


def send_signup_activation_code(type: str, value: str) -> None:
    """
    send activation code based on registration type\n
    email: send email\n
    phone number: send message
    """
    import time
    time.sleep(5)

    print('Sending code')
