import requests
import config
import telebot
from bs4 import BeautifulSoup
import datetime

bot = telebot.TeleBot(config.access_token)
today = datetime.datetime.now()

days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
dni = ['<b>Понедельник:</b>\n', '<b>Вторник:</b>\n', '<b>Среда:</b>\n', '<b>Четверг:</b>\n',
       '<b>Пятница:</b>\n', '<b>Суббота:</b>\n', '<b>Воскресенье:</b>\n']


def get_page(group, week=''):
    if week:
        week = str(week) + '/'
    url = '{domain}/{group}/{week}raspisanie_zanyatiy_{group}.htm'.format(
        domain=config.domain,
        week=week,
        group=group)
    response = requests.get(url)
    web_page = response.text
    return web_page


def parse_schedule_for_a_monday(web_page, day=''):
    soup = BeautifulSoup(web_page, "html5lib")

    # Получаем таблицу с расписанием на понедельник
    schedule_table = soup.find("table", attrs={"id": day})

    # Время проведения занятий
    try:
        times_list = schedule_table.find_all("td", attrs={"class": "time"})
        times_list = [time.span.text for time in times_list]
    except AttributeError:
        raise AttributeError

    # Место проведения занятий
    locations_list = schedule_table.find_all("td", attrs={"class": "room"})
    locations_list = [room.span.text for room in locations_list]

    # Название дисциплин и имена преподавателей
    lessons_list = schedule_table.find_all("td", attrs={"class": "lesson"})
    lessons_list = [lesson.text.split('\n\n') for lesson in lessons_list]
    lessons_list = [', '.join([info for info in lesson_info if info]) for lesson_info in lessons_list]

    return times_list, locations_list, lessons_list


@bot.message_handler(commands=['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'])
def get_schedule(message):
    """ Получить расписание на указанный день """

    days = ['/monday', '/tuesday', '/wednesday', '/thursday', '/friday', '/saturday', '/sunday']
    try:
        w_day, week, group = message.text.split()
        if len(group) != 5:
            bot.send_message(message.chat.id, 'Нет такой группы !', parse_mode='HTML')
            return None
        web_page = get_page(group, week)
        day = str(days.index(w_day) + 1) + 'day'
    except Exception:
        resp = '<b>Наверное, ты что-то не так ввёл :(</b>'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        return None
    try:
        times_lst, locations_lst, lessons_lst = \
         parse_schedule_for_a_monday(web_page, day)
        resp = ''
        for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
            resp += '<b>{}</b>, {}, {}'.format(time, location, lesson)
        bot.send_message(message.chat.id, resp, parse_mode='HTML')
        return times_lst, locations_lst, lessons_lst
    except AttributeError:
        resp = '<b>В этот день пар нет! Ты свободен!!</b>'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


@bot.message_handler(commands=['near'])
def get_near_lesson(message):
    """ Получить ближайшее занятие """
    global today
    _, group = message.text.split()
    w_day = today.weekday() + 1
    if len(group) != 5:
        bot.send_message(message.chat.id, 'Нет такой группы !', parse_mode='HTML')
        return None
    week = 1
    if int(today.strftime('%W')) % 2 == 1:
        week = 2
    web_page = get_page(group, str(week))
    try:
        schedule = parse_schedule_for_a_monday(web_page, str(w_day) + 'day')
        times_lst, locations_lst, lessons_lst = schedule
        for i in times_lst:
            time, _ = i.split('-')
            h, m = time.split(':')
            cur_h, cur_m = int(datetime.datetime.now().hour), int(datetime.datetime.now().minute)
            if cur_h - h <= 0:
                resp = '<b>Твои ближайщие пары:</b> \n'
                resp += ' <b>{}</b>, {}, {}\n'.format(i, locations_lst[times_lst.index(i)], lessons_lst[times_lst.index(i)])
                bot.send_message(message.chat.id, resp, parse_mode='HTML')
                break
    except Exception:
        bot.send_message(message.chat.id, 'На сегодня ты свободен, но скоро наступит:', parse_mode='HTML')
        for _ in range(3):
            try:
                w_day += 1
                if w_day == 6:
                    w_day = 1
                times_lst, locations_lst, lessons_lst = parse_schedule_for_a_monday(web_page, str(w_day) + 'day')
                bot.send_message(message.chat.id, str(dni[w_day - 1]), parse_mode='HTML')
                for i in times_lst:
                    resp = '<b>{}</b>, {}, {}\n'.format(i, locations_lst[times_lst.index(i)], lessons_lst[times_lst.index(i)])
                    bot.send_message(message.chat.id, resp, parse_mode='HTML')
                break
            except:
                pass


@bot.message_handler(commands=['tomorrow'])
def get_tomorrow(message):
    """ Получить расписание на следующий день """

    _, group = message.text.split()
    tomorrow = int(today.weekday()) + 2
    week = 1
    if int(today.strftime('%W')) % 2 == 1:
        week = 2
    web_page = get_page(group, str(week))
    i = 1
    if len(group) != 5:
        bot.send_message(message.chat.id, 'Нет такой группы !', parse_mode='HTML')
        return None
    while i:
        if tomorrow == 6 and week == 1:
            week = 2
        elif tomorrow == 6 and week == 2:
            week = 1

        day = str(tomorrow) + 'day'
        try:
            times_lst, locations_lst, lessons_lst = \
                parse_schedule_for_a_monday(web_page, day)
            resp = '<b>Твое расписание на завтра:</b> \n'
            for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}'.format(time, location, lesson)
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            i = 0
        except AttributeError:
            resp = '<b>Завтра пар нет! Но, вероятно, они будут послезавтра!!</b>'
            bot.send_message(message.chat.id, resp, parse_mode='HTML')
            tomorrow += 1


@bot.message_handler(commands=['all'])
def get_all_schedule(message):
    """ Получить расписание на всю неделю для указанной группы """

    _, week, group = message.text.split()
    web_page = get_page(group, week)
    for i in range(6):
        day = str(i+1) + 'day'
        resp = str(dni[i])
        try:
            times_lst, locations_lst, lessons_lst = \
                parse_schedule_for_a_monday(web_page, day)
            for time, location, lesson in zip(times_lst, locations_lst, lessons_lst):
                resp += '<b>{}</b>, {}, {}'.format(time, location, lesson)
        except AttributeError:
            resp += '<b>В этот день пар нет!</b>'
        bot.send_message(message.chat.id, resp, parse_mode='HTML')


if __name__ == '__main__':
    bot.polling(none_stop=True)

