import ptbot
from dotenv import load_dotenv
import os
from pytimeparse import parse


def notify(chat_id):
    bot.send_message(chat_id, "Время вышло")


def render_progressbar(total, iteration, prefix='', suffix='', length=30, fill='█', zfill='░'):
    iteration = min(total, iteration)
    percent = "{0:.1f}"
    percent = percent.format(100 * (iteration / float(total)))
    filled_length = int(length * iteration // total)
    pbar = fill * filled_length + zfill * (length - filled_length)
    return '{0} |{1}| {2}% {3}'.format(prefix, pbar, percent, suffix)


def for_count_down(chat_id, question, message_id):
    bot.create_countdown(parse(question), notify_progress, chat_id=chat_id, message_id=message_id, num=parse(question))
    bot.create_timer(parse(question) + 1, notify, chat_id=TG_CHAT_ID)


def notify_progress(secs_left, chat_id, message_id, num):
    bot.update_message(TG_CHAT_ID, message_id, f"Осталось сукунд(ы): {secs_left} \n {render_progressbar(num, secs_left)}")


if __name__ == "__main__":
    load_dotenv()
    TG_TOKEN = os.getenv("TG_TOKEN")
    TG_CHAT_ID = os.getenv("TG_CHAT_ID")

    bot = ptbot.Bot(TG_TOKEN)
    message_id = bot.send_message(TG_CHAT_ID, "Бот запущен! \n\n На сколько запустить таймер?")
    bot.reply_on_message(for_count_down, message_id = message_id)
    bot.run_bot()
