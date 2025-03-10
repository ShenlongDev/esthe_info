import time
import math
import csv
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
import os

# Construct the full path to the file
downloads_folder = os.path.join(os.path.expanduser('~'), 'Downloads')

neiru_path = os.path.join(f"{downloads_folder}/csvs", 'neiru_output.csv')
matuge_path = os.path.join(f"{downloads_folder}/csvs", 'matuge_output.csv')
relax_path = os.path.join(f"{downloads_folder}/csvs", 'relax_output.csv')
esthe_path = os.path.join(f"{downloads_folder}/csvs", 'esthe_output.csv')

neiru_c_path = os.path.join(downloads_folder, 'neiru_kanryou.csv')
matuge_c_path = os.path.join(downloads_folder, 'matuge_kanryou.csv')
relax_c_path = os.path.join(downloads_folder, 'relax_kanryou.csv')
esthe_c_path = os.path.join(downloads_folder, 'esthe_kanryou.csv')

# Mapping of prefecture numbers to names
PREFECTURES = {
    1: "北海道", 2: "青森県", 3: "岩手県", 4: "宮城県", 5: "秋田県", 6: "山形県", 7: "福島県",
    8: "茨城県", 9: "栃木県", 10: "群馬県", 11: "埼玉県", 12: "千葉県", 13: "東京都", 14: "神奈川県",
    15: "新潟県", 16: "富山県", 17: "石川県", 18: "福井県", 19: "山梨県", 20: "長野県", 21: "岐阜県",
    22: "静岡県", 23: "愛知県", 24: "三重県", 25: "滋賀県", 26: "京都府", 27: "大阪府", 28: "兵庫県",
    29: "奈良県", 30: "和歌山県", 31: "鳥取県", 32: "島根県", 33: "岡山県", 34: "広島県", 35: "山口県",
    36: "徳島県", 37: "香川県", 38: "愛媛県", 39: "高知県", 40: "福岡県", 41: "佐賀県", 42: "長崎県",
    43: "熊本県", 44: "大分県", 45: "宮崎県", 46: "鹿児島県", 47: "沖縄県"
}

# Mapping the kind of esthe
ESTHES = {
    1: neiru_path, 2: matuge_path, 3: relax_path, 4: esthe_path
}
KANRYOUESTHES = {
    1: neiru_c_path, 2: matuge_c_path, 3: relax_c_path, 4: esthe_c_path
}


def get_shop_urls():
    
    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.maximize_window()
    
    for i in range(1, 48):
        # pref_url = f"https://beauty.hotpepper.jp/g-nail/pre{str(i).zfill(2)}/"
        # pref_url = f"https://beauty.hotpepper.jp/g-eyelash/pre{str(i).zfill(2)}/"
        # pref_url = f"https://beauty.hotpepper.jp/relax/pre{str(i).zfill(2)}/"
        pref_url = f"https://beauty.hotpepper.jp/esthe/pre{str(i).zfill(2)}/"
        
        driver.get(pref_url)
        time.sleep(5)
        
        res_num_text = driver.find_element(By.CSS_SELECTOR, "span.numberOfResult").text
        res_num = int(res_num_text.replace(",", ""))
        page_num = math.ceil(res_num / 20)
        
        for j in range(1, page_num + 1):
            # driver.get(f"https://beauty.hotpepper.jp/g-nail/pre{str(i).zfill(2)}/PN{j}")
            # driver.get(f"https://beauty.hotpepper.jp/g-eyelash/pre{str(i).zfill(2)}/PN{j}")
            # driver.get(f"https://beauty.hotpepper.jp/relax/pre{str(i).zfill(2)}/PN{j}")
            driver.get(f"https://beauty.hotpepper.jp/esthe/pre{str(i).zfill(2)}/PN{j}")
            
            url_lis = driver.find_elements(By.CSS_SELECTOR, "li.searchListCassette")
            
            for li in url_lis:
                try:
                    shop_url = li.find_element(By.TAG_NAME, "a").get_attribute("href")
                    print(shop_url)

                    data = {
                        "エステ種別": "エステ",
                        "都道府県": PREFECTURES[i],
                        "URL": shop_url,
                        "店舗名": "",
                        "店舗住所": "",
                        "店舗電話番号": "",
                        "スタッフの人数": "",
                        "席数": "",
                        "有料か無料か": "",
                        "クーポンメニューの項目があるかどうか": "",
                    }

                    # Save to CSV
                    out = pd.DataFrame([data])
                    out.to_csv(esthe_path, mode="a", header=not pd.io.common.file_exists(esthe_path), index=False, encoding="utf-8-sig")
                except:
                    continue
    
    driver.quit()
 

