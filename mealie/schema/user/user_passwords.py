from pydantic import UUID4
from sqlalchemy.orm import joinedload
from sqlalchemy.orm.interfaces import LoaderOption

from mealie.schema._mealie import MealieModel

from ...db.models.users import PasswordResetModel, User
from .user import PrivateUser


class ForgotPassword(MealieModel):
    email: str


class PasswordResetToken(MealieModel):
    token: str


class ValidateResetToken(MealieModel):
    token: str


class ResetPassword(ValidateResetToken):
    email: str
    password: str
    passwordConfirm: str


class SavePasswordResetToken(MealieModel):
    user_id: UUID4
    token: str


class PrivatePasswordResetToken(SavePasswordResetToken):
    user: PrivateUser

    class Config:
        orm_mode = True

    @classmethod
    def loader_options(cls) -> list[LoaderOption]:
        return [
            joinedload(PasswordResetModel.user).joinedload(User.group),
            joinedload(PasswordResetModel.user).joinedload(User.favorite_recipes),
            joinedload(PasswordResetModel.user).joinedload(User.tokens),
        ]
