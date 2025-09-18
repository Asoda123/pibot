import os
from aiogram import Bot, Dispatcher, types
from aiogram import executor
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from googletrans import Translator
from humanfriendly.terminal import message
from pyparsing import replaced_by_pep8

import eqs_solver as eq_s
import gt_ratings as gt
import read_sessions as sess
import transl as tl
import user_storage as us

BOT_TOKEN = '8346525529:AAElTNkTAmjbbTv5Cp8e_wM0kM7KYA2iEec'

tr = Translator()
user_equations = {}
maths_chat_is_active = False
physics_chat_is_active = False

bot = Bot(token=BOT_TOKEN)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)

class Bot_states(StatesGroup):
    st1 = State()
    st2 = State()
    st3 = State()
    st4 = State()
    maths = State()
    physics = State()
    graph_state = State()
    lever_state = State()
    help = State()
    rate = State()

rating_kb = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text='⭐️',callback_data='1'),
     InlineKeyboardButton(text='⭐️',callback_data='2'),
     InlineKeyboardButton(text='⭐️',callback_data='3'),
     InlineKeyboardButton(text='⭐️',callback_data='4'),
     InlineKeyboardButton(text='⭐️',callback_data='5')],
    [InlineKeyboardButton(text="✅",callback_data='sub')]
])

lang_keyboard = InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text='🏴󠁧󠁢󠁥󠁮󠁧󠁿', callback_data="en"),
        InlineKeyboardButton(text='🇩🇪', callback_data="de")],
        [InlineKeyboardButton(text='🇪🇸', callback_data="es"),
         InlineKeyboardButton(text='🇯🇵', callback_data="ja")],
        [InlineKeyboardButton(text='🇺🇦', callback_data="uk")]])

def get_kb(USER_ID):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=tl.set_to_lang('add_eqs', USER_ID), callback_data="your equations")],
        [InlineKeyboardButton(text=tl.set_to_lang('solve_eqs', USER_ID), callback_data="solve your equations")],
        [InlineKeyboardButton(text=tl.set_to_lang('del_eqs', USER_ID), callback_data="del your equations")],
        [InlineKeyboardButton(text=tl.set_to_lang('show_eqs', USER_ID), callback_data="show equations")],
        [InlineKeyboardButton(text=tl.set_to_lang('reg_calc', USER_ID), callback_data="regular calculation")],
        [InlineKeyboardButton(text=tl.set_to_lang('show_graph', USER_ID), callback_data="show graph")],
        [InlineKeyboardButton(text=tl.set_to_lang('back', USER_ID), callback_data="back")]])

def get_kb1(USER_ID):
    Inlinekb = InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text=tl.set_to_lang('maths', USER_ID), callback_data="maths"),
             InlineKeyboardButton(text=tl.set_to_lang('physics', USER_ID), callback_data="physics")],
            [InlineKeyboardButton(text=tl.set_to_lang('help', USER_ID), callback_data="help")],
            [InlineKeyboardButton(text=tl.set_to_lang('change_lang', USER_ID), callback_data="change_lang")],
            [InlineKeyboardButton(text=tl.set_to_lang('htu', USER_ID), callback_data="htu")]])            # How To Use
    if us.get_user(USER_ID)['role'] == 'admin':
        Inlinekb.add(InlineKeyboardButton(text=tl.set_to_lang('admin', USER_ID), callback_data="admin"),
                     InlineKeyboardButton(text='⭐'+gt.get_rating(USER_ID)+'⭐️', callback_data='nothing'))
    return Inlinekb

def get_kb2(USER_ID):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=tl.set_to_lang('levers', USER_ID), callback_data="lever")],
        [InlineKeyboardButton(text=tl.set_to_lang('back', USER_ID), callback_data="back")]])

def back_kb(USER_ID):
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=tl.set_to_lang('back', USER_ID), callback_data="back")]])

async def get_student_help_kb(USER_ID):
    translated = await translate_text("Start a chat", USER_ID)
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text=translated.text, callback_data='start_chat')]])

async def translate_text(text, user_id):
    return await tr.translate(text, dest=us.get_user(user_id)['lang'])


