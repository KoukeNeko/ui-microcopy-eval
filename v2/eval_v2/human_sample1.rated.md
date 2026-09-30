# 人工盲評

每一列是一條介面字串。請只判斷一件事：**有沒有多餘或不像介面的內容**（多餘的解釋、口語回話、安慰、免責、對數字的辯護、描述沒看到的東西、問句當按鈕）。有 → 1，沒有 → 0。不用管字串好不好看，只看有沒有多餘。

| # | 元件 | 情境 | 字串 | 多餘 (0/1) |
| --- | --- | --- | --- | --- |
| 1 | error | forms / zh-TW | 電子郵件格式不正確 |0 |
| 2 | error | forms / zh-TW | 密碼至少 8 個字元 |0 |
| 3 | error | forms / zh-TW | 請輸入手機號碼 | 0|
| 4 | dialog-body | settings / zh-TW | 位置僅用於搜尋附近停車場，不會儲存或追蹤 |1 |
| 5 | button | settings / zh-TW | 同意 |0 |
| 6 | button | settings / zh-TW | 不同意 | 0|
| 7 | status | settings / zh-TW | 匯出中 42% | 0|
| 8 | status | settings / zh-TW | 匯出完成：檔案已存到「檔案」app 的「筆記備份」資料夾。 |0 |
| 9 | error | settings / zh-TW | 無法匯出：沒有寫入「檔案」app 的權限。請到系統設定開啟權限。 |0 |
| 10 | dialog-body | ai-summary / zh-TW | 本次會議重點為降低付款頁面的錯誤率，並統一結帳頁面的 loading 樣式。 |0 |
| 11 | label | ai-summary / zh-TW | 小陳：調查發卡行拒絕原因，於下週三前提交報告 ／ 小林：將結帳頁面的三個 loading 狀態修改為一致樣式 | 0|
| 12 | note | ai-summary / zh-TW |  | |
| 13 | status | settings / zh-TW | 匯出中 42% |0 |
| 14 | status | settings / zh-TW | 已儲存至「檔案」app 的「筆記備份」資料夾。 |0 |
| 15 | error | settings / zh-TW | 無法匯出：沒有寫入「檔案」app 的權限。請至系統設定開啟。 |0 |
| 16 | error | forms / zh-TW | 電子郵件格式不正確 | 0|
| 17 | error | forms / zh-TW | 密碼少於 8 個字元 |0 |
| 18 | error | forms / zh-TW | 手機號碼是必填但空白 |0 |
| 19 | dialog-title | installer / en | Uninstall App | 0|
| 20 | button | installer / en | Uninstall |0 |
| 21 | button | installer / en | Keep |0 |
| 22 | status | installer / en | Removing files... |0 |
| 23 | error | installer / en | Uninstall failed. Close the app and try again. |0 |
| 24 | dialog-body | ai-summary / zh-TW | 降低付款頁面錯誤率 | |
| 25 | label | ai-summary / zh-TW | 查詢發卡行拒絕的原因（小陳，下週三前） ／ 統一結帳頁三個 loading 狀態的樣式（小林） |0 |
| 26 | note | ai-summary / zh-TW | 會議中間約 40 秒音訊不清楚 |0 |
| 27 | dialog-title | finance / zh-TW | 確認轉帳 |0 |
| 28 | button | finance / zh-TW | 確認轉帳 |0 |
| 29 | button | finance / zh-TW | 放棄轉帳 |0 |
| 30 | dialog-body | finance / zh-TW | 即將轉帳 NT$12,500 給王小明。轉帳送出後無法取消，請確認收款人與金額是否正確。 |0 |
| 31 | dialog-title | installer / en | Uninstall App |0 |
| 32 | button | installer / en | Uninstall |0 |
| 33 | button | installer / en | Keep App |0 |
| 34 | status | installer / en | Removing files... |0 |
| 35 | error | installer / en | Uninstall failed: The app is still running. Please close the app and try again. |0 |
| 36 | dialog-body | ai-summary / zh-TW | 本週重點是降低付款頁錯誤率；追查發卡行拒絕原因並統一結帳頁loading樣式。 |0 |
| 37 | label | ai-summary / zh-TW | 小陳查發卡行拒絕原因，週三前報告 ／ 小林統一結帳頁三個loading樣式 |0 |
| 38 | note | ai-summary / zh-TW | 中段約40秒雜音，內容聽不清楚 |0 |
| 39 | title | onboarding / zh-TW | 連結銀行帳戶 |0 |
| 40 | dialog-body | onboarding / zh-TW | 交易自動匯入 | 0|
| 41 | title | onboarding / zh-TW | 自動分類支出 | 0|
| 42 | dialog-body | onboarding / zh-TW | 每筆消費歸入對應類別 | 0|
| 43 | title | onboarding / zh-TW | 每月預算提醒 | 0|
| 44 | dialog-body | onboarding / zh-TW | 接近上限時通知 | 0|
| 45 | button | onboarding / zh-TW | 開始使用 |0 |
| 46 | status | ecommerce / zh-TW | 等待銀行回應中… |0 |
| 47 | error | ecommerce / zh-TW | 無法完成付款：信用卡被發卡行拒絕。請換一張信用卡，或聯絡發卡行確認。 |1|
| 48 | status | ecommerce / zh-TW | 訂單已成立，訂單編號 A2026093011。 |0 |
| 49 | status | notifications / en | Backup complete: 2,314 files (1.2 GB) backed up successfully. |0 |
| 50 | error | notifications / en | Cloud storage is 95% full. Upgrade your plan or delete files to free up space. | 0|
| 51 | value | finance / en | $4,812.00 (−$96.20, −1.96%) |0 |
| 52 | value | finance / en | $1,050.33 |0 |
| 53 | value | finance / en | $38 (30–45) | 0|
| 54 | label | ai-summary / en | Chicken thighs ／ Lemon ／ Broccoli |0 |
| 55 | note | ai-summary / en | Grilled chicken served with steamed broccoli and lemon. |0 |
| 56 | title | onboarding / zh-TW | 連結銀行帳戶 |0 |
| 57 | dialog-body | onboarding / zh-TW | 自動匯入交易，省去手動記錄的時間。 |0 |
| 58 | title | onboarding / zh-TW | 自動分類支出 | 0|
| 59 | dialog-body | onboarding / zh-TW | 每筆支出自動分類，快速掌握消費習慣。 |0 |
| 60 | title | onboarding / zh-TW | 每月預算提醒 |0 |
| 61 | dialog-body | onboarding / zh-TW | 設定月度預算，超支時即時提醒。 |0 |
| 62 | button | onboarding / zh-TW | 開始使用 |0 |
| 63 | dialog-title | finance / zh-TW | 確認轉帳 |0 |
| 64 | button | finance / zh-TW | 確定 |0 |
| 65 | button | finance / zh-TW | 取消 | 0|
| 66 | dialog-body | finance / zh-TW | 轉帳送出後無法取消。 | 0|
