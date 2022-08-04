from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import undetected_chromedriver as uc
from time import sleep
from loguru import logger
from os import path, getcwd
from web3.auto import w3


def create_wallet():
    account = w3.eth.account.create()
    privatekey = str(account.privateKey.hex())
    address = str(account.address)
    return (address, privatekey)


def main():
    for _ in range(100):
        while emails:
            mail = emails.pop()
            wallet_data = create_wallet()
            co = uc.ChromeOptions()
            co.add_argument('--disable-gpu')
            co.add_argument(f'--load-extension={anticaptcha}')
            co.add_experimental_option('prefs', {'intl.accept_languages': 'en,en_US'})
            co.page_load_strategy = 'eager'
            driver = uc.Chrome(options=co)
            wait = WebDriverWait(driver, 100)

            driver.get(url)

            wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[1]/div[3]/input[1]'))).send_keys(
                'WAGMI')  # access code
            driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/input[2]').send_keys(mail)  # mail
            driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/input[3]').send_keys(wallet_data[0])  # wallet

            for c in range(30):
                try:
                    wait.until(lambda x: x.find_element(By.CSS_SELECTOR, '.antigate_solver.solved'))
                    logger.info('капча решена')
                    break
                except:
                    logger.error('ошибка при решении капчи')

            for b in range(5):
                try:
                    logger.info('кнопка')
                    driver.find_element(By.XPATH, '/html/body/div[1]/div[3]/button').click()  # confirm button
                    sleep(1)
                except:
                    break


            sleep(1)
            with open('bubble_data.txt', 'a') as file:
                file.write(wallet_data[0] + ':' + wallet_data[1] + ':' + mail + '\n')
            driver.quit()


if __name__ == '__main__':
    anticaptcha = path.join(getcwd(), "anticaptcha")
    url = 'https://lensformintakewl.bubbleapps.io/'
    with open('emails.txt', encoding='utf-8') as file:
        emails = [row.strip() for row in file]
        main()
