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
    // 檢查是否有 POST 資料
    if (!e || !e.postData || !e.postData.contents) {
      throw new Error('No POST data received');
    }
    
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
      .createTextOutput(JSON.stringify({ 
        status: 'success', 
        message: 'Data saved successfully' 
      }))
      .setMimeType(ContentService.MimeType.JSON);
      
  } catch (error) {
    console.error('Error:', error);
    return ContentService
      .createTextOutput(JSON.stringify({ 
        status: 'error', 
        message: error.toString() 
      }))
      .setMimeType(ContentService.MimeType.JSON);
  }
}

function getOrCreateSheet() {
  const SHEET_NAME = 'LINE Bot 對話記錄';
  
  // 嘗試取得現有試算表，如果沒有就建立新的
  let spreadsheet;
  
  // 檢查是否有現有的試算表檔案
  const files = DriveApp.getFilesByName(SHEET_NAME);
  if (files.hasNext()) {
    const file = files.next();
    spreadsheet = SpreadsheetApp.openById(file.getId());
  } else {
    // 建立新的試算表
    spreadsheet = SpreadsheetApp.create(SHEET_NAME);
  }
  
  let sheet = spreadsheet.getSheetByName(SHEET_NAME);
  
  if (!sheet) {
    sheet = spreadsheet.insertSheet(SHEET_NAME);
  }
  
  // 檢查是否需要設定標題列
  if (sheet.getLastRow() === 0) {
    sheet.getRange(1, 1, 1, 3).setValues([['時間', '用戶ID', '對話內容']]);
    sheet.getRange(1, 1, 1, 3).setFontWeight('bold');
  }
  
  return sheet;
}

function doGet() {
  return ContentService.createTextOutput('LINE Bot Webhook is running!');
}

// 測試函數 - 可以在 GAS 編輯器中執行來測試
function testWebhook() {
  const testData = {
    timestamp: '2024-01-01 12:00:00',
    user_id: 'test_user',
    conversation: '測試對話內容'
  };
  
  const mockEvent = {
    postData: {
      contents: JSON.stringify(testData)
    }
  };
  
  const result = doPost(mockEvent);
  console.log('Test result:', result.getContent());
}