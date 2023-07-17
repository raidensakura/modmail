import datetime
import enum
from dataclasses import dataclass
from typing import Optional, Self, Tuple

import discord
import isodate
from bson import CodecOptions, ObjectId
from motor.core import AgnosticCollection


class BlockType(enum.IntEnum):
    USER = 0
    ROLE = 1


class BlockReason(enum.StrEnum):
    GUILD_AGE = "guild_age"
    ACCOUNT_AGE = "account_age"
    BLOCKED_ROLE = "blocked_role"
    BLOCKED_USER = "blocked_user"


@dataclass(frozen=True)
class BlockedUser:
    # _id: ObjectId
    # May be role or user id
    id: int
    expires_at: Optional[datetime.datetime]
    reason: str
    timestamp: datetime.datetime
    blocking_user_id: int
    # specifies if the id is a role or user id
    type: BlockType


class Blocklist:
    blocklist_collection: AgnosticCollection

    def __init__(self: Self, bot) -> None:
        self.blocklist_collection = bot.api.db.blocklist.with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=datetime.timezone.utc))
        self.bot = bot

    async def setup(self):
        index_info = await self.blocklist_collection.index_information()
        print(index_info)
        await self.blocklist_collection.create_index("id")
        await self.blocklist_collection.create_index("expires_at", expireAfterSeconds=0)

    async def block_user(self, user_id: int, expires_at: Optional[datetime.datetime], reason: str,
                         blocked_by: int) -> None:
        now = datetime.datetime.utcnow()

        await self.blocklist_collection.insert_one(BlockedUser(
            id=user_id,
            expires_at=expires_at,
            reason=reason,
            timestamp=now,
            blocking_user_id=blocked_by,
            type=BlockType.USER
        ))

    # we will probably want to cache these
    async def is_user_blocked(self, member: discord.Member) -> Tuple[bool, Optional[BlockReason]]:
        """
        Side effect free version of is_blocked

        Parameters
        ----------
        member

        Returns
        -------
        True if the user is blocked
        """
        #

        if str(member.id) in self.bot.blocked_whitelisted_users:
            return False

        blocked = await self.blocklist_collection.find_one({"id": member.id})
        if blocked is not None:
            print(blocked)
            return True, BlockReason.BLOCKED_USER

        roles = member.roles

        blocked = await self.blocklist_collection.find_one(filter={"id": {"$in": [r.id for r in roles]}})
        if blocked is not None:
            return True, BlockReason.BLOCKED_ROLE

        if not self.is_valid_account_age(member):
            print("account_age")
            return True, BlockReason.ACCOUNT_AGE
        if not self.is_valid_guild_age(member):
            print("guild_age")
            return True, BlockReason.GUILD_AGE

        return False, None

    def is_valid_account_age(self, author: discord.User) -> bool:
        account_age = self.bot.config.get("account_age")

        if account_age is None or account_age == isodate.Duration():
            return True

        now = discord.utils.utcnow()

        min_account_age = author.created_at + account_age

        if min_account_age < now:
            # User account has not reached the required time
            return False
        return True

    def is_valid_guild_age(self, author: discord.Member) -> bool:
        guild_age = self.bot.config.get("guild_age")

        if guild_age is None or guild_age == isodate.Duration():
            return True

        now = discord.utils.utcnow()

        if not hasattr(author, "joined_at"):
            self.bot.logger.warning("Not in guild, cannot verify guild_age, %s.", author.name)
            return False

        min_guild_age = author.joined_at + guild_age

        if min_guild_age > now:
            # User has not stayed in the guild for long enough
            return False
        return True
