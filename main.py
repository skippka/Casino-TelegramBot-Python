import telebot
import random
import time
from game_file import read_from_file, write_in_file

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
    data = read_from_file()
    bonus_amount = random.randint(1, 500)
    data['balance'] += bonus_amount
    bot.send_message(message.chat.id, f'Тебе начислен бонус: {bonus_amount} Coin')
    write_in_file(data)

@bot.message_handler(commands=['game', 'игры'])
def game(message):
    bot.send_message(message.chat.id, '''
Здесь ты можешь поиграть в разные игры!
··········································
Как запустить игру 👇

🎰 /casino [ставка]
/crash [1.1-10]
Пример: /casino 100
Пример: /crash 3.7
    ''')

@bot.message_handler(commands=['balance', 'balanse'])
def balance(message):
    data = read_from_file()
    bot.send_message(message.chat.id, f'''
Баланс: {data['balance']} Coin
····················
Сыграно игр: {data['gameplay']}
    ''')

@bot.message_handler(commands=['casino'])
def casino(message):
    data = read_from_file()
    try:
        args = message.text.split()
        if len(args) != 2 or not args[1].isdigit():
            bot.send_message(message.chat.id, "Укажите ставку в виде числа. Пример: /casino 100")
            return

        stake = int(args[1])
        if stake > data['balance']:
            bot.send_message(message.chat.id, "Недостаточно средств на балансе!")
            return
        if stake <= 0:
            bot.send_message(message.chat.id, "Ставка должна быть больше 0!")
            return

        multiplier = round(random.uniform(0, 2), 1)
        win = int(stake * multiplier)
        data['balance'] += win - stake
        data['gameplay'] += 1

        bot.send_message(message.chat.id, f'''
Тебе выпало: {multiplier} 🎲
Выигрыш: {win} Coin
Новый баланс: {data['balance']} Coin
        ''')

        write_in_file(data)

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
