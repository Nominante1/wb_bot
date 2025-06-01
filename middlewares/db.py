from aiogram import BaseMiddleware
from sqlalchemy.orm import Session
from typing import Callable, Awaitable, Dict, Any
from database import get_db

class DatabaseSessionMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[Any, Dict[str, Any]], Awaitable[Any]],
        event: Any,
        data: Dict[str, Any]
    ) -> Any:
        db_gen = get_db()
        db: Session = next(db_gen)
        try:
            data["db"] = db  # Передаем сессию в хендлеры
            result = await handler(event, data)
        finally:
            db.close()
        return result