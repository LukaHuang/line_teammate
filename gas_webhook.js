/**
 * Google Apps Script Webhook 接收器
 * 1. 建立新的 Google Sheets
 * 2. 開啟 Google Apps Script (script.google.com)
 * 3. 貼上這段程式碼
 * 4. 部署為網頁應用程式
 * 5. 取得 Webhook URL
 */

function doPost(e) {
  try {
    // 解析 POST 請求的 JSON 資料
    const data = JSON.parse(e.postData.contents);
    
    // 取得或建立 Google Sheets
    const sheet = getOrCreateSheet();
    
    // 新增資料到試算表
    const timestamp = data.timestamp || new Date().toLocaleString('zh-TW');
    const userId = data.user_id || 'unknown';
    const conversation = data.conversation || '';
    
    sheet.appendRow([timestamp, userId, conversation]);
    
    // 回傳成功訊息
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'success', message: 'Data saved' }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    console.error('Error:', error);
    return ContentService
      .createTextOutput(JSON.stringify({ status: 'error', message: error.toString() }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getOrCreateSheet() {
  const SHEET_NAME = 'LINE Bot 對話記錄';
  
  // 嘗試開啟現有的試算表，如果不存在就建立新的
  let spreadsheet;
  try {
    // 如果有特定的 Spreadsheet ID，可以在這裡指定
    spreadsheet = SpreadsheetApp.getActiveSpreadsheet();
  } catch (e) {
    // 建立新的試算表
    spreadsheet = SpreadsheetApp.create(SHEET_NAME);
  }
  
  let sheet = spreadsheet.getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    sheet = spreadsheet.insertSheet(SHEET_NAME);
    // 設定標題列
    sheet.getRange(1, 1, 1, 3).setValues([['時間', '用戶ID', '對話內容']]);
    sheet.getRange(1, 1, 1, 3).setFontWeight('bold');
  }
  
  return sheet;
}

function doGet(e) {
  return ContentService.createTextOutput('LINE Bot Webhook is running!');
}