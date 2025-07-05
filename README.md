# LINE 語音備忘機器人

這是一個 LINE 機器人，可以將使用者的語音訊息轉換為文字並儲存為備忘錄，當使用者發送 `/save` 指令時，會將對話儲存到 Google Sheets。

## 功能特色

- 🎤 接收 LINE 語音訊息
- 🔄 使用 OpenAI Whisper API 將語音轉為文字
- 📝 自動累積對話內容
- 💾 透過 `/save` 指令儲存對話到 Google Sheets

## 安裝步驟

1. **設置虛擬環境**
   ```bash
   ./setup_venv.sh
   ```

2. **配置環境變數**
   ```bash
   cp .env.example .env
   ```
   編輯 `.env` 檔案，填入以下資訊：
   - LINE Channel Access Token
   - LINE Channel Secret
   - OpenAI API Key
   - Google Sheets 服務帳戶 JSON 檔案路徑
   - Google Spreadsheet ID

3. **啟動機器人**
   ```bash
   source venv/bin/activate
   python line_bot.py
   ```

## 使用方式

1. 向機器人發送語音訊息，會自動轉換為文字並儲存
2. 發送文字訊息也會被記錄
3. 發送 `/save` 來將目前的對話儲存到 Google Sheets
4. 儲存後對話記錄會被清空，可以開始新的對話

## 配置說明

### LINE Bot 設置
1. 在 LINE Developers 建立 Channel
2. 取得 Channel Access Token 和 Channel Secret
3. 設置 Webhook URL: `https://your-domain.com/callback`

### Google Sheets 設置
1. 建立 Google Cloud 專案
2. 啟用 Google Sheets API
3. 建立服務帳戶並下載 JSON 金鑰檔案
4. 在 Google Sheets 中分享試算表給服務帳戶

### OpenAI 設置
1. 註冊 OpenAI 帳號
2. 取得 API Key
3. 確保帳戶有足夠的 credits 使用 Whisper API