import os
from selenium.webdriver import Chrome, ChromeOptions
from selenium import webdriver
import time
import pandas as pd

# Chromeを起動する関数


def set_driver(driver_path, headless_flg):
    # Chromeドライバーの読み込み
    options = ChromeOptions()

    # ヘッドレスモード（画面非表示モード）をの設定
    if headless_flg == True:
        options.add_argument('--headless')

    # 起動オプションの設定
    options.add_argument(
        '--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36')
    # options.add_argument('log-level=3')
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--ignore-ssl-errors')
    options.add_argument('--incognito')          # シークレットモードの設定を付与

    # ChromeのWebDriverオブジェクトを作成する。
    return Chrome(executable_path=os.getcwd() + "/" + driver_path, options=options)

# main処理


def main():
    search_keyword = str(input('検索したいキーワードは何ですか？>>'))
    # driverを起動
    driver = webdriver.Chrome('./chromedriver.exe')
    """
    if os.name == 'nt': #Windows
        driver = set_driver("chromedriver.exe", False)
    elif os.name == 'posix': #Mac
        driver = set_driver("chromedriver", False)
    """
    # Webサイトを開く
    
    driver.get("https://tenshoku.mynavi.jp/")
    time.sleep(5)
 
    try:
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
        time.sleep(5)
        # ポップアップを閉じる
        driver.execute_script('document.querySelector(".karte-close").click()')
    except:
        pass
    
    # 検索窓に入力
    driver.find_element_by_class_name(
        "topSearch__text").send_keys(search_keyword)
    # 検索ボタンクリック
    driver.find_element_by_class_name("topSearch__button").click()

    output_list = []
    flag_page = False
    cnt_page = 1
    print(str(cnt_page) + "ページ目")

    while flag_page == False:

        try:
            # 検索結果の一番上の会社のコピーを取得
            th_list = driver.find_elements_by_class_name("tableCondition__head")
            td_list = driver.find_elements_by_class_name("tableCondition__body")

            # 1ページ分繰り返し
            for i in range(len(th_list)):
                if th_list[i - 1].text == "初年度年収" or th_list[i - 1].text == "仕事内容" or th_list[i - 1].text == "対象となる方":
                    output = th_list[i - 1].text + ',' + td_list[i - 1].text
                    output2 = output.split(',')
                    print(output2)
                    output_list.append(output2)
            
            # 次ページ移動
            find_href = driver.find_elements_by_class_name("iconFont--arrowLeft")
            if len(find_href) == 0:
                flag_page = True
            else:
                my_href = find_href[len(find_href) - 1] # class_name("iconFont--arrowLeft")が二箇所あるため、先頭のものURLを取得
                driver.get(my_href.get_attribute("href"))
                cnt_page += 1
                print(str(cnt_page) + "ページ目") 
        
        except:

          pass

    pd.DataFrame(output_list).to_csv("kekka.csv", index=False, header=False)
    

# 直接起動された場合はmain()を起動(モジュールとして呼び出された場合は起動しないようにするため)
if __name__ == "__main__":
    main()
