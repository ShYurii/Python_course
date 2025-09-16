import telebot
from telebot.types import Message
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import random
from property import TOKEN

bot = telebot.TeleBot(TOKEN)

secret_number = {}

jokes_ua = [
    "Чому програмісти не ходять на вулицю? Бо там багато помилок.",
    "Програміст купив собі каву, бо без неї код не компілюється.",
    "Коли програмісти говорять 'це працює', вони мають на увазі 'поки що працює'."
]

movies_by_genre = {
    "Пригоди": ["Indiana Jones", "Pirates of the Caribbean", "Jumanji"],
    "Фантастика": ["Inception", "Interstellar", "The Matrix"],
    "Комедія": ["The Mask", "Superbad", "Step Brothers"],
    "Жахи": ["It", "The Conjuring", "A Quiet Place"]
}

game_genres = {
    "логічні": ["Вгадай число 🎲", "Судоку 🧩"],
    "стратегічні": ["Шахи ♟️", "Морський бій ⚓"],
    "аркадні": ["Камінь-ножиці-папір ✂️", "Змійка 🐍"]
}

music_genres = {
    "Поп": ["Imagine Dragons - Believer", "Dua Lipa - Levitating", "Ed Sheeran - Shape of You"],
    "Рок": ["Linkin Park - Numb", "Queen - Bohemian Rhapsody", "Nirvana - Smells Like Teen Spirit"],
    "Класика": ["Beethoven - Moonlight Sonata", "Mozart - Eine kleine Nachtmusik", "Bach - Toccata and Fugue"],
    "Хіп-хоп": ["Eminem - Lose Yourself", "Drake - God's Plan", "Kendrick Lamar - HUMBLE."]
}


def main_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    keyboard.add(
        InlineKeyboardButton("🎬 Фільми", callback_data="movie"),
        InlineKeyboardButton("🎵 Музика", callback_data="music"),
        InlineKeyboardButton("🎮 Ігри", callback_data="game"),
        InlineKeyboardButton("😂 Анекдот", callback_data="joke"),
        InlineKeyboardButton("🎲 Вгадай число", callback_data="guess_number"),
        InlineKeyboardButton("❌ Завершити", callback_data="exit")
    )
    return keyboard


def movie_genre_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for genre in movies_by_genre.keys():
        keyboard.add(InlineKeyboardButton(genre, callback_data=f"genre_movie_{genre}"))
    keyboard.add(InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
    return keyboard


def game_genre_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for genre in game_genres.keys():
        keyboard.add(InlineKeyboardButton(genre, callback_data=f"genre_game_{genre}"))
    keyboard.add(InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
    return keyboard


def music_genre_menu():
    keyboard = InlineKeyboardMarkup(row_width=2)
    for genre in music_genres.keys():
        keyboard.add(InlineKeyboardButton(genre, callback_data=f"genre_music_{genre}"))
    keyboard.add(InlineKeyboardButton("⬅️ Назад", callback_data="main_menu"))
    return keyboard


@bot.message_handler(commands=["start"])
def start(message: Message):
    bot.send_message(
        message.chat.id,
        "Привіт 👋 Я твій розважальний бот!\nВибери категорію:",
        reply_markup=main_menu()
    )


def recommend_movie(chat_id: int):
    bot.send_message(chat_id, "Оберіть жанр фільму:", reply_markup=movie_genre_menu())


def recommend_music(chat_id: int):
    bot.send_message(chat_id, "🎵 Оберіть жанр музики:", reply_markup=music_genre_menu())


def recommend_game(chat_id: int):
    bot.send_message(chat_id, "Оберіть жанр гри:", reply_markup=game_genre_menu())


def tell_joke(chat_id: int):
    joke = random.choice(jokes_ua)
    bot.send_message(chat_id, f"😂 {joke}")


def start_game(chat_id: int):
    number = random.randint(1, 10)
    secret_number[chat_id] = number
    bot.send_message(chat_id, "🎲 Я загадав число від 1 до 10. Спробуй відгадати!")


def is_guess_number(message: Message):
    return message.chat.id in secret_number


@bot.message_handler(func=is_guess_number)
def guess_number(message: Message):
    chat_id = message.chat.id
    if not message.text.isdigit():
        bot.send_message(chat_id, "❌ Введи, будь ласка, число від 1 до 10.")
        return

    guess = int(message.text)
    number = secret_number[chat_id]

    if guess == number:
        bot.send_message(chat_id, "🎉 Ти вгадав! Вітаю!")
        del secret_number[chat_id]
    elif guess < number:
        bot.send_message(chat_id, "🔼 Загадане число більше. Спробуй ще раз!")
    else:
        bot.send_message(chat_id, "🔽 Загадане число менше. Спробуй ще раз!")


def all_callbacks(call):
    return True


@bot.callback_query_handler(func=all_callbacks)
def callback_handler(call):
    chat_id = call.message.chat.id
    if call.data == "movie":
        recommend_movie(chat_id)

    elif call.data.startswith("genre_movie_"):
        genre = call.data[len("genre_movie_"):]
        if genre in movies_by_genre:
            movie = random.choice(movies_by_genre[genre])
            bot.send_message(chat_id, f"🎬 Рекомендую фільм у жанрі '{genre}': {movie}")

    elif call.data == "music":
        recommend_music(chat_id)

    elif call.data.startswith("genre_music_"):
        genre = call.data[len("genre_music_"):]
        if genre in music_genres:
            song = random.choice(music_genres[genre])
            bot.send_message(chat_id, f"🎵 Рекомендую музику в жанрі '{genre}': {song}")

    elif call.data == "game":
        recommend_game(chat_id)

    elif call.data.startswith("genre_game_"):
        genre = call.data[len("genre_game_"):]
        if genre in game_genres:
            game = random.choice(game_genres[genre])
            bot.send_message(chat_id, f"🎮 Рекомендую гру у жанрі '{genre}': {game}")

    elif call.data == "joke":
        tell_joke(chat_id)
    elif call.data == "guess_number":
        start_game(chat_id)
    elif call.data == "main_menu":
        bot.send_message(chat_id, "Головне меню:", reply_markup=main_menu())
    elif call.data == "exit":
        bot.send_message(chat_id, "👋 До зустрічі! Бот завершив роботу.")
        if chat_id in secret_number:
            del secret_number[chat_id]


bot.polling(none_stop=True)