def getInfo():

    # driver = webdriver.Chrome()
    driver = webdriver.Firefox()
    driver.maximize_window()
    
    def extract_urls(filename):
        urls = set()
        try:
            with open(filename, "r", encoding="utf-8") as file:
                reader = csv.DictReader(file)  # Read as dictionary
                for row in reader:
                    if "URL" in row and row["URL"].strip():  # Ensure "URL" column exists
                        urls.add(row["URL"].strip())  # Store unique URLs
            return urls
        except Exception as e:
            print(f"Error reading {filename}: {e}")
            return set()
    
    for i in range(1,5):
        # Get URLs from both files
        esthes_urls = extract_urls(ESTHES[i])
        
        kanryou_urls = extract_urls(KANRYOUESTHES[i])
        
        new_urls = esthes_urls - kanryou_urls
            
        with open(ESTHES[i], "r", encoding="utf-8") as file:
            reader = csv.DictReader(file)  # Read as dictionary
            for row in reader:
                print(row)
                if row["URL"] == "" or not row["URL"] in new_urls:  # Check if missing
                    print(row["URL"])
                    continue
                else:
                    driver.get(row["URL"])
                    time.sleep(5)
                    
                    shop_info = {}
                    mainContents = driver.find_element(By.ID, "mainContents")
                    tableContents = mainContents.find_element(By.CSS_SELECTOR, "table.wFull.bdCell.bgThNml.fgThNml.vaThT.pCellV10H12.bgWhite.mT20")
                    
                    # 店舗名
                    try:
                        shop_info["title"] = mainContents.find_element(By.CLASS_NAME, "detailTitle").text
                        print(shop_info["title"])
                    except:
                        print("title exception")
                        shop_info["title"] = "N/A"

                    
                    # 店舗住所
                    try:
                        addr_tr = tableContents.find_elements(By.TAG_NAME, "tr")[1]
                        shop_info["addr"] = addr_tr.find_element(By.TAG_NAME, "td").text
                        print(shop_info["addr"])
                    except:
                        print("addr exception")
                        shop_info["addr"] = "N/A"

                    # スタッフの人数
                    try:
                        staff_tr = tableContents.find_elements(By.TAG_NAME, "tr")[7]
                        shop_info["staff"] = staff_tr.find_element(By.TAG_NAME, "td").text
                        print(shop_info["staff"])
                    except:
                        print("staff exception")
                        shop_info["staff"] = "N/A"
                    
                    # 席数
                    try:
                        equip_tr = tableContents.find_elements(By.TAG_NAME, "tr")[6]
                        shop_info["equip"] = equip_tr.find_element(By.TAG_NAME, "td").text
                        print(shop_info["equip"])
                    except:
                        print("equip exception")
                        shop_info["equip"] = "N/A"
                    
                    # 有料か無料か
                    shop_info["fee"] = "有料"
                    
                    # クーポンメニューの項目があるかどうか
                    shop_info["coupon"] = "あり"
                    
                    # 店舗電話番号
                    try:
                        tel_link = f'{row["URL"].split("?")[0]}tel/'
                        driver.execute_script("window.open(arguments[0], '_blank');", tel_link)
                        time.sleep(3)
                        
                        driver.switch_to.window(driver.window_handles[1])
                        time.sleep(1)
                        
                        shop_info["tel"] = driver.find_element(By.CSS_SELECTOR, "td.fs16").text
                        print(shop_info["tel"])
                        
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)
                    except:
                        print("tel exception")
                        shop_info["tel"] = "N/A"
                        driver.close()
                        driver.switch_to.window(driver.window_handles[0])
                        time.sleep(1)
                    
                    scraped_data = {
                        "エステ種別": row["\ufeffエステ種別"],
                        "都道府県": row["都道府県"],
                        "URL": row["URL"],
                        "店舗名": shop_info['title'],
                        "店舗住所": shop_info['addr'],
                        "店舗電話番号": shop_info['tel'],
                        "スタッフの人数": shop_info['staff'],
                        "席数": shop_info['equip'],
                        "有料か無料か": shop_info['fee'],
                        "クーポンメニューの項目があるかどうか": shop_info['coupon'],
                    }
                    
                    # Save to CSV
                    out = pd.DataFrame([scraped_data])
                    out.to_csv(KANRYOUESTHES[i], mode="a", header=not pd.io.common.file_exists(KANRYOUESTHES[i]), index=False, encoding="utf-8-sig")

        print("Scraping and filling complete!")


if __name__ == '__main__':
    get_shop_urls()