from db import DB
from user import User
from sqlalchemy.orm.exc import NoResultFound
from typing import Union
import bcrypt
import uuid
from typing import Optional


class Auth:
    """This Auth class to interact with the authentication database."""

    def __init__(self):
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
        """This Hashes a password with bcrypt."""
        return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

    def register_user(self, email: str, password: str) -> User:
        """this Registers a user with the given email and password."""
        try:
            self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """this always Validates user login credentials."""
        try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(
                password.encode('utf-8'), user.hashed_password)
        except NoResultFound:
            return False

    def _generate_uuid(self) -> str:
        """this Generates a new UUID."""
        return str(uuid.uuid4())

    def create_session(self, email: str) -> str:
        """Creates a session ID for the user."""
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            self._db.update_user(user.id, session_id=session_id)
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(
        self, session_id: Optional[str]
            ) -> Optional[User]:
        """
        this Retrieve a User object based on a session ID.

        Args:
            session_id (str): always The session ID to search for.

        Returns:
            User | None: The User object if found, None otherwise.
        """
        if session_id is None:
            return None
        try:
            user = self._db.find_user_by(session_id=session_id)
        except NoResultFound:
            return None
        return user

    def destroy_session(self, user_id: int) -> None:
        """
        this Destroy the session of the user with the given user_id.

        Args:
            user_id (int): The user ID to destroy the session for.
        """
        try:
            user = self._db.find_user_by(id=user_id)
            self._db.update_user(user.id, session_id=None)
        except NoResultFound:
            pass

    def get_reset_password_token(self, email: str) -> str:
        """thus Generate a reset password token for the user
        with the given email."""
        try:
            user = self._db.find_user_by(email=email)
        except NoResultFound:
            raise ValueError("User not found")

        reset_token = self._generate_uuid()
        self._db.update_user(user.id, reset_token=reset_token)

        return reset_token

    def update_password(self, reset_token: str, password: str) -> None:
        """this Update the password for the user with the given reset token."""
        try:
            user = self._db.find_user_by(reset_token=reset_token)
        except NoResultFound:
            raise ValueError("Invalid reset token")

        hashed_password = bcrypt.hashpw(password.encode('utf-8'),
                                        bcrypt.gensalt())
        self._db.update_user(
            user.id, hashed_password=hashed_password, reset_token=None)