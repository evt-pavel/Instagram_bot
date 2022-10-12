from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from config import username, password, exceptions
from time import sleep
import random


browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()))


def authenticate():  # функция авторизации
    browser.get('https://www.instagram.com')
    sleep(random.randrange(5, 7))
    username_input = browser.find_element(By.NAME, 'username')
    username_input.clear()
    username_input.send_keys(username)
    sleep(3)
    password_input = browser.find_element(By.NAME, 'password')
    password_input.clear()
    password_input.send_keys(password)
    sleep(2)
    password_input.send_keys(Keys.ENTER)
    sleep(random.randrange(5, 7))


def write_to_file(url):  # функция для записи ссылок на аккаунты в файл accounts.txt
    browser.get(f'{url}liked_by/')
    sleep(random.randrange(6, 7))

    hrefs = browser.find_elements(By.TAG_NAME, 'a')
    hrefs = [item.get_attribute('href') + '\n' for item in hrefs if item.get_attribute('href') not in exceptions]
    hrefs = set(hrefs)
    amount_hrefs = len(hrefs)

    with open('accounts.txt', 'w', encoding='utf-8') as file:
        file.writelines(hrefs)
    return print(f'Получено {amount_hrefs} ссылок')


def liked_posts():  # ставим лайки фотографиям

    print('собираем картинки')
    account_images = browser.find_elements(By.TAG_NAME, 'a')
    account_images = [item.get_attribute('href') for item in account_images if '/p/' in
                      item.get_attribute('href')]
    count = 0
    for url in account_images:
        browser.get(url)
        sleep(random.randrange(7, 10))
        browser.find_element(By.XPATH, '/html/body/div[1]/div/div/div/div[1]/div/div/div/div[1]/div[1]/div[2]/section/main/div[1]/div[1]/article/div/div[2]/div/div[2]/section[1]/span[1]/button').click()
        count += 1
        sleep(random.randrange(3, 6))
        if count == 2:
            break


def number_of_publication():  # проверяем количество публикаций в аккаунте
    amount = browser.find_elements(By.TAG_NAME, 'header')
    for am in amount:
        li = am.find_elements(By.TAG_NAME, 'li')
        for l in li:
            if 'публикаций' in l.text.split() and int(l.text.split()[0]) >= 2:
                return True
        else:
            return False


def type_account():  # проверяем тип аккаунта
    type_acc = browser.find_elements(By.TAG_NAME, 'h2')
    for t in type_acc:
        print()
        if t.text == 'Это закрытый аккаунт':
            return True
    return False


def clock():  # задержка между открыванием публикаций с визуализацией
    x = random.randrange(90, 150)
    count = 0
    for i in range(x):
        count += 1
        if count <= 20:
            print(f'{x - i}', end=' ')
        else:
            count = 0
            print(x - i)
        sleep(1)


def follow_the_account(href): # открываем ссылку
    browser.get(href)

    try:
        sleep(random.randrange(5, 7))
        head = browser.find_element(By.TAG_NAME, 'header')
        button = head.find_elements(By.TAG_NAME, 'button')
        activity = False

        for b in button:
            if b.text == 'Подписаться':
                activity = True
                b.click()
                print('Подписано!')
                sleep(random.randrange(3, 6))
                break

        if activity:
            if type_account():
                print('Это закрытый аккаунт')
                clock()
            else:
                if number_of_publication():
                    liked_posts()
                    clock()
                else:
                    print('Аккаунт Пустой')
                    clock()
        else:
            print('Вы уже подписаны на этот аккаунт')
            sleep(random.randrange(3, 5))

    except Exception as ex:
        print(ex)


def reading_from_file(): # функция считывания ссылок из файла
    with open('accounts.txt', 'r') as file:
        accounts = file.readlines()

    while accounts != []:
        acc = accounts[0]
        follow_the_account(acc)
        accounts.remove(acc)

        with open('accounts.txt', 'w') as file_follow, open('to_unsubscribe.txt', 'a') as file_unfollow:
            file_follow.writelines(accounts)
            file_unfollow.write(acc)


authenticate()
write_to_file(url=input('Введите ссылку:\n'))
sleep(3)
reading_from_file()

browser.close()
print('Программа завершена')

