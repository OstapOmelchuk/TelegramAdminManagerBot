import asyncio
import logging
from main import dp, bot
from aiogram.types import ChatJoinRequest
from db.schemas.tables import User
from datetime import datetime
from config import CHAT_ID

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


async def on_startup(dp):
    from db.db_connection import on_startup
    await on_startup(dp)
    await check_users()

    print("bot has been started its work.")


async def check_users():
    while True:
        users = await User.query.gino.all()
        now = datetime.now()
        for user in users:
            if (not user.is_admin) and (user.subscription_end_date and user.subscription_end_date < now):
                try:
                    await bot.ban_chat_member(chat_id=CHAT_ID, user_id=user.user_id)
                    await bot.unban_chat_member(chat_id=CHAT_ID, user_id=user.user_id)
                    await User.update.values(
                        subscription_status=False,
                        subscription_start_date=None,
                        subscription_end_date=None
                    ).where(User.user_id == user.user_id).gino.status()

                    logger.info(f"User was kicked:\n- username - {user.username}")

                except Exception as err:
                    logger.info(f"Kick user error:\n- username - {user.username}\n error - {err}")

        logger.info(f"The 'kick' process was done successfully")
        await asyncio.sleep(10800)  # sleep на 3 години


@dp.chat_join_request_handler()
async def handle_join_request(request: ChatJoinRequest):
    logger.info(request)

    try:
        user = await User.query.where(User.user_id == request.from_user.id).gino.first()
        if user and user.subscription_status:
            await request.approve()
        else:
            await request.decline()
    except Exception as err:
        logger.info(f"Error occurred while approving user to join the private chat: {err}")