@dp.message_handler(commands='start')
async def start_command(message : types.Message):
    global USER_ID
    USER_ID = message.from_user.id
    user = us.get_user(message.from_user.id)
    if user:
        user_equations.update({str(message.from_user.id): us.get_user(message.from_user.id).get('eqs')})
    else:
        us.add_user(message.from_user.id, [], message.from_user.username)
    choose_keyboard1 = get_kb1(USER_ID)
    choose_keyboard = get_kb1(USER_ID)
    choose_keyboard2 = get_kb2(USER_ID)

    if not maths_chat_is_active and not physics_chat_is_active:
        await message.answer(tl.set_to_lang('greeting', USER_ID), reply_markup=choose_keyboard1)
    elif maths_chat_is_active:
        await message.answer(tl.set_to_lang('wuwtc', USER_ID), reply_markup=choose_keyboard)
    elif physics_chat_is_active:
        await message.answer(tl.set_to_lang('wuwtc', USER_ID), reply_markup=choose_keyboard2)


@dp.callback_query_handler(text=['maths','physics','change_lang','help','htu'])
async def get_to_chat(call : types.CallbackQuery):
    global maths_chat_is_active
    global physics_chat_is_active
    global USER_ID
    USER_ID = call.from_user.id
    info = call.data
    if info == 'maths':
        choose_keyboard = get_kb(USER_ID)
        maths_chat_is_active = True
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=tl.set_to_lang('wuwtc', USER_ID),
            reply_markup=choose_keyboard
        )
    if info == 'physics':
        choose_keyboard2 = get_kb2(USER_ID)
        physics_chat_is_active = True
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=tl.set_to_lang('wuwtc', USER_ID),
            reply_markup=choose_keyboard2
        )
    if info == 'change_lang':
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=tl.set_to_lang('change_lang', USER_ID),
            reply_markup=lang_keyboard
        )

    if info == 'htu':
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=tl.set_to_lang('htuF', USER_ID),
            reply_markup=back_kb(call.from_user.id)
        )

    if info == 'help' and us.get_user(call.from_user.id)['role'] == 'user':
        # translated = await translate_text("We are finding a teacher for you! Wait a second", call.from_user.id)
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='⏳'
        )
        users = us.load_users()
        for teacher_id in users:
            if users[teacher_id]['role'] == 'admin':
                translated = await translate_text("There a request from a student!", call.from_user.id)
                await bot.send_message(teacher_id, text=translated.text)

        sess.add_user_to_queue(call.from_user.id)


    elif info == 'help' and us.get_user(call.from_user.id)['role'] == 'admin':

        # translated = await translate_text("We are finding a student for you! Wait a second", call.from_user.id)
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text='⏳'
        )
        if sess.add_teacher_queue(call.from_user.id):
            sessions = sess.load_info()
            chat_id = sess.find_session_id(call.from_user.id)
            student_id = sessions.get(chat_id).get('student').get('id')
            sess.teacher_to_true()
            translated = await translate_text('Student is found!\nStart your chat.', call.from_user.id)
            translated1 = await translate_text("Teacher has been found!\nStart your chat.", call.from_user.id)
            translated2 = await translate_text('to end the chat', call.from_user.id)

            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=translated.text + "\n/stop " + translated2.text
            )
            # await bot.send_message(student_id, text=translated1.text+'\n/stop', reply_markup= await get_student_help_kb(student_id))
            await bot.send_message(student_id, text=translated1.text + '\n/stop ' + translated2.text)
            opposite_state = dp.current_state(user=student_id, chat=student_id)
            await opposite_state.set_state(Bot_states.help.state)
            await Bot_states.help.set()


        else:
            translated = await translate_text('No requests from students', call.from_user.id)
            await bot.edit_message_text(
                chat_id=call.message.chat.id,
                message_id=call.message.message_id,
                text=translated.text
            )







@dp.callback_query_handler(text=['your equations', 'regular calculation', "solve your equations",
                                 "del your equations", 'back', 'show equations', 'show graph',
                                 'start_chat'])
