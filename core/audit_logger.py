from dataclasses import dataclass, asdict
from datetime import datetime, timezone
from typing import Self

from bson import ObjectId, CodecOptions
from motor.motor_asyncio import AsyncIOMotorCollection

from core.utils import get_permissions_level


@dataclass(frozen=True)
class AuditEventSource:
    user_id: int
    username: str
    ip: str
    country: str
    user_agent: str
    role: int
    source: str


async def audit_event_source_from_user(bot: object, user: dict) -> AuditEventSource:
    return AuditEventSource(user_id=user.id,
                            username=user.name,
                            ip="",
                            country="",
                            user_agent="Discord",
                            role=await get_permissions_level(bot, user),
                            source="modmail")


@dataclass(frozen=True)
class AuditEvent:
    action: str
    description: str
    actor: AuditEventSource
    timestamp: datetime = datetime.now(tz=timezone.utc)
    id: ObjectId = None

    def to_short_dict(self) -> dict:
        result = asdict(self)
        result.pop("id")
        return result


def _construct_audit_event_from_dict(dict: dict) -> AuditEvent:
    return AuditEvent(action=dict["action"],
                      description=dict["description"],
                      actor=_construct_audit_event_source_from_dict(dict["actor"]),
                      timestamp=dict["timestamp"],
                      id=dict["_id"])


def _construct_audit_event_source_from_dict(dict: dict) -> AuditEventSource:
    return AuditEventSource(user_id=dict["user_id"],
                            username=dict["username"],
                            ip=dict["ip"],
                            country=dict["country"],
                            user_agent=dict["user_agent"],
                            role=dict["role"],
                            source=dict["source"])


class AuditLogger:
    audit_log_collection: AsyncIOMotorCollection

    def __init__(self: Self, bot):
        # don't create our own connection, use the one from the bot
        # We need to use the tz_aware option to ensure that datetimes are retrieved as timezone aware
        self.audit_log_collection = bot.api.db.audit_log.with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=timezone.utc))

    def push(self, event: AuditEvent):
        # push the audit log to the database
        self.audit_log_collection.insert_one(event.to_short_dict())

    async def get_audit_log(self: Self, event_id: str) -> AuditEvent:
        event = await self.audit_log_collection.find_one({"_id": ObjectId(event_id)})
        return _construct_audit_event_from_dict(event)
