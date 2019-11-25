import time
import telebot
import datetime
import requests
from bs4 import BeautifulSoup
from telebot import apihelper
import config

bot = telebot.TeleBot(config.access_token)

apihelper.proxy = config.proxy

WEEKDAYS = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
WEEKDAYS_RUSSIAN = {'monday': 'понедельник',
                    'tuesday': 'вторник',
                    'wednesday': 'среду',
                    'thursday': 'четверг',
                    'friday': 'пятницу',
                    'saturday': 'субботу',
                    'sunday': 'воскресенье'}
WEEK_PARITY = {0: 'четная неделя', 1: 'нечетная неделя', 3: ''}
EMOJI_NUMBERS = [u'\u0031\u20E3', u'\u0032\u20E3', u'\u0033\u20E3', u'\u0034\u20E3', u'\u0035\u20E3',
                 u'\u0036\u20E3', u'\u0037\u20E3', u'\u0038\u20E3', u'\u0039\u20E3']
CACHED_SCHEDULE = {}


def get_week_number():
    return datetime.date.today().isocalendar()[1] - 35


def get_day_number():
    return datetime.date.today().weekday() + 1


def parse_command(message):
    try:
        day, group = message.text.split()
        day = day[1:]
    except ValueError:
        bot.send_message(message.chat.id, 'You should specify your group number like "/monday K3141"')
        return
    return day, group


def get_schedule_page(group, week: str = None):
    if week is None or week == '0':
        week = ''
    else:
        week = week + '/'

    url = f'http://www.ifmo.ru/ru/schedule/0/K3141/raspisanie_zanyatiy_K3141.htm'
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_day(web_page, day_number: str):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": f"{day_number}day"})

    if schedule_table is None:
        return None

    times_list = schedule_table.find_all("td", attrs={"class": "time"})
    times_list = [time.span.text for time in times_list]

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([
        info.replace('\r\n', '(', 1).replace('\r\n', ') ', 1).replace('\t', '').replace('\n', '') for info in
        lesson_info if info
    ]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


def get_schedule_info(group: str, day: str, week: str = None):
    global CACHED_SCHEDULE
    if week is None:
        week_key = 0
    elif week == '0':
        week_key = 0
    elif week == '1':
        week_key = 1
    elif week == '2':
        week_key = 2
    elif int(week) % 2 == 0:
        week_key = 1
    else:
        week_key = 2

    if CACHED_SCHEDULE.get(group) is None:
        CACHED_SCHEDULE[group] = {}

    if CACHED_SCHEDULE[group].get(week_key) is None:
        CACHED_SCHEDULE[group][week_key] = {}

    if CACHED_SCHEDULE[group][week_key].get(day) is None:
        # print('Loading web-page with schedule...')
        web_page = get_schedule_page(group, week)
        schedule = parse_schedule_for_day(web_page, day)

        if schedule is None:
            CACHED_SCHEDULE[group][week_key][day] = [[], [], []]
            return None
        else:
            CACHED_SCHEDULE[group][week_key][day] = schedule
            return schedule
    else:
        # print('Loading schedule from cache...')
        schedule = CACHED_SCHEDULE[group][week_key][day]
        if len(schedule[0]) == 0:
            return None
        return schedule


@bot.message_handler(commands=WEEKDAYS)
def get_schedule(message, week_number: str = None, return_reply=False, consider_week_parity=True):
    """ Получить расписание на указанный день """
    try:
        day, week_number, group = message.text.split()
        day = day[1:]
    except ValueError:
        _cmd = parse_command(message)
        if _cmd is None:
            return
        else:
            day, group = _cmd

    weekday_number = str(WEEKDAYS.index(day) + 1)
    if consider_week_parity:
        schedule = get_schedule_info(group, weekday_number, week_number)
    else:
        schedule = get_schedule_info(group, weekday_number)

    if schedule is None:
        resp = 'На указанный день пар нет. Можно отдыхать :)'
        if return_reply:
            return resp
        else:
            bot.send_message(message.chat.id, resp)
            return

    times_list, locations_list, lessons_list = schedule

    resp = f'Расписание на {WEEKDAYS_RUSSIAN[day]}:\n'
    for i in range(len(times_list)):
        resp += f'{EMOJI_NUMBERS[i]} {times_list[i]} | {lessons_list[i]} | {locations_list[i]}\n'

    if return_reply:
        return resp
    bot.send_message(message.chat.id, resp)


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    _cmd = parse_command(message)
    if _cmd is None:
        return
    else:
        day, group = _cmd

    weekday_number = get_day_number()
    week_number = get_week_number()

    found = False
    this_day = True
    while not found:
        schedule = get_schedule_info(group, str(weekday_number), str(weekday_number))
        if schedule is not None:
            times_list, locations_list, lessons_list = schedule
            if this_day:
                time_now = time.strptime(time.strftime('%H:%M'), '%H:%M')
                for i in range(len(times_list)):
                    lesson_start_time = time.strptime(times_list[0].split('-')[i], '%H:%M')
                    if time_now < lesson_start_time:
                        bot.send_message(message.chat.id, f'Ближайшая пара сегодня, в {times_list[i]}\n'
                                                          f'{lessons_list[i]}\n'
                                                          f'Корпус: {locations_list[i]}\n')
                        found = True
                        break
            else:
                if len(times_list) != 0:
                    if weekday_number <= get_day_number():
                        weekday_number += 7
                    bot.send_message(message.chat.id, f'Ближайшая пара через {weekday_number - get_day_number()} дня в '
                                                      f'{WEEKDAYS_RUSSIAN[WEEKDAYS[weekday_number % 7 - 1]]}, {times_list[0]}\n'
                                                      f'{lessons_list[0]}\n'
                                                      f'Корпус: {locations_list[0]}\n')
                    found = True
        else:
            this_day = False
            weekday_number += 1
            if weekday_number == 8:
                weekday_number = 1
                week_number += 1


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """
    _cmd = parse_command(message)
    if _cmd is None:
        return
    else:
        _, group = _cmd

    day = get_day_number() + 1
    week = get_week_number()
    if day == 7:
        day = 1
        week += 1

    message.text = f'/{WEEKDAYS[day - 1]} {group}'
    get_schedule(message, str(week))


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """
    _cmd = parse_command(message)
    if _cmd is None:
        return
    else:
        _, group = _cmd

    all_response = []
    for day in range(1, 8):
        resp = ''
        message.text = f'/{WEEKDAYS[day - 1]} {group}'
        schedule_for_day = get_schedule(message, return_reply=True, consider_week_parity=False)
        if 'пар нет' in schedule_for_day:
            resp += f'Расписание на {WEEKDAYS_RUSSIAN[WEEKDAYS[day - 1]]}:\n' \
                    f'Нет пар'
        else:
            resp += schedule_for_day
        all_response.append(resp.strip())

    bot.send_message(message.chat.id, f'\n{"=" * 30}\n'.join(all_response))


if __name__ == '__main__':
    bot.polling(none_stop=True)
