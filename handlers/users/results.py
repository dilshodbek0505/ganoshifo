from aiogram import types
from aiogram.dispatcher import FSMContext
from loader import db, dp
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from .company import image_or_video


# #inline keyboard yasash
# async def result_keyboard():
#     button = InlineKeyboardMarkup(row_width=1)
#     button.insert(InlineKeyboardButton(text="Ko'proq bilish ⇣", callback_data="more"))
#     return button

# foydalanuvchilarning natijalarni yuborish
async def send_results(msg: types.Message):
    data = await db.get_results()
    text = str()
    # button = await result_keyboard()
    for result in data:
        text += result['description']
        media = types.MediaGroup()
        count = 0
        if result['file'] != []:
            for i in range(len(result['file'])):
                is_image = await image_or_video(result['file'][i])
                file = open(result['file'][i], 'rb')
                if is_image:
                    if count == 0:
                        media.attach_photo(file, text)
                    else:
                        media.attach_photo(file)
                else:
                    if count == 0:
                        media.attach_video(file, caption=text)
                    else:
                        media.attach_video(file)
                count = 1
            await msg.answer_media_group(media)
        else:
            await msg.answer(text)
