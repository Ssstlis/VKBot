import vk
import time
import datetime
import platform
import os
import pyowm
import re
import requests
import random
from PIL import Image
from io import BytesIO
from bs4 import BeautifulSoup as bs

start2 = 'OS ' + platform.platform() + '\n' + 'CPU Arc' + platform.machine() + '\n' + 'CPU set' + platform.processor() + '\n' + 'Compiller' + platform.python_compiler() + '\n' + 'Python v.' + platform.python_version() + '\n'
owm = pyowm.OWM('75d3076d13f283022dc1c5e19b765db5', language='ru')
to = 0
app = '5679286'
dev = 'VKbot 0.1 by Ssstlis'
commands = []
res = []
log = 'vkbotlog' + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M') + '.log'
log_path = 'logs'
adr = 'https://www.google.ru'


def whatiscloudness(weather):
    if 0 <= weather.get_clouds() <= 10:
        return 'ясная'
    if 10 < weather.get_clouds() <= 30:
        return 'небольшая облачность'
    if 30 < weather.get_clouds() <= 70:
        return 'пасмурная'
    if 70 < weather.get_clouds() <= 100:
        return 'мрачная'


def issunny(weather):
    if str(weather.get_status()) == 'Sunny':
        return 'солнечная'
    if str(weather.get_status()) == 'Clouds':
        return 'облачная'


def pascale(weather):
    return str(round(weather.get_pressure()['press'] * 0.75))


def strtolist(s):
    a = []
    while s.find(',') > -1:
        a.append(s[:s.find(','):])
        s = s[s.find(',') + 1::]
    if len(s) > 0:
        a.append(s)
    return a


def mbody(s):
    s = s.lower()
    s = s.strip()
    return s


def send(to, id, msg):
    src = api.users.get(uid=user_id)[0]
    dts = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    dt = datetime.datetime.now().strftime('[%H:%M:%S]')
    msg = dt + '\t' + msg + '\t'

    if to > 0:
        api.messages.send(chat_id=str(to), message=msg)
    else:
        api.messages.send(user_id=id, message=msg)
    logs = 'id ' + str(src['uid']) + ' ' + src['first_name'] + ' ' + src['last_name'] + ' ' + dts + '\n\t>>>>' + msg
    print(logs)
    lf.write(logs + '\n')
    lf.flush()


def sendf(to, id, msg, f):
    src = api.users.get(uid=user_id)[0]
    dts = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    dt = datetime.datetime.now().strftime('[%H:%M:%S]')
    msg = '\t' + msg + '\t'

    if to > 0:
        api.messages.send(chat_id=str(to), message=msg, forward_messages=str(f))
    else:
        api.messages.send(user_id=id, message=msg, forward_messages=str(f))
    logs = 'id ' + str(src['uid']) + ' ' + src['first_name'] + ' ' + src['last_name'] + ' ' + dts + '\n\t>>>>' + msg
    print(logs)
    lf.write(logs + '\n')
    lf.flush()


