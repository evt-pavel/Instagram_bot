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
options.headless = False  # отключаем интерфейс браузера
options.add_argument(
    "user-agent=Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36")
options.add_argument("--disable-blink-features=AutomationControlled")  # отключение режима вебдрайвера
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
xpath_like_button = '''
/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/section/main/div[1]
/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button
'''
like_button_status = ''


def authenticate():  # функция авторизации
    print('Открываем Instagram.')
    browser.get('https://www.instagram.com')
    sleep(random.randrange(1, 3))
    os.system('clear')
    print('Открываем Instagram.')
    sleep(2)
    os.system('clear')
    print('Открываем Instagram..')
    sleep(2)
    os.system('clear')
    print('Открываем Instagram...')
    sleep(2)
    os.system('clear')
    print('Открываем Instagram... Готово')
    sleep(2)
    print('Входим в аккаунт.')
    username_input = browser.find_element(By.NAME, 'username')
    username_input.clear()
    username_input.send_keys(username)
    sleep(3)
    os.system('clear')
    print('Открываем Instagram... Готово')
    print('Входим в аккаунт..')
    sleep(3)
    password_input = browser.find_element(By.NAME, 'password')
    password_input.clear()
    password_input.send_keys(password)
    os.system('clear')
    print('Открываем Instagram... Готово')
    print('Входим в аккаунт...')
    sleep(2)
    password_input.send_keys(Keys.ENTER)
    os.system('clear')
    print('Открываем Instagram... Готово')
    print('Входим в аккаунт... Готово')
    sleep(random.randrange(5, 7))


def write_to_file(url):  # функция для записи ссылок на аккаунты в файл accounts.txt
    browser.get(f'{url}liked_by/')
    sleep(random.randrange(6, 7))

    hrefs = browser.find_elements(By.TAG_NAME, 'a')
    hrefs = [item.get_attribute('href') + '\n' for item in hrefs if item.get_attribute('href') not in exceptions]
    hrefs = set(hrefs)

    with open('accounts.txt', 'w', encoding='utf-8') as file:
        file.writelines(hrefs)

    return view()


def liked_posts():  # ставим лайки фотографиям
    like = 0
    global img_status, like_status
    img_status = 'Получаю изображения'
    view()
    account_images = browser.find_elements(By.TAG_NAME, 'a')
    account_images = [item.get_attribute('href') for item in account_images if '/p/' in
                      item.get_attribute('href')]
    img_status = 'Готово!'
    view()

    for url in account_images:
        browser.get(url)
        like += 1
        like_status = f'{like} из 2'
        view()
        sleep(random.randrange(7, 10))
        browser.find_element(By.XPATH, xpath_like_button).click()

        sleep(random.randrange(3, 6))
        if like == 2:
            break


def number_of_publication():  # проверяем количество публикаций в аккаунте
    amount = browser.find_elements(By.TAG_NAME, 'header')
    for am in amount:
        tag_li = am.find_elements(By.TAG_NAME, 'li')
        for li in tag_li:
            if 'публикаций' in li.text.split():
                if ',' in li.text.split()[0] or int(li.text.split()[0]) >= 2:
                    return True


def type_account():  # проверяем тип аккаунта
    type_acc = browser.find_elements(By.TAG_NAME, 'h2')
    for t in type_acc:
        if t.text == 'Это закрытый аккаунт':
            return True


def clock():  # задержка между открыванием публикаций с визуализацией
    x = random.randrange(90, 150)
    for i in range(x):
        view()
        print(f'До открытия следующего аккаунта осталось: {x - i} секунд')
        sleep(1)
        if x - i == 0:
            view()


def follow_the_account(href):  # открываем ссылку
    global account_name, count, follow, follower, errors, hrefs_errors, account_status, img_status, subscribe, \
        like_status
    account_status, img_status, account_name, like_status, subscribe = '', '', href.split('/')[3], '0 из 2', ''
    view()
    count += 1

    browser.get(href)
    try:
        sleep(random.randrange(5, 7))
        head = browser.find_element(By.TAG_NAME, 'header')
        button = head.find_elements(By.TAG_NAME, 'button')
        activity = False

        for b in button:
            if b.text == 'Подписаться':
                activity = True
                follow += 1
                b.click()
                subscribe = 'Оформлена!'
                view()
                sleep(random.randrange(3, 6))
                break

        if activity:
            if type_account():
                account_status = 'Закрытый.'
                img_status = 'Это закрытый аккаунт!'
                like_status = 'Это закрытый аккаунт!'
                view()
                clock()
            else:
                if number_of_publication():
                    account_status = 'Общедоступный.'
                    view()
                    liked_posts()
                    clock()
                else:
                    account_status = 'Пустой.'
                    img_status = 'Аккаунт пустой!'
                    like_status = 'Аккаунт пустой!'
                    view()
                    clock()
        else:
            follower += 1
            subscribe = 'Вы уже подписаны на этот аккаунт!'
            account_status = 'Вы уже подписаны на этот аккаунт!'
            img_status = 'Вы уже подписаны на этот аккаунт!'
            like_status = 'Вы уже подписаны на этот аккаунт!'
            view()
            sleep(random.randrange(3, 5))

    except Exception as ex:
        print(ex)
        errors += 1
        count += 1
        hrefs_errors.append(href)


def reading_from_file():  # функция считывания ссылок из файла
    with open('accounts.txt', 'r', encoding='utf-8') as file:
        accounts = file.readlines()

        global amount_hrefs
        amount_hrefs = len(accounts)
        view()

    while len(accounts) != 0:
        acc = accounts[0]
        follow_the_account(acc)
        accounts.remove(acc)

        with open('accounts.txt', 'w', encoding='utf-8') as file_follow,\
                open('to_unsubscribe.txt', 'a', encoding='utf-8') as file_unfollow:
            file_follow.writelines(accounts)
            file_unfollow.write(acc)


def view():
    os.system('clear')

    print(f'Осталось {amount_hrefs}/{amount_hrefs - count}')
    print('Всего подписок: ', follow)
    print('Пропущено аккаунтов: ', follower)
    print('Ошибок: ', errors)
    print()
    print('Название аккаунта', account_name)
    print('Подписка на аккаунт: ', subscribe)
    print('Статус аккаунта: ', account_status)
    print('Поучение фотографий: ', img_status)
    print(f'Открыто изображений: {like_status}')


authenticate()
write_to_file(url=input('Введите ссылку на публикацию: '))
sleep(3)
reading_from_file()

browser.close()
view()
print('Программа завершена!')
print('Список ошибок:')

with open('errors.txt', 'w', encoding='utf-8') as error:
    error.writelines(hrefs_errors)

for error in hrefs_errors:
    print(error)

input('Press ENTER to exit')