async def write_eq(call: types.CallbackQuery):
    info = call.data
    global maths_chat_is_active
    if info == "your equations":                                                                                        # ADD EQUATIONS
        translated = await translate_text("Write down equations using commas"+"(eg: a*x**2 + b*x + c = d)", call.from_user.id)
        await call.message.answer(translated.text)
        await Bot_states.st1.set()
    elif info == "regular calculation":                                                                                 # REGULAR CALCULATIONS
        translated = await translate_text("Write down what you need to solve using commas (eg: 1 + 2 / 2)",call.from_user.id)
        await call.message.answer(translated.text)
        await Bot_states.st2.set()
    elif info == "solve your equations":                                                                                # SOLVE
        translated = await translate_text("Your solved equations!\n🔽🔽🔽🔽",call.from_user.id)
        await call.message.answer(translated.text)
        res = [eq_s.solve_eq(i) for i in us.get_user(call.from_user.id)['eqs']]
        for i, i1 in enumerate(res):
            await call.message.answer(f"{us.get_user(call.from_user.id)['eqs'][i]}  ----->  {i1}")

    elif info == "del your equations":
        translated = await translate_text("Write down what equation you want to delete!(write a number)\n",call.from_user.id)
        eqs = us.get_user(call.from_user.id)['eqs']
        if len(eqs) == 0:
            translated = await translate_text("You have no equations so far!\n", call.from_user.id)
            await call.message.answer(translated.text)
        else:
            await call.message.answer(translated.text)
            for i, i1 in enumerate(eqs):
                await call.message.answer(f"{i+1} : {i1}")
            await Bot_states.st4.set()

    elif info == 'show equations':                                                                                      # SHOW EQUATIONS
        try:
            eqs = us.get_user(call.from_user.id)['eqs']
            if len(eqs) == 0:
                translated = await translate_text("You have no equations so far", call.from_user.id)
                await call.message.answer(translated.text)
            else:
                translated = await translate_text("Your equations\n🔽🔽🔽🔽", call.from_user.id)
                await call.message.answer(translated.text)
                for i, i1 in enumerate(eqs):
                    await call.message.answer(f"{i + 1} : {i1}")
        except:
            translated = await translate_text("Error. Try again", call.from_user.id)
            await call.message.answer(translated.text)

    elif info == 'show graph':                                                                                          # SHOW GRAPH
        translated = await translate_text("Write down a function (eg: 1 / x + 2x)",call.from_user.id)
        await call.message.answer(translated.text)
        await Bot_states.graph_state.set()
    elif info == 'start_chat':
        await Bot_states.help.set()


    elif info == 'back':
        choose_keyboard1 = get_kb1(call.from_user.id)
        maths_chat_is_active = False
        await bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=tl.set_to_lang('wuwtc', USER_ID),
            reply_markup=choose_keyboard1
        )

@dp.callback_query_handler(text=['en','uk','de','es','ja'])
async def get_to_chan(call : types.CallbackQuery):
    info = call.data
    us.add_or_update_info(call.from_user.id, lang=info)
    await bot.edit_message_text(
        chat_id=call.message.chat.id,
        message_id=call.message.message_id,
        text=tl.set_to_lang('greeting', USER_ID),
        reply_markup=get_kb1(USER_ID)
    )



@dp.message_handler(state=Bot_states.help, commands='stop')
async def del_chat(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    opponent_id = sess.find_opponent_id(user_id)

    translated = await translate_text("Chat was ended.", message.from_user.id)
    await message.answer(translated.text)
    await bot.send_message(chat_id=opponent_id,text=translated.text)


    # if us.get_user(message.from_user.id)['role'] == 'user':
    for i in [user_id,opponent_id]:
        if us.get_user(i)['role'] == 'user':
            await bot.send_message(chat_id=i,
                               text='/⭐️⭐️⭐️⭐️⭐️',
                               reply_markup=rating_kb)
            student_state = dp.current_state(user=i, chat=i)
            await student_state.set_state(Bot_states.rate.state)
        else:
            opponent_state = dp.current_state(user=i, chat=i)
            await opponent_state.reset_state()

    # else:
    #     opponent_session = dp.current_state(user=opponent_id,chat=opponent_id)
    #     await opponent_session.set_state(Bot_states.)
    #     await state.reset_state(with_data=False)

@dp.callback_query_handler(text=['1','2','3','4','5','sub'], state=Bot_states.rate)
async def get_rating(call: types.CallbackQuery, state: FSMContext):
    student_id = sess.find_student_id(call.from_user.id)
    info = call.data
    if info != 'sub':
        rating = int(info)
        await state.update_data(rating=rating)
        await   bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=     int(info)*'⭐️'+'/⭐️⭐️⭐️⭐️⭐️',
            reply_markup=rating_kb
        )
        await call.answer()
    elif info == 'sub':
        data = await state.get_data()
        rating_value = data.get('rating')
        gt.create_a_rating(student_id, rating_value)
        sess.del_session(call.from_user.id)
        await bot.delete_message(chat_id=call.from_user.id, message_id=call.message.message_id)
        await state.reset_state(with_data=False)



