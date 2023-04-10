import asyncio

from sys import platform
from vkbottle.bot import Bot, Message
from plugins.binder import Binder
from plugins.cpp import Downoloader
from plugins.states import SendMessageState
from plugins.database import Database

if 'win' in platform:
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

loop = asyncio.get_event_loop()
downoloader = Downoloader()
binder = Binder(
    cpp=downoloader,
    loop=loop
)
database = Database(filename='users.bin')
vk = Bot(token=binder.sync_get_config()['token'])
vk.ob.vbml_ignore_case = True


@vk.on.private_message(state=SendMessageState.message)
async def send_message(message: Message):
    if message.text.splitlines() < 6:
        await message.send('''АВТОМАТИЧЕСКОЕ СООБЩЕНИЕ
Заполните следующую анкету и в скором времени с вами свяжутся:
1. (!!!) Ваш возраст
2. (!!!) Ваш город (или место проживания. Например: Большой Букор)
3. (!!!) Ваше имя и фамилию
4. (!!!) На сколько общительны (по 10-бальной шкале)
5. (!!!) Почему хотите к нам
6. (!!!) Где увидели рекламу

Если вы заполнили все поля, вам напишет специальный аккаунт и назначит встречу,\
на которой вы прогуляетесь с представителем.

Мы не приносим кому-либо жертвы.
Сатанизм - не религия, сатанизм - философия
Подробнее про "Сатанизм Лавея":
https://ru.wikipedia.org/wiki/Сатанизм_Лавея''')
    else:
        await message.answer('Ваша анкуета теперь на рассмотрении. Крайне советуекм пригласить других людей,\
будем рады всем!')
        await vk.state_dispenser.delete(message.from_id)
        await database.reg(message.from_id, message.text)
        for admin in (await binder.get_config())['admins']:
            await vk.api.messages.send(
                peer_id=admin,
                user_id=admin,
                random_id=0,
                message=f'Человек @id{message.from_id} желает присоединится!\nАнкета: {message.text}'
            )
            await asyncio.sleep(1)


@vk.on.private_message(text='admin <i>')
async def admin_command_handler(message: Message, i: str):
    parameters = await binder.get_config()
    if message.from_id in parameters['admins']:
        options = i.lower().split()
    if options[0] == 'info':
        await message.answer('''СПИСОК ВСЕХ КОММАНД АДМИНИСТРАЦИИ
admin delete (id) - удаляет ID из базы данных
admin send (id) (text) - отправить сообщение поределённому человеку
admin get - поуулчить список всех кто внутри базы данных
РАЗРАБОТАНО АМБИЦИЯМИ САВЕЛЬЕВА ЯКОВА''')
    elif options[0] == 'delete':
        if (await database.exists(id=options[1])):
            await database.delete(id=int(options[1]))
            await message.answer('Успешно удалено')
        else:
            await message.answer('Этой записи нет в базе данных!')
    elif options[0] == 'send':
        await vk.api.messages.send(
            peer_id=int(options[1]),
            user_id=int(options[1]),
            random_id=0,
            message=i.split(' ', 2)[-1]
        )
        await message.answer('успешно отправлено')
    elif options[0] == 'get':
        db = await database.get()
        text = ''
        for num, row in enumerate(db):
            text += f'№{num + 1}\nID: {row["id"]}\nАнкета: {row["message"]}\n\n'
        await message.answer(f'Список всех анкет:\n{text}')
    else:
        await message.send('Неверная команда. Список всех комманд в "admin info"')


@vk.on.private_message()
async def firstest(message: Message):
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

if __name__ == "__main__":
    vk.run_forever()