def SearchGoogleImages(to, id, query, num):
    if num > 10:
        num = 10

    nm = num

    path = os.path.abspath(os.curdir)
    path = os.path.join(path, str(query))

    if not os.path.exists(path):
        os.makedirs(path)

    query = query.split()
    query = '+'.join(query)
    query = adr + '/search?q=' + query + '&newwindow=1&source=lnms&tbm=isch&tbs=isz:l'

    req = requests.get(query, headers={
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, Chrome/43.0.2357.134 Safari/537.36'})
    req.close()
    soup = bs(req.content, "html.parser")
    allphoto = ''
    images = soup.find_all('div', attrs={'class': re.compile("rg_meta")})
    number = 1
    for image in enumerate(images[:num]):
        for tag in image[1]:
            try:
                tag = tag[tag.find('ou"') + 5:tag.find('"ow') - 2:]
                data = requests.get(tag, headers={
                    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64)'})
                tagA = Image.open(BytesIO(data.content))
                imagePath = os.path.join(path, str(number) + '.' + tagA.format.lower())
                tagA.save(imagePath)
                urm = api.photos.getMessagesUploadServer()
                time.sleep(0.5)
                req = requests.post(urm['upload_url'], files={'photo': open(imagePath, "rb")})
                req.close()
                params = {'server': req.json()['server'], 'photo': req.json()['photo'], 'hash': req.json()['hash']}
                msgphoto = api.photos.saveMessagesPhoto(**params)
                msgphoto = msgphoto[0]['id'] + ','
                allphoto += msgphoto
                time.sleep(0.3)
            except:
                nm -= 1
                pass
        number += 1

    params = {'attachment': allphoto}
    if len(allphoto) < 0:
        msg = 'Ошибка поиска'
        if to > 0:
            api.messages.send(chat_id=to, message=msg)
        else:
            api.messages.send(user_id=id, message=msg)
    else:
        msg = str(nm) + ' фотографий'
        if to > 0:
            api.messages.send(chat_id=to, **params)
        else:
            api.messages.send(user_id=id, **params)

    dts = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
    src = api.users.get(uid=user_id)[0]
    logs = 'id ' + str(src['uid']) + ' ' + src['first_name'] + ' ' + src[
        'last_name'] + ' ' + dts + '\n\t>>>>' + msg
    print(logs)
    lf.write(logs + '\n')
    lf.flush()


def wind(weather):
    if 0 < weather.get_wind()['deg'] <= 22:
        return 'Северо-северо-восточный'
    if 23 <= weather.get_wind()['deg'] <= 44:
        return 'Северно-восточный'
    if 45 <= weather.get_wind()['deg'] <= 66:
        return 'Восточно-северо-восточный'
    if 67 <= weather.get_wind()['deg'] <= 90:
        return 'Восточный'
    if 91 <= weather.get_wind()['deg'] <= 112:
        return 'Восточно-юго-восточнй'
    if 113 <= weather.get_wind()['deg'] <= 134:
        return 'Юго-восточный'
    if 135 <= weather.get_wind()['deg'] <= 156:
        return 'Юго-юго-восточный'
    if 157 <= weather.get_wind()['deg'] <= 180:
        return 'Южный'
    if 181 <= weather.get_wind()['deg'] <= 202:
        return 'Юго-юго-западный'
    if 203 <= weather.get_wind()['deg'] <= 224:
        return 'Юго-западный'
    if 225 <= weather.get_wind()['deg'] <= 246:
        return 'Западно-юго-западный'
    if 247 <= weather.get_wind()['deg'] <= 270:
        return 'Западный'
    if 271 <= weather.get_wind()['deg'] <= 292:
        return 'Западно-северо-западный'
    if 293 <= weather.get_wind()['deg'] <= 314:
        return 'Северо-западный'
    if 315 <= weather.get_wind()['deg'] <= 336:
        return 'Северо-северо-западный'
    if 337 <= weather.get_wind()['deg'] <= 360:
        return 'Северный'


def getweather(wt):
    observation = owm.weather_at_place(wt)
    weather = observation.get_weather()
    location = observation.get_location()
    return 'Погода в городе ' + location.get_name() + ' (' + location.get_country() + ') на сегодня ' + str(
        weather.get_reference_time('iso'))[11:16] + ': ' + str(
        weather.get_detailed_status()) + ', облачность составляет ' + str(
        weather.get_clouds()) + '%, давление ' + pascale(weather) + ' мм рт.ст.,\n' + 'Температура ' + str(
        weather.get_temperature('celsius')['temp']) + ' градусов Цельсия ' + ', ночью ' + str(
        weather.get_temperature('celsius')['temp_min']) + ' днем ' + str(
        weather.get_temperature('celsius')['temp_max']) + ' градусов Цельсия,\n' + 'Ветер ' + wind(
        weather) + ', ' + str(weather.get_wind()['speed']) + ' м/с.'


if os.path.exists(log_path):
    os.chdir(os.getcwd() + '\\' + log_path)
else:
    os.mkdir(log_path)
    os.chdir(os.getcwd() + '\\' + log_path)

tok = open('token.txt', 'r')
token = tok.read()
tok.close()

tok = open('tasks.txt', 'r')
ln = tok.read()
lm = ''

for line in ln:
    if line != '\n':
        lm += line
    else:
        commands.append(lm)
        lm = ''
tok.close()

tok = open('results.txt', 'r')
ln = tok.read()
lm = ''

for line in ln:
    if line != '\n':
        lm += line
    else:
        res.append(lm)
        lm = ''
tok.close()

session = vk.Session(
    access_token=token)
api = vk.API(session)

lf = open(log, 'w')
lf.close()
lf = open(log, 'a')
start = '\n\t\t\tVKBot starting ' + datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]') + '\n'
print(start)
lf.write(start)
lf.write(start2)
print(start2)

while (True):
    try:
        while (True):
            user_id = ''
            dt = datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
            messages = api.messages.get(filters='1', count='200', preview_length='1')
            new_ln = len(messages)
            if new_ln > 1:
                logs = '\n\t\t' + dt + '\n\t\tНайдено ' + str(new_ln - 1) + ' новых сообщений.'
                print(logs)
                lf.write('\n' + logs + '\n')
                lf.flush()

            for m in messages[1:]:
                m['body'] = mbody(m['body'].replace('.', ''))

            am = [(m['uid'], m['mid'], m['body'])
                  for m in messages[1:] if m['body'] not in commands]

            new_am = len(am)
            if new_am > 0:
                logs = '\t\tИз них не содержат команд: ' + str(new_am) + ' сообщений.'
                print(logs)
                lf.write(logs + '\n')
                lf.flush()

            ids2 = ', '.join([str(m[1]) for m in am])

            try:
                if ids2:
                    api.messages.markAsRead(message_ids=ids2)
                    logs = '\t\t\tПомечено как прочитанные: ' + str(new_am) + ' сообщений.'
                    print(logs)
                    lf.write(logs + '\n')
                    lf.flush()
            except:
                logs = 'Возникли проблемы с пометкой сообщений....'
                print(logs)
                lf.write(logs + '\n')
                lf.flush()

            messages = [(m['uid'], m['mid'], m['body'])
                        for m in messages[1:] if m['body'] in commands]

            new_am = len(messages)
            if new_am > 0:
                logs = '\t\tСсодержат команд ' + str(new_am) + ' сообщений.'
                print(logs)
                lf.write(logs + '\n\n')
                lf.flush()

                try:
                    for m in messages:
                        user_id = m[0]
                        message_id = m[1]
                        comand = m[2]
                        to = 0
                        if api.messages.getById(message_ids=m[1])[1].get('chat_id'):
                            to = api.messages.getById(message_ids=m[1])[1].get('chat_id')

                        if comand == commands[0]:
                            send(to, user_id, ' ' + res[0])
                            continue

                        if comand == commands[1]:
                            wt = api.messages.getById(message_ids=m[1])[1].get('body')
                            wt = mbody(wt.replace('.', ''))
                            if wt.find(' ') > 1:
                                wt = wt[wt.find(' ') + 1::]
                                wt = wt.capitalize()
                                send(to, user_id, getweather(wt))
                                continue

                        if comand == commands[2]:
                            send(to, user_id, ' ' + res[2])
                            continue

                        if comand == commands[3]:
                            wt = api.messages.getById(message_ids=m[1])[1].get('body')
                            wt = mbody(wt.replace('.', ''))
                            if wt.find(' ') > 1:
                                wt = wt[wt.find(' ') + 1::]
                                wt = wt.capitalize()
                                SearchGoogleImages(to, user_id, wt, 3)
                                continue

                        if comand == commands[4]:
                            wt = strtolist(api.messages.getById(message_ids=m[1])[1].get('chat_active'))
                            wt = wt[random.randint(0, len(wt) - 1)]
                            sr = api.users.get(uid=wt)[0]
                            sendf(to, user_id, ' ' + res[4] + sr['first_name'] + ' ' + sr['last_name'], m[1])
                        print('\n')
                        time.sleep(1)
                except:
                    logs = 'Произошла ошибка при отправке сообщения для id %s' % user_id
                    print(logs)
                    lf.write(logs + '\n')
                    lf.flush()

            ids = ', '.join([str(m[1]) for m in messages])

            if ids:
                api.messages.markAsRead(message_ids=ids)
            time.sleep(1)
    except:
        logs = 'Непредвиденная ошибка в ' + datetime.datetime.now().strftime('[%Y-%m-%d %H:%M:%S]')
        print(logs)
        lf.write(logs + '\n')
        lf.flush()
        time.sleep(10)
