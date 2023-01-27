import os
from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import username, password, exceptions
from time import sleep
import random

options = Options()
options.headless = False # отключаем интерфейс браузера
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")  # отключение режима веб драйвера
browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

follow = 0
follower = 0
count = 0
amount_hrefs = 0
errors = 0
hrefs_errors = []
account_name = ''
account_status = ''
img_status = ''
like_status = ''
subscribe = ''
xpath_like_button = '''/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]
/article/div/div[2]/div/div[2]/section[1]/span[1]/button'''
like_button_status = ''
process = ''


def authenticate():  # функция авторизации
    print('Открываем Instagram.')
    browser.get('https://www.instagram.com')
    os.system('clear')
    print('Открываем Instagram.')
    sleep(2)
    os.system('clear')
    print('Открываем Instagram..')
    sleep(2)
    os.system('clear')
    print('Открываем Instagram...')
    browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/section/main/article/div[2]/div[1]/div[2]/form/div/div[5]/button').click()
    sleep(8)
    os.system('clear')
    print('Открываем Instagram... Готово')
    sleep(2)
    print('Входим в аккаунт.')
    username_input = browser.find_element(By.NAME, 'email')
    username_input.clear()
    username_input.send_keys(username)
    sleep(1)
    os.system('clear')
    print('Открываем Instagram... Готово')
    print('Входим в аккаунт..')
    sleep(1)
    password_input = browser.find_element(By.NAME, 'pass')
    password_input.clear()
    password_input.send_keys(password)
    os.system('clear')
    print('Открываем Instagram... Готово')
    print('Входим в аккаунт...')
    sleep(1)
    password_input.send_keys(Keys.ENTER)
    os.system('clear')
    print('Открываем Instagram... Готово')
    print('Входим в аккаунт... Готово')
    sleep(random.randrange(15, 20))



def write_to_file(url):  # функция для записи ссылок на аккаунты в файл accounts.txt
    browser.get(f'{url}liked_by/')
    sleep(random.randrange(6, 7))
    # hrefs = browser.find_elements(By.TAG_NAME, 'a')
    # hrefs = [item.get_attribute('href') + '\n' for item in hrefs if item.get_attribute('href') not in exceptions]
    # hrefs = set(hrefs)
    # with open('accounts.txt', 'w', encoding='utf-8') as file:
    #     file.writelines(hrefs)
    # view()

    # собираем ссылки в список со скролом страницы
    for i in range(10):
        print(f'Итерация №{i}')
        hrefs = browser.find_elements(By.TAG_NAME, 'a')
        hrefs = [item.get_attribute('href') + '\n' for item in hrefs if item.get_attribute('href') not in exceptions]
        browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
        sleep(3)

    hrefs = set(hrefs)
    with open('accounts.txt', 'w', encoding='utf-8') as file:
        file.writelines(hrefs)
    view()

def liked_posts():  # ставим лайки фотографиям
    like = 0
    global process, like_status
    process = 'Проверяем наличие публикаций:'
    view()
    account_images = browser.find_elements(By.TAG_NAME, 'a')
    account_images = [item.get_attribute('href') for item in account_images if '/p/' in
                      item.get_attribute('href')]
    process = 'Проверяем наличие публикаций: Готово!'
    like_status = f'Открыто публикаций: {like} из 2'
    view()

    for url in account_images:
        browser.get(url)
        like += 1
        like_status = f'Открыто публикаций: {like} из 2'
        view()
        sleep(random.randrange(10, 15))
        browser.find_element(By.XPATH, xpath_like_button).click()
        sleep(random.randrange(3, 6))
        if like == 2:
            break


def number_of_publication():  # проверяем количество публикаций в аккаунте
    global img_status
    img_status = 'Проверяем наличие публикаций:'
    amount = browser.find_elements(By.TAG_NAME, 'header')
    for am in amount:
        tag_li = am.find_elements(By.TAG_NAME, 'li')
        for li in tag_li:
            if 'публикаций' in li.text.split():
                if ',' in li.text.split()[0] or int(li.text.split()[0]) >= 2:
                    img_status = 'Проверяем наличие публикаций: Готово!'
                    view()
                    return True
    img_status = 'Проверяем наличие публикаций: Аккаунт пустой!'
    view()


