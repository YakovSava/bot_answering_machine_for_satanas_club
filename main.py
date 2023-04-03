import asyncio

from sys import platform
from vkbottle import ABCRule, CtxStorage
from vkbottle.bot import Bot, Message
from plugins.binder import Binder
from plugins.cpp import Downoloader
from plugins.states import SendMessageState

if 'win' in platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

class Firstes(ABCRule[Message]):
    async def check(self, message:Message):
        return message.conversation_message_id < 10

loop = asyncio.get_event_loop()
downoloader = Downoloader()
binder = Binder(
    cpp=downoloader,
    loop=loop
)
configuration = binder.sync_get_config()
storage = CtxStorage()
vk = Bot(token=configuration['token'])

@vk.on.private_message(Firstes())
async def firstest(message:Message):
    await message.answer('''АВТОМАТИЧЕСКОЕ СООБЩЕНИЕ
Заполните следующую анкету и в скором времени с вами свяжутся:
1. Ваш возраст
2. Ваш город (или место проживания. Например: Большой Букор)
3. Ваше имя и фамилию
4. На сколько общительны (по 10-бальной шкале)
5. Почему хотите к нам
6. Где увидели рекламу

Если вы заполнили все поля, вам напишет специальный аккаунт и назначит встречу,\
на которой вы прогуляетесь с представителем.

Мы не приносим кому-либо жертвы.
Сатанизм - не религия, сатанизм - философия
Подробнее про "Сатанизм Лавея":
https://ru.wikipedia.org/wiki/Сатанизм_Лавея''')
    await vk.state_dispenser.set(message.from_id, SendMessageState.message)

@vk.on.private_message(state=SendMessageState.message)
async def send_message(message:Message):
    pass

if __name__ == "__main__":
    vk.run_forever()