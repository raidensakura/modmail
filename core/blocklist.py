import datetime
import enum
from dataclasses import dataclass
from typing import Optional, Tuple

import discord
import isodate
from bson import CodecOptions
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
class BlocklistEntry:
    # _id: ObjectId
    # May be role or user id
    id: int
    expires_at: Optional[datetime.datetime]
    reason: Optional[str]
    timestamp: datetime.datetime
    blocking_user_id: int
    # specifies if the id is a role or user id
    type: BlockType

    @staticmethod
    def from_dict(data: dict):
        return BlocklistEntry(
            id=data["id"],
            expires_at=data["expires_at"],
            reason=data["reason"],
            timestamp=data["timestamp"],
            blocking_user_id=data["blocking_user_id"],
            type=data["type"],
        )


class Blocklist:
    blocklist_collection: AgnosticCollection

    def __init__(self, bot) -> None:
        self.blocklist_collection = bot.api.db.blocklist.with_options(
            codec_options=CodecOptions(tz_aware=True, tzinfo=datetime.timezone.utc)
        )
        self.bot = bot

    async def setup(self):
        await self.blocklist_collection.create_index("id")
        await self.blocklist_collection.create_index("expires_at", expireAfterSeconds=0)

    async def add_block(self, block: BlocklistEntry) -> None:
        await self.blocklist_collection.insert_one(block.__dict__)

    async def block_id(
        self,
        user_id: int,
        expires_at: Optional[datetime.datetime],
        reason: str,
        blocked_by: int,
        block_type: BlockType,
    ) -> None:
        now = datetime.datetime.utcnow()

        await self.add_block(
            block=BlocklistEntry(
                id=user_id,
                expires_at=expires_at,
                reason=reason,
                timestamp=now,
                blocking_user_id=blocked_by,
                type=block_type,
            )
        )

    async def unblock_id(self, user_or_role_id: int) -> bool:
        result = await self.blocklist_collection.delete_one({"id": user_or_role_id})
        if result.deleted_count == 0:
            return False
        return True

    async def is_id_blocked(self, user_or_role_id: int) -> Tuple[bool, Optional[BlocklistEntry]]:
        """
        Checks if the given ID is blocked

        This method only checks to see if there is an active manual block for the given ID.
        It does not do any checks for whitelisted users or roles, account age, or guild age.

        Parameters
        ----------
        user_or_role_id

        Returns
        -------

        True if there is an active block for the given ID

        """
        result = await self.blocklist_collection.find_one({"id": user_or_role_id})
        if result is None:
            return False, None
        return True, BlocklistEntry.from_dict(result)

    async def get_all_blocks(self) -> list[BlocklistEntry]:
        """
        Returns a list of all active blocks

        THIS RETRIEVES ALL ITEMS FROM THE DATABASE COLLECTION, USE WITH CAUTION

        Returns
        -------

        A list of BlockListItems

        """
        dict_list = await self.blocklist_collection.find().to_list(length=None)
        dataclass_list: list[BlocklistEntry] = []
        for i in dict_list:
            dataclass_list.append(BlocklistEntry.from_dict(i))
        return dataclass_list

    # TODO we will probably want to cache these
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
            return False, None

        blocked = await self.blocklist_collection.find_one({"id": member.id})
        if blocked is not None:
            return True, BlockReason.BLOCKED_USER

        roles = member.roles

        blocked = await self.blocklist_collection.find_one(filter={"id": {"$in": [r.id for r in roles]}})
        if blocked is not None:
            return True, BlockReason.BLOCKED_ROLE

        if not self.is_valid_account_age(member):
            return True, BlockReason.ACCOUNT_AGE
        if not self.is_valid_guild_age(member):
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
