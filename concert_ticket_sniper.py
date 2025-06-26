# -----------------------------------------------------------------------------
# 演唱會搶飛腳本 (Python + Selenium) - 教學範例
# 使用前準備：
# 1. 安裝 Python: https://www.python.org/downloads/
# 2. 開啟端程機 (Terminal) 或命令提示字元 (Command Prompt)，安裝必要的套件：
#    pip install selenium webdriver-manager
# -----------------------------------------------------------------------------

import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service

# --- 用戶設定區 (請根據你的目標修改以下資料) ---

# 1. 演唱會搶票頁面的完整網址
# 例如: 'https://www.cityline.com/Events.do'
CONCERT_URL = 'https://www.urbtix.hk/' # <--- 請將這裡換成目標網頁的 URL

# 2. 尋找「購買」或「選擇日期」按鈕的策略
# Selenium 提供多種定位方式 (By.ID, By.CLASS_NAME, By.XPATH 等)
# 你需要用瀏覽器的「檢查元素」功能來找出最適合的定位方式和值
#
# 範例：
# - 如果按鈕是 <button id="buy-ticket-btn">購買門票</button>，可以用 ID
#   BUTTON_LOCATOR = (By.ID, 'buy-ticket-btn')
# - 如果按鈕是 <a class="button primary">立即購買</a>，可以用 CLASS_NAME 或 XPATH
#   BUTTON_LOCATOR = (By.CLASS_NAME, 'primary')
#   BUTTON_LOCATOR = (By.XPATH, "//a[contains(text(), '立即購買')]") # 推薦使用 XPATH，更精準

# ** 這裡需要你根據實際網站情況填寫 **
BUY_BUTTON_LOCATOR = (By.XPATH, "//*[contains(text(), '購買門票') or contains(text(), '立即購買') or contains(text(), 'Buy Now')]") # <--- 這是一個通用範例，你必須修改成精準的目標

# 3. 腳本設定
REFRESH_INTERVAL = 0.5  # 每次刷新頁面的間隔時間（秒），不要設太低，以免被網站封鎖
MAX_ATTEMPTS = 500      # 最大嘗試次數，防止無限循環

# --- 腳本主體 (一般無需修改) ---

def initialize_driver():
    """初始化並返回一個 Chrome WebDriver 實例"""
    print("初始化瀏覽器驅動程式...")
    try:
        # 使用 webdriver-manager 自動下載及設定 ChromeDriver
        service = Service(ChromeDriverManager().install())
        options = webdriver.ChromeOptions()
        # 以下是一些可能有助於繞過檢測的選項（但不保證有效）
        options.add_argument("--disable-blink-features=AutomationControlled")
        options.add_experimental_option("excludeSwitches", ["enable-automation"])
        options.add_experimental_option('useAutomationExtension', False)
        
        driver = webdriver.Chrome(service=service, options=options)
        driver.execute_script("Object.defineProperty(navigator, 'webdriver', {get: () => undefined})")
        
        print("瀏覽器已啟動。")
        return driver
    except Exception as e:
        print(f"初始化 WebDriver 時發生錯誤: {e}")
        print("請確保你已安裝 Google Chrome 瀏覽器，並且網絡連線正常。")
        return None

def wait_for_button_and_click(driver, locator):
    """
    等待指定的按鈕出現並變為可點擊狀態，然後點擊它。
    如果按鈕不存在，則刷新頁面。
    """
    attempts = 0
    while attempts < MAX_ATTEMPTS:
        try:
            print(f"第 {attempts + 1} 次嘗試：正在尋找購買按鈕...")
            # 等待最多 REFRESH_INTERVAL 秒，讓按鈕出現
            wait = WebDriverWait(driver, REFRESH_INTERVAL)
            buy_button = wait.until(EC.element_to_be_clickable(locator))
            
            print("目標按鈕已找到並且可以點擊！")
            
            # 嘗試點擊按鈕
            try:
                buy_button.click()
                print("按鈕已點擊！任務可能已完成。")
                print("請立即手動接管瀏覽器，完成後續步驟（如登入、付款）。")
                return True # 成功點擊，跳出循環
            except Exception as e:
                print(f"點擊按鈕時發生錯誤：{e}")
                print("嘗試使用 JavaScript 點擊...")
                driver.execute_script("arguments[0].click();", buy_button)
                print("JavaScript 點擊已執行。請手動接管。")
                return True

        except TimeoutException:
            # 在指定時間內找不到按鈕，刷新頁面
            print("找不到按鈕或按鈕無法點擊，將在 0.5 秒後刷新頁面。")
            time.sleep(0.5)
            driver.refresh()
            attempts += 1
        except NoSuchElementException:
            print("頁面元素結構可能已改變，腳本無法找按鈕。請檢查你的 BUTTON_LOCATOR 設定。")
            time.sleep(0.5)
            driver.refresh()
            attempts += 1
        except Exception as e:
            print(f"發生未知錯誤：{e}")
            print("腳本將在 1 秒後繼續...")
            time.sleep(1)
            driver.refresh()
            attempts += 1
            
    print("已達到最大嘗試次數，腳本停止。")
    return False

def main():
    """主執行函數"""
    print("--- 演唱會搶飛腳本已啟動 ---")
    print(f"目標網項: {CONCERT_URL}")
    
    driver = initialize_driver()
    if not driver:
        return

    try:
        # 打開目標網頁
        print(f"正在打開目標網頁...")
        driver.get(CONCERT_URL)

        # 開始等待並點擊按鈕的循環
        success = wait_for_button_and_click(driver, BUY_BUTTON_LOCATOR)
        
        if success:
            # 成功後，給用户足夠時間手動操作
            print("腳本已暫停，請手動完成購買。瀏覽器將在 10 分鐘後自動關閉。")
            time.sleep(600)
        else:
            print("未能在指定嘗試次數內完成操作。")
            
    except Exception as e:
        print(f"在主流程中發生錯誤: {e}")
    finally:
        print("腳本執行完畢，關閉瀏覽器。")
        if driver:
            driver.quit()

if __name__ == "__main__":
    main()
