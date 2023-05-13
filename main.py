import ptbot
import telegram
from dotenv import load_dotenv
from pathlib import Path
import os
import random
from pytimeparse import parse


def wait(chat_id, question):
	print(question)
	bot.create_timer(5, choose, chat_id=chat_id, question=question)


def choose(chat_id, question):
	answers = ('да', 'нет', 'это возможно')
	choice = random.choice(answers)
	message = "Думаю, {}".format(choice)
	bot.send_message(TG_CHAT_ID, message)
	print("Мне написал пользователь с ID:", chat_id)
	print("Он спрашивал:", question)
	print("Я ответил:", message)


def notify(chat_id):
	bot.send_message(TG_CHAT_ID, "Время вышло")


def echo(chat_id, question):
	bot.send_message(TG_CHAT_ID, question)


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)
    

def for_count_down(chat_id, question):
	message_id = bot.send_message(TG_CHAT_ID, chat_id)
	bot.create_countdown(parse(question), notify_progress, chat_id=TG_CHAT_ID, message_id=message_id)


def notify_progress(secs_left, chat_id, message_id):
	try:
		bot.update_message(TG_CHAT_ID, message_id, f"Осталось сукунд: {secs_left} \n {render_progressbar(secs_left, 1)}")
	except:
		notify(TG_CHAT_ID)


def main():
	env_path = Path('.') / '.env'
	load_dotenv()
	TG_TOKEN = os.getenv("TG_TOKEN")
	TG_CHAT_ID = '525368545'

	bot = ptbot.Bot(TG_TOKEN)
	bot.reply_on_message(for_count_down)
	bot.run_bot()


if __name__ == "__main__":
	main()
