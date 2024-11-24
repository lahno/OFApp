from datetime import datetime
import logging
from typing import Optional, Union

from pydantic import ValidationError
from sqlalchemy import select, update, delete

from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session

from db.database import session_factory
from db.models import MessageORM, AccountORM, UserORM
from db.schemas import MessageDTO, AccountDTO, UserDTO

logger = logging.getLogger(__name__)


class SyncORM:

    @staticmethod
    def new_message(message: str) -> Optional[Union[int, str]]:
        if message:
            with session_factory() as session:
                message_data = {
                    "message": message,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }
                stmt = (
                    insert(MessageORM)
                    .values(message_data)
                    .on_conflict_do_nothing(index_elements=["message"])
                    .returning(MessageORM.id)
                )

                return SyncORM._get_result_id(session, stmt)

    @staticmethod
    def get_message(message_id: int) -> Optional[MessageDTO]:
        try:
            with session_factory() as session:
                query = select(MessageORM).filter_by(id=message_id)
                result = session.execute(query)
                if result_orm := result.scalars().one_or_none():
                    return MessageDTO.model_validate(result_orm)
        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")

        return None

    @staticmethod
    def get_messages(status=True) -> Optional[list[MessageDTO]]:
        try:
            with session_factory() as session:
                result = session.execute(select(MessageORM).filter_by(status=status))
                result_orm = result.scalars().all()

                return (
                    [MessageDTO.model_validate(user) for user in result_orm]
                    if result_orm
                    else None
                )

        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")

        return None

    @staticmethod
    def get_all_messages() -> Optional[list[MessageDTO]]:
        try:
            with session_factory() as session:
                result = session.execute(select(MessageORM))
                result_orm = result.scalars().all()

                return (
                    [MessageDTO.model_validate(user) for user in result_orm]
                    if result_orm
                    else None
                )

        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")

        return None

    @staticmethod
    def update_message(updated_data: dict, message_id: int) -> None:
        with session_factory() as session:
            stmt = (
                update(MessageORM)
                .where(MessageORM.id == message_id)
                .values(**updated_data)
                .returning(MessageORM)
            )
            session.execute(stmt)
            session.commit()

    @staticmethod
    def delete_message(message_id: int) -> None:
        try:
            with session_factory() as session:
                stmt = delete(MessageORM).where(MessageORM.id == message_id)
                session.execute(stmt)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении сообщения: {e}")

    @staticmethod
    def new_account(email: str) -> Optional[Union[int, str]]:
        if email:
            with session_factory() as session:
                message_data = {
                    "email": email,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }

                stmt = (
                    insert(AccountORM)
                    .values(message_data)
                    .on_conflict_do_nothing(index_elements=["email"])
                    .returning(AccountORM.id)
                )

                return SyncORM._get_result_id(session, stmt)

    @staticmethod
    def get_account(account_id: int) -> Optional[AccountDTO]:
        try:
            with session_factory() as session:
                query = select(AccountORM).filter_by(id=account_id)
                result = session.execute(query)
                if result_orm := result.scalars().one_or_none():
                    return AccountDTO.model_validate(result_orm)
        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")

        return None

    @staticmethod
    def get_accounts() -> Optional[list[AccountDTO]]:
        try:
            with session_factory() as session:
                result = session.execute(select(AccountORM))
                result_orm = result.scalars().all()

                return (
                    [AccountDTO.model_validate(user) for user in result_orm]
                    if result_orm
                    else None
                )

        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")

        return None

    @staticmethod
    def update_account(updated_data: dict, account_id: int) -> None:
        with session_factory() as session:
            stmt = (
                update(AccountORM)
                .where(AccountORM.id == account_id)
                .values(**updated_data)
                .returning(AccountORM)
            )
            session.execute(stmt)
            session.commit()

    @staticmethod
    def delete_account(account_id: int) -> None:
        try:
            with session_factory() as session:
                stmt = delete(AccountORM).where(AccountORM.id == account_id)
                session.execute(stmt)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении accounts: {e}")

    @staticmethod
    def new_user(username: str) -> Optional[Union[int, str]]:
        if username:
            with session_factory() as session:
                message_data = {
                    "username": username,
                    "created_at": datetime.utcnow(),
                    "updated_at": datetime.utcnow(),
                }

                stmt = (
                    insert(UserORM)
                    .values(message_data)
                    .on_conflict_do_nothing(index_elements=["username"])
                    .returning(UserORM.id)
                )

                return SyncORM._get_result_id(session, stmt)

    @staticmethod
    def get_user(user_id: int) -> Optional[UserDTO]:
        try:
            with session_factory() as session:
                query = select(UserORM).filter_by(id=user_id)
                result = session.execute(query)
                if result_orm := result.scalars().one_or_none():
                    return UserDTO.model_validate(result_orm)
        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")

        return None

    @staticmethod
    def get_users() -> Optional[list[UserDTO]]:
        try:
            with session_factory() as session:
                result = session.execute(select(UserORM))
                result_orm = result.scalars().all()

                return (
                    [UserDTO.model_validate(user) for user in result_orm]
                    if result_orm
                    else None
                )

        except ValidationError as e:
            logger.error(f"Ошибка валидации: {e}")
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при выполнении запроса: {e}")

        return None

    @staticmethod
    def update_user(updated_data: dict, user_id: int) -> None:
        with session_factory() as session:
            stmt = (
                update(UserORM)
                .where(UserORM.id == user_id)
                .values(**updated_data)
                .returning(UserORM)
            )
            session.execute(stmt)
            session.commit()

    @staticmethod
    def delete_user(user_id: int) -> None:
        try:
            with session_factory() as session:
                stmt = delete(UserORM).where(UserORM.id == user_id)
                session.execute(stmt)
                session.commit()
        except SQLAlchemyError as e:
            logger.error(f"Ошибка при удалении accounts: {e}")

    @staticmethod
    def _get_result_id(session: Session, stmt) -> Optional[Union[int, str]]:
        try:
            result = session.execute(stmt)
            new_id = result.scalar_one_or_none()
            session.commit()
            if new_id is None:
                return "Error: Model already exists"
            return new_id
        except IntegrityError as e:
            session.rollback()
            logger.error(f"Ошибка целостности данных: {e}")
            return "Error: Model already exists"
        except SQLAlchemyError as e:
            session.rollback()
            message = f"Ошибка при выполнении запроса: {e}"
            logger.error(message)
            return message
