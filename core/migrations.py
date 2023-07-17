import datetime
import re

from core import blocklist
from core.models import getLogger

logger = getLogger(__name__)

old_format_matcher = re.compile("by ([\w]*#[\d]{1,4})(?: until <t:(\d*):f>)?.")


def _convert_legacy_v2_block_format(k, v: dict, block_type: blocklist.BlockType) -> blocklist.BlocklistEntry:
    blocked_by = int(v["blocked_by"])
    if "until" in v:
        # todo make sure this is the correct from format
        blocked_until = datetime.datetime.fromisoformat(v["until"])
    else:
        blocked_until = None
    if "reason" in v:
        reason = v["reason"]
    else:
        reason = None
    blocked_ts = datetime.datetime.fromisoformat(v["blocked_at"])
    return blocklist.BlocklistEntry(
        id=int(k),
        expires_at=blocked_until,
        reason=reason,
        timestamp=blocked_ts,
        blocking_user_id=blocked_by,
        type=block_type
    )


def _convert_legacy_block_format(k, v: str, block_type: blocklist.BlockType) -> blocklist.BlocklistEntry:
    match = old_format_matcher.match(v)
    # blocked_by = match.group(1)
    blocked_until = match.group(2)
    if blocked_until is not None:
        blocked_until = datetime.datetime.fromtimestamp(int(blocked_until), tz=datetime.timezone.utc)

    return blocklist.BlocklistEntry(
        id=int(k),
        expires_at=blocked_until,
        reason=f"migrated from old format `{v}`",
        timestamp=datetime.datetime.utcnow(),
        # I'm not bothering to fetch the user object here, discords username migrations will have broken all of them
        blocking_user_id=0,
        type=block_type
    )


async def _convert_legacy_block_list(foo: dict, blocklist_batch: list[blocklist.BlocklistEntry],
                                     block_type: blocklist.BlockType, bot) -> int:
    skipped = 0

    for k, v in foo.items():
        # handle new block format
        if type(v) is dict:
            block = _convert_legacy_v2_block_format(k, v, block_type=block_type)
            if block.expires_at is not None and block.expires_at < datetime.datetime.now(datetime.timezone.utc):
                logger.debug("skipping expired block entry")
                skipped += 1
                continue
            logger.debug(f"migrating new format {v}")
            blocklist_batch.append(block)

            continue

        match = old_format_matcher.match(v)
        blocked_by = match.group(1)
        blocked_until = match.group(2)
        if blocked_until is not None:
            blocked_until = datetime.datetime.fromtimestamp(int(blocked_until), tz=datetime.timezone.utc)

        # skip this item if blocked_until occurred in the past
        if blocked_until is not None and blocked_until < datetime.datetime.now(datetime.timezone.utc):
            logger.debug("skipping expired block entry")
            skipped += 1
            continue

        logger.debug(f"migrating id:{k} ts:{blocked_until} blocker:{blocked_by}")

        blocklist_batch.append(blocklist.BlocklistEntry(
            id=int(k),
            expires_at=blocked_until,
            reason=f"migrated from old format `{v}`",
            timestamp=datetime.datetime.utcnow(),
            # I'm not bothering to fetch the user object here, discords username migrations will have broken all of them
            blocking_user_id=0,
            type=blocklist.BlockType.USER
        ))
        if len(blocklist_batch) >= 100:
            await bot.api.db.blocklist.insert_many([x.__dict__ for x in blocklist_batch])
            blocklist_batch.clear()

    return skipped


async def migrate_blocklist(bot):
    start_time = datetime.datetime.utcnow()

    blocked_users = bot.blocked_users
    logger.info(f"preparing to migrate blocklist")
    skipped = 0

    blocklist_batch: list[blocklist.BlocklistEntry] = []
    logger.info(f"preparing to process {len(blocked_users)} blocked users")
    skipped += await _convert_legacy_block_list(foo=blocked_users, blocklist_batch=blocklist_batch,
                                                block_type=blocklist.BlockType.USER, bot=bot)
    logger.info(f"processed blocked users")
    logger.info(f"preparing to process {len(bot.blocked_roles)} blocked roles")
    skipped += await _convert_legacy_block_list(foo=bot.blocked_roles, blocklist_batch=blocklist_batch,
                                                block_type=blocklist.BlockType.ROLE, bot=bot)
    logger.info(f"processed blocked roles")

    await bot.api.db.blocklist.insert_many([x.__dict__ for x in blocklist_batch])
    blocklist_batch.clear()

    logger.info(f"Migration complete! skipped {skipped} entries")
    logger.info(f"migrated in {datetime.datetime.utcnow() - start_time}")
    return
