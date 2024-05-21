import time

from selenium import webdriver


def main():
    print('start')

    # ChromeOptionsの設定
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # ヘッドレスモードで実行
    options.add_argument('--no-sandbox')
    options.add_argument('--disable-dev-shm-usage')
    options.add_argument('--disable-gpu')
    options.add_argument('--window-size=1920,1080')

    driver = webdriver.Remote(
        command_executor='http://selenium:4444/wd/hub', options=options
    )

    driver.implicitly_wait(10)

    url = 'https://datascience-beginer.com/'  # テストでアクセスするURLを指定
    driver.get(url)

    time.sleep(3)
    driver.save_screenshot('test.png')  # アクセスした先でスクリーンショットを取得
    driver.quit()


if __name__ == '__main__':
    main()
