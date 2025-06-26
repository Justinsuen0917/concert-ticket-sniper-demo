# 如何使用及注意事項

## 第一步：安裝準備
1. **安裝 Python**  
   如果你的電腦未安裝 Python，請到 [Python 官網](https://www.python.org/) 下載並安裝。安裝時請務必勾選 **Add Python to PATH** 的選項。
2. **安裝必要套件**  
   打開你電腦的「端程機」(macOS) 或「命令提示字元 / PowerShell」(Windows)，複製並貼上以下指令，然後按 **Enter** 執行：

```bash
pip install selenium webdriver-manager
```

## 第二步：設定腳本（最重要的一步）
1. **複製程式碼**  
   將上面的 Python 程式碼完整複製，並儲存到一個檔案中，例如 `ticket_bot.py`。
2. **修改 `CONCERT_URL`**  
   將 `CONCERT_URL = '...'` 後面的網址換成你真正想搶飛的那個頁面（建議用開賣前顯示倒數計時的那個頁面）。
3. **找出並修改 `BUY_BUTTON_LOCATOR`**  
   - 用 Chrome 瀏覽器打開你的目標網頁。  
   - 在「購買」「立即預訂」或類似功能的按鈕上按右鍵，選擇 **檢查 (Inspect)**。  
   - 右邊會彈出開發者工具，並反發發現該按鈕的 HTML 程式碼。  
   - 你需要根據這段程式碼，決定用哪種方式來定位它（推薦使用 XPath）。

   **XPath 範例**  
   ```html
   <button>立即購買</button>
   ```
   XPath: `//button[text()='立即購買']`

   ```html
   <div class="btn">購買門票</div>
   ```
   XPath: `//div[contains(text(), '購買門票')]`

   > `contains(text(), '購買')` 的寫法比 `text()='購買門票'` 更靈活，因為有時按鈕文字前後可能有空格。

   將你找出的定位策略，更新到  
   ```python
   BUY_BUTTON_LOCATOR = (By.XPATH, "...")
   ```
   這一步的準確性直接決定腳本能否成功。

## 笭三步：執行腳本
1. 打開端程機，並切換到你儲存 `ticket_bot.py` 檔案的目錄。  
   例如，如果檔案在桌面，可以輸入：
   ```bash
   cd Desktop
   ```
2. 在開賣前約一兩分鐘，執行：
   ```bash
   python ticket_bot.py
   ```
3. 腳本會自動打開一個新的 Chrome 瀏覽器視窗並開始執行。  
   當腳本成功點擊按鈕後，它會停止刷新，並提示你 **「手動接管」**。  
   這時你要立即在該瀏覽器視窗中完成之後的所有步驟（登入、選票、付款等）。

---

