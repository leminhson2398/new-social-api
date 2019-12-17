from social_api.db.base import database
from .model import UserTable
from sqlalchemy import select, or_
from sqlalchemy.sql.selectable import Select
import typing
from validate_email import validate_email
import re


MALE: str = 'male'
FEMALE: str = 'female'
OTHER: str = 'other'
USE_EMAIL: str = 'email'
USE_PHONE_NUMBER: str = 'phone_number'


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
