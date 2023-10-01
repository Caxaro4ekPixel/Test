from datetime import datetime, timedelta
from typing import Optional, Dict
from beanie import Document
from loguru import logger as log
from .episode import Episode
from anilibria import Title

class Release(Document):
    id: int
    chat_id: int
    status: Optional[str] = ""
    code: str
    en_title: str
    ru_title: str
    is_ongoing: bool = True
    is_top: bool = False
    is_commer: bool = False
    days_to_work: Optional[int] = 4
    episodes: Optional[Dict[str, Episode]] = None

    class Settings:
        name = "releases"

    @classmethod
    async def get_by_id(cls, id: int) -> Optional["Release"]:
        return await cls.find_one(cls.id == id)
    
    @classmethod
    async def get_by_chat_id(cls, chat_id: int) -> Optional["Release"]:
        return await cls.find_one(cls.chat_id == chat_id)
    
    @classmethod
    async def get_by_code(cls, code: str) -> Optional["Release"]:
        return await cls.find_one(cls.code == code)
    
    @classmethod
    async def check_time(cls, title: Title) -> timedelta:
        release = await cls.find_one(cls.id == title.id)
        try:
            ep = list(release.episodes)[-1]
            ep = release.episodes.get(ep)
        except Exception as ex:
            log.error(ex)
            log.error("Не нашли эпизода в БД")
            return False

        td = datetime.fromtimestamp(title.updated) - ep.date
        return td