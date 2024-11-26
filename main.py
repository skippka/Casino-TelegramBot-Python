import telebot
import random
import time
from game_file import get_user_data, update_user_data

bot = telebot.TeleBot('6416697474:AAH2y6UeM0Rpdg8YiwS6FB0yv2uHh12Z73I')


@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '''
Привет! 👋 Я бот — Вованчик казино 🎰

Со мной ты точно не заскучаешь! Ты можешь как играть один, так и играть с друзьями. 🔥
А вот тут все игры — /game 
··········································
Есть вопросы? — не проблема 👉 /help 
    ''')

@bot.message_handler(commands=['help'])
def help(message):
    bot.send_message(message.chat.id, '''
Привет! 
Здесь собраны все команды, которые тебе могут понадобиться:

/game - Все игры
/balance - Баланс 
/bonus - Бонус
Скоро: /give - Передать коины
    ''')

@bot.message_handler(commands=['bonus', 'бонус'])
def bonus(message):
    user_id = message.chat.id
    user_data = get_user_data(user_id)
    bonus_amount = random.randint(1, 500)
    user_data['balance'] += bonus_amount
    update_user_data(user_id, user_data)
    bot.send_message(message.chat.id, f'Тебе начислен бонус: {bonus_amount} Coin')

@bot.message_handler(commands=['game', 'игры'])
def game(message):
    bot.send_message(message.chat.id, '''
Здесь ты можешь поиграть в разные игры!
··········································
Как запустить игру 👇

🎰 /casino [ставка]
/crash [ставка]
Пример: /casino 100
Пример: /crash 100
    ''')

@bot.message_handler(commands=['balance', 'balanse'])
def balance(message):
    user_id = message.chat.id
    user_data = get_user_data(user_id)
    bot.send_message(message.chat.id, f'''
Баланс: {user_data['balance']} Coin
····················
Сыграно игр: {user_data['gameplay']}
    ''')

@bot.message_handler(commands=['casino'])
def casino(message):
    user_id = message.chat.id
    user_data = get_user_data(user_id)
    try:
        args = message.text.split()
        if len(args) != 2 or not args[1].isdigit():
            bot.send_message(message.chat.id, "Укажите ставку в виде числа. Пример: /casino 100")
            return

        stake = int(args[1])
        if stake > user_data['balance']:
            bot.send_message(message.chat.id, "Недостаточно средств на балансе!")
            return
        if stake <= 0:
            bot.send_message(message.chat.id, "Ставка должна быть больше 0!")
            return

        multiplier = round(random.uniform(0, 2), 1)
        win = int(stake * multiplier)
        user_data['balance'] += win - stake
        user_data['gameplay'] += 1

        bot.send_message(message.chat.id, f'''
Тебе выпало: {multiplier} 🎲
Выигрыш: {win} Coin
Новый баланс: {user_data['balance']} Coin
        ''')

        update_user_data(user_id, user_data)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(commands=['crash'])
def crash(message):
    user_id = message.chat.id
    user_data = get_user_data(user_id)
    try:
        args = message.text.split()
        if len(args) != 2 or not args[1].isdigit():
            bot.send_message(message.chat.id, "Укажите ставку в виде числа. Пример: /crash 100")
            return

        stake = int(args[1])
        if stake > user_data['balance']:
            bot.send_message(message.chat.id, "Недостаточно средств на балансе!")
            return
        if stake <= 0:
            bot.send_message(message.chat.id, "Ставка должна быть больше 0!")
            return

        crash_point = round(random.uniform(1.1, 10), 1)
        user_choice = round(random.uniform(1.1, crash_point), 1)
        user_data['gameplay'] += 1

        if user_choice >= crash_point:
            bot.send_message(message.chat.id, f"Твой множитель не дошел до {crash_point}! Ты проиграл!")
            user_data['balance'] -= stake
        else:
            win = int(stake * user_choice)
            user_data['balance'] += win - stake
            bot.send_message(message.chat.id, f"Ты вышел с множителем {user_choice} и выиграл {win} Coin!")

        bot.send_message(message.chat.id, f"Твой новый баланс: {user_data['balance']} Coin")
        update_user_data(user_id, user_data)

    except Exception as e:
        bot.send_message(message.chat.id, f"Произошла ошибка: {str(e)}")

@bot.message_handler(func=lambda message: 'гоша' in message.text.lower())
def handle_gosha(message):
    bot.send_message(message.chat.id, "Ты просто классный чувак!")

def poll_bot():
    while True:
        try:
            bot.polling(non_stop=True)
        except Exception as e:
            print(f"Ошибка: {e}")
            time.sleep(5)

if __name__ == '__main__':
    poll_bot()
