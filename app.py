from bs4 import BeautifulSoup
import time
import selenium.webdriver.common.by
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from config import email, password, API_TOKEN, per_sec_refresh, my_id, id_father
import telebot
import pickle



bot = telebot.TeleBot(API_TOKEN)
bot.send_message(id_father, "Бот начал работу!")
bot.send_message(my_id, "Бот начал работу!")
cnt = 1
s = Service('/chromedriver.exe')
driver = webdriver.Chrome(service=s)
driver.get('https://portal.xn----8sbavmdilly8a9gpb.xn--p1ai/sign-in')
driver.find_element(value='inputEmail', by='id').send_keys(email)
driver.find_element(value='inputPassword', by='id').send_keys(password)
driver.find_element(value='sb_enter', by='name').click()
driver.get('https://portal.xn----8sbavmdilly8a9gpb.xn--p1ai/account/signal/common')
driver.find_element(selenium.webdriver.common.by.By.XPATH,
                    "//*[contains(text(), 'Мосбиржа')]").click()
last = driver.page_source.split('table_signal_1')[1]
with open("test", "rb") as fp:  # Unpickling
    last_list = pickle.load(fp)
while (True):
    try:
        if cnt % 25 == 0:
            bot.send_message(id_father, "Бот перезагружен!")
            bot.send_message(my_id, "Бот перезагружен!")
            driver.close()
            driver = webdriver.Chrome(service=s)
            driver.get('https://portal.xn----8sbavmdilly8a9gpb.xn--p1ai/sign-in')
            driver.find_element(value='inputEmail', by='id').send_keys(email)
            driver.find_element(value='inputPassword', by='id').send_keys(password)
            driver.find_element(value='sb_enter', by='name').click()
            driver.get('https://portal.xn----8sbavmdilly8a9gpb.xn--p1ai/account/signal/common')
            driver.find_element(selenium.webdriver.common.by.By.XPATH,
                                "//*[contains(text(), 'Мосбиржа')]").click()
        driver.refresh()
        driver.find_element(selenium.webdriver.common.by.By.XPATH,
                            "//*[contains(text(), 'Мосбиржа')]").click()
        new = driver.page_source.split('table_signal_1')[1]
        if last != new:
            check = last.split('</table>')[0].split('<tr>')[2:]
            current = []
            for i in range(len(check)):
                t = BeautifulSoup(check[i])
                hide_mobile_signal = t.find_all('div', class_='hide_mobile_signal')[0].text
                tg_signal_id = t.find_all('td', class_='tg_signal_id')[0].text
                tg_signal_tiker = t.find_all('td', class_='tg_signal_tiker')[0].text
                tg_signal_status = t.find_all('td', class_='tg_signal_status')[0].text.strip()
                tg_signal_diraction = t.find_all('td', class_='tg_signal_diraction')[0].text
                tg_signal_date_open = t.find_all('td', class_='tg_signal_date_open')[0].text
                tg_signal_price_open = t.find_all('td', class_='tg_signal_price_open')[0].text
                tg_signal_stop_loss_1 = t.find_all('td', class_='tg_signal_stop_loss')[0].text
                tg_signal_stop_loss_2 = t.find_all('td', class_='tg_signal_stop_loss')[1].text
                tg_signal_take_profit_1 = t.find_all('td', class_='tg_signal_take_profit')[0].text
                tg_signal_take_profit_2 = t.find_all('td', class_='tg_signal_take_profit')[1].text
                tg_signal_take_profit_3 = t.find_all('td', class_='tg_signal_take_profit')[2].text
                tg_signal_take_profit_4 = t.find_all('td', class_='tg_signal_take_profit')[3].text
                tg_signal_take_profit_5 = t.find_all('td', class_='tg_signal_take_profit')[4].text
                tg_signal_date_close = t.find_all('td', class_='tg_signal_date_close')[0].text
                tg_signal_price_close = t.find_all('td', class_='tg_signal_price_close')[0].text
                tg_signal_d1 = t.find_all('td', class_='tg_signal_d1')[0].text
                tg_signal_d2 = t.find_all('td', class_='tg_signal_d2')[0].text
                itog = {'ID: ': tg_signal_id,
                        'Инструмент: ': tg_signal_tiker,
                        'Статус: ': tg_signal_status, 'Направление: ': tg_signal_diraction,
                        'Дата входа: ': tg_signal_date_open,
                        'Цена входа: ': tg_signal_price_open,
                        'Стоп базовый: ': tg_signal_stop_loss_1,
                        'Стоп текущий: ': tg_signal_stop_loss_2,
                        'Тейк 1: ': tg_signal_take_profit_1,
                        'Тейк 2: ': tg_signal_take_profit_2, 'Тейк 3: ': tg_signal_take_profit_3,
                        'R расчетный: ': tg_signal_take_profit_4,
                        'Дата закрытия: ': tg_signal_date_close,
                        'Цена закрытия: ': tg_signal_price_close,
                        'R факт: ': tg_signal_take_profit_5,
                        'Доходность, 1% риска: ': tg_signal_d1,
                        'Доходность, 2% риска: ': tg_signal_d2}
                current.append(itog)
                flag = 0
                if itog['ID: '] == '1628':
                    pass
                for j in range(len(last_list)):
                    if last_list[j]['ID: '] == itog['ID: ']:
                        if last_list[j] != itog:
                            res = 'ИЗМЕНЕНИЯ:\n'
                            for k in last_list[j]:
                                if last_list[j][k] != itog[k]:
                                    res += k + itog[k] + ' (' + last_list[j][k] + ')\n'
                                else:
                                    res += k + last_list[j][k] + '\n'
                            bot.send_message(id_father, res)
                            bot.send_message(my_id, res)
                            last_list[j] = itog
                            flag = 1
                            break
                        else:
                            flag = 2
                if flag == 0:
                    last_list.append(itog)
                    res = 'НОВОЕ:\n'
                    for j in itog:
                        res += j + itog[j] + '\n'
                    bot.send_message(id_father, res)
                    bot.send_message(my_id, res)

            i = 0
            while i < len(last_list):
                if last_list[i] not in current:
                    del last_list[i]
                else:
                    i += 1
            with open("test", "wb") as fp:  # Pickling
                pickle.dump(last_list, fp)

        last = new
        time.sleep(per_sec_refresh)
        cnt += 1
        bot.send_message(my_id, f"Обновлено! Счетчик: {cnt}")
    except:
        cnt = 25
        bot.send_message(my_id, f"ОШИБКА! Ожидаю решения")
        time.sleep(per_sec_refresh)