@dp.message_handler(state=Bot_states.help)
async def help_chat(message: types.Message, state: FSMContext):
    info = message.text
    if sess.check_whether_queue_is_full(message.from_user.id):
        sess.add_message(info,message.from_user.id)
        await bot.send_message(chat_id=sess.find_opponent_id(message.from_user.id), text=sess.get_last_message(message.from_user.id))
    else:
        await state.reset_state(with_data=False)


@dp.message_handler(state=Bot_states.st1)
async def get_eqs(message: types.Message, state: FSMContext):
    try:
        info = message.text.split(',')
        old_eqs = us.get_user(message.from_user.id)['eqs']
        us.add_or_update_info(message.from_user.id,eqs=old_eqs+info)
        translated = await translate_text("All is added!", message.from_user.id)
        await message.answer(translated.text)
        await state.reset_state(with_data=False)
    except:
        translated = await translate_text("Error. Try again", message.from_user.id)
        await message.answer(translated.text)

@dp.message_handler(state=Bot_states.st2)
async def reg_calc(message: types.Message, state: FSMContext):
    try:
        info = message.text.split(",")
        res = [str(eval(i)) for i in info]
        await message.answer('\n'.join(res))
        await state.reset_state(with_data=False)
    except:
        translated = await translate_text("Error. Try again", message.from_user.id)
        await message.answer(translated.text)


@dp.message_handler(state=Bot_states.st4)
async def del_eq(message: types.Message, state: FSMContext):
    info = message.text
    try:
        info = int(info)
        eqs = us.get_user(message.from_user.id)['eqs']
        eqs.pop(info-1)
        us.add_or_update_info(message.from_user.id, eqs=eqs)
        translated = await translate_text("Equation has been removed!", message.from_user.id)
        await message.answer(translated.text)
        await state.reset_state(with_data=False)
    except:
        translated = await translate_text("Error. Write a number", message.from_user.id)
        await message.answer(translated.text)


@dp.message_handler(state=Bot_states.graph_state)
async def graph_show(message: types.Message, state: FSMContext):
    import graphs12
    info = message.text
    graphs12.set_user_id(message.from_user.id)
    graphs12.set_y(info)

    script_dir = os.path.dirname(os.path.abspath(__file__))
    full_image_path = os.path.join(script_dir, graphs12.get_f_n())
    print(full_image_path)
    print(f"DEBUG: Attempting to send file from: {full_image_path}")
    if not os.path.exists(full_image_path):
        translated = await translate_text("Error. Try again", message.from_user.id)
        await message.reply(translated.text)
        print(f"DEBUG: File '{full_image_path}' does not exist.")
        return
    try:
        with open(full_image_path, "rb") as photo:
            await bot.send_photo(message.from_user.id, photo)
        print(f"DEBUG: Successfully attempted to send '{full_image_path}'.")
    except Exception as e:
        await message.reply(f"Виникла помилка під час надсилання фото: {e}")
        print(f"DEBUG: An error occurred during photo send: {e}")
    os.remove(full_image_path)
    await state.reset_state(with_data=False)


@dp.callback_query_handler(text=['lever'])
async def write_eq(call: types.CallbackQuery):
    info = call.data
    if info == ('lever'):
        translated = await translate_text('Write down l1,l2 (in M) using commas. (eg: "1,2")',call.from_user.id)
        await call.message.answer(translated.text)
        await Bot_states.lever_state.set()

@dp.message_handler(state=Bot_states.lever_state)
async def lever_show(message: types.Message, state: FSMContext):
    try:
        info = [float(i) for i in message.text.split(',')]
        import turtle_lever
        turtle_lever.set_user_id(message.from_user.id)
        turtle_lever.create_lever(info[0],info[1])

        script_dir = os.path.dirname(os.path.abspath(__file__))
        full_image_path = os.path.join(script_dir, f'canv_{message.from_user.id}.png')

        try:
            with open(full_image_path, "rb") as photo:
                await bot.send_photo(message.from_user.id, photo)
            print(f"DEBUG: Successfully attempted to send '{full_image_path}'.")
        except Exception as e:
            # translated = await translate_text("Error. Try again", message.from_user.id)
            # await message.reply(translated.text)
            print(f"DEBUG: An error occurred during photo send: {e}")
        os.remove(full_image_path)
        os.remove(f'temp_canv_{message.from_user.id}.ps')
        await state.reset_state(with_data=False)
    except:
        translated = await translate_text("Error. Try again", message.from_user.id)
        await message.reply(translated.text)



if __name__ == '__main__':
    executor.start_polling(dp)
