# 人工盲評（第二批）

這批只抽備註、說明、錯誤、狀態、數值這幾種元件。判準同前：**有沒有多餘或不像介面的內容**，有=1、沒有=0。另外若你覺得字串**少了必要資訊**（例如錯誤沒說原因），在最後一欄填 1，否則留空。

| # | 元件 | 情境 | 字串 | 多餘 (0/1) | 缺資訊 (1) |
| --- | --- | --- | --- | --- | --- |
| 1 | error | installer / en | Uninstall failed because the app is still running. Quit the app, then try again. |0 | |
| 2 | note | ai-summary / zh-TW | 會議中曾有約40秒的雜音導致內容聽不清楚，但未影響主要議題與行動項目的確認。 | 0| |
| 3 | status | notifications / en | 備份完成：2,314 個檔案（1.2 GB） |0 | |
| 4 | error | settings / zh-TW | 沒有寫入「檔案」app 的權限，請到系統設定開啟 |0 | |
| 5 | dialog-body | onboarding / zh-TW | 接近預算上限時提醒你，花錢更有底。 | 0| |
| 6 | error | installer / en | Can't uninstall: the app is still running. Quit the app, then try again. |0 | |
| 7 | dialog-body | onboarding / zh-TW | 設定預算上限，超支時即時通知，掌控財務健康 | 0| |
| 8 | status | ecommerce / zh-TW | 付款處理中 |0 | |
| 9 | status | installer / en | Removing files... | 0| |
| 10 | dialog-body | onboarding / zh-TW | 交易自動匯入 |0 | |
| 11 | value | finance / en | $4,812.00 (-$96.20, -1.96%) | 0| |
| 12 | note | ai-summary / en | No sauce on plate | 0| |
| 13 | value | finance / en | Est. $38 next month (range $30–$45) |0 | |
| 14 | dialog-body | onboarding / zh-TW | 自動匯入交易，不用手動記帳。 |0 | |
| 15 | dialog-body | ai-summary / zh-TW | 本週重點為降低付款頁錯誤率。 |0 | |
| 16 | value | finance / en | $38 est. ($30–$45) |0 | |
| 17 | note | health / zh-TW | 入睡花了 48 分鐘，遠高於過去 7 天平均 15 分鐘，建議睡前減少螢光，保持規律作息；今晚實際睡著 6 小時 20 分，未達目標 7 小時，明天可嘗試提前上床放鬆。 |0 | |
| 18 | status | settings / zh-TW | 匯出中：42% |0 | |
| 19 | error | forms / zh-TW | 手機號碼是必填但空白 |0 | |
| 20 | dialog-body | ai-summary / zh-TW | 壓低付款頁錯誤率為本週重點 |0 | |
| 21 | dialog-body | settings / zh-TW | 位置只用來找附近停車場，不會儲存或用於其他用途 | 1| |
| 22 | dialog-body | onboarding / zh-TW | 每筆消費自動歸類，餐飲、交通、購物一目瞭然。 | 0| |
| 23 | error | forms / zh-TW | 電子郵件格式不正確。請輸入完整的電子郵件地址，例如 name@example.com。 | 0| |
| 24 | error | settings / zh-TW | 沒有寫入「檔案」app 的權限，請在系統設定中開啟 |0 | |
| 25 | dialog-body | settings / zh-TW | 位置只用於搜尋附近停車場，不會收集或儲存 |1 | |
| 26 | note | ai-summary / zh-TW | 會議中曾有約40秒的雜音導致內容聽不清楚，但未影響主要議題與行動項目的確認。 |0 | |
| 27 | note | ai-summary / zh-TW | 約 40 秒聽不清楚，該段未納入 |0 | |
| 28 | dialog-body | onboarding / zh-TW | 綁定你的銀行帳戶，交易自動匯入，不必再手動記帳。 |0 | |
| 29 | dialog-body | onboarding / zh-TW | AI 自動辨識消費類別，如餐飲、交通、購物，讓支出一目了然 |0 | |
| 30 | status | installer / en | Removing files... |0 | |
| 31 | dialog-body | ai-summary / zh-TW | 主持人指出本週重點是降低付款頁錯誤率，並分配任務給小陳與小林。 | 0| |
| 32 | error | installer / en | Uninstall failed: [App Name] is still running. Please close the application and try again. |0 | |
| 33 | dialog-body | ai-summary / zh-TW | 本週重點為降低付款頁錯誤率，並指派後續調查與介面調整工作。 | 0| |
| 34 | dialog-body | ai-summary / zh-TW | 降低付款頁面錯誤率 | 0| |
| 35 | note | health / zh-TW | 入睡偏久，離目標還差40分 | 0| |
| 36 | value | finance / en | $1,050.33 |0 | |
| 37 | error | forms / zh-TW | 手機號碼為必填欄位，請填寫 |0 | |
| 38 | dialog-body | settings / zh-TW | 位置權限僅用於搜尋您附近的可用停車場，協助您快速找到停車位，我們不會收集、儲存或共享您的位置資訊。 | 0| |
| 39 | dialog-body | onboarding / zh-TW | 讓支出紀錄自動同步，不用手動輸入 | 0| |
| 40 | dialog-body | onboarding / zh-TW | 讓交易紀錄即時同步，省去手動輸入 | 0| |
| 41 | status | ecommerce / zh-TW | 訂單已成立！訂單編號：A2026093011 |0 | |
| 42 | error | forms / zh-TW | 電子郵件格式不正確。請輸入完整的電子郵件地址，例如 name@example.com。 |0 | |
| 43 | dialog-body | onboarding / zh-TW | 設定預算目標，超支時收到提醒 | 0| |
| 44 | note | ai-summary / zh-TW | 會議中段約 40 秒出現雜音聽不清，但核心決策與任務分配已明確。 |0 | |