def type_account():  # проверяем тип аккаунта
    global account_status
    account_status = "Статус аккаунта:"
    type_acc = browser.find_elements(By.TAG_NAME, 'h2')
    for t in type_acc:
        if t.text == 'Это закрытый аккаунт':
            account_status = "Статус аккаунта: Это закрытый аккаунт!"
            view()
            return True
    account_status = "Статус аккаунта: Общедоступный аккаунт."
    view()


def clock():  # задержка между открыванием публикаций с визуализацией
    x = random.randrange(80, 110)
    y = ''
    for i in range(x):
        if len(y) == 51:
            y = ''
        y += '*'
        view()
        print(y)
        print(f'До открытия следующего аккаунта осталось: {x - i} секунд')
        sleep(1)
        if x - i == 0:
            view()


def subscribe_status(button):
    global subscribe, follow, follower
    subscribe = 'Статус подписки:'
    for b in button:
        if b.text == 'Подписаться':
            follow += 1
            b.click()
            subscribe = 'Статус подписки: Подписка оформлена!'
            view()
            return True
    subscribe = 'Статус аккаунта: Подписка уже была оформлена!'
    follower += 1
    view()


def follow_the_account(href):  # открываем ссылку
    global account_name, count, errors

    account_name = f"Открываем аккаунт: {href.split('/')[3]}"
    view()
    count += 1

    browser.get(href)
    try:
        sleep(random.randrange(7, 10))
        head = browser.find_element(By.TAG_NAME, 'header')
        button = head.find_elements(By.TAG_NAME, 'button')

        if subscribe_status(button):
            if type_account():
                clock()
            else:
                if number_of_publication():
                    liked_posts()
                    clock()
                else:
                    clock()
        else:
            sleep(random.randrange(3, 5))

    except Exception as ex:

        with open('errors.txt', 'a', encoding='utf-8') as error:
            error.write(href)
            error.write(str(ex))
            error.write('')
        errors += 1


def reading_from_file():  # функция считывания ссылок из файла
    with open('accounts.txt', 'r', encoding='utf-8') as file:
        accounts = file.readlines()

        global amount_hrefs
        amount_hrefs = len(accounts)
        view()

    while follow != 50: #len(accounts) != 0:
        acc = accounts[0]

        global account_name, subscribe, account_status, img_status, like_status, process
        account_status, subscribe, account_status, img_status, like_status, process = '', '', '', '', '', ''

        follow_the_account(acc)
        accounts.remove(acc)

        with open('accounts.txt', 'w', encoding='utf-8') as file_follow,\
                open('to_unsubscribe.txt', 'a', encoding='utf-8') as file_unfollow:
            file_follow.writelines(accounts)
            file_unfollow.write(acc)


def unsubscribe():
    with open('to_unsubscribe.txt', 'r', encoding='utf-8') as file:
        accounts = file.readlines()

        global amount_hrefs
        amount_hrefs = len(accounts)

        for acc in accounts:

            browser.get(acc)
            sleep(random.randrange(10))
            button = browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]'
                                           '/section/main/div/header/section/div[1]/div[1]/div/div[1]/button')

            print(button.text)

            if button.text == 'Подписки':
                button.click()
                sleep(random.randrange(3, 7))
                browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div/div[7]/div/div/div/div/div/div').click()
            elif button.text == 'Запрос отправлен':
                button.click()
                sleep(random.randrange(3, 7))
                browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]'
                                                    '/div/div/div/div/div[2]/div/div/div/div[7]').click()
            else:
                print('continue')

            sleep(15)







            sleep(5)
            # browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div'
            #                                '/div/div[2]/div/div/div/div[7]/div/div/div/div/div').click()


            # browser.find_element(By.XPATH, '/html/body/div[2]/div/div/div/div[2]/div/div/div[1]/div/div[2]/div/div/div/'
            #                                'div/div[2]/div/div/div[3]/button[1]').click()
            sleep(10)








def view():
    os.system('clear')

    print(f'Осталось: {amount_hrefs - count} из {amount_hrefs}')
    print('Всего подписок: ', follow)
    print('Пропущено аккаунтов: ', follower)
    print('Ошибок: ', errors)
    print()
    print(account_name)
    print(subscribe)
    print(account_status)
    print(img_status)
    print(like_status)

#
# authenticate()
#
# if input('Нужно добавлять ссылки? ') == '+':
#     write_to_file(url=input('Введите ссылку на публикацию: '))
#     sleep(3)
#     reading_from_file()
# else:
#     reading_from_file()
#
# browser.close()
# view()
# print('Программа завершена!')
# input('Press ENTER to exit')

authenticate()
unsubscribe()

