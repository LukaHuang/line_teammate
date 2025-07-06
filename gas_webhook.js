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
    
    const timestamp = data.timestamp || new Date().toLocaleString('zh-TW');
    const userId = data.user_id || 'unknown';
    
    // 根據資料類型選擇不同的工作表
    if (data.type === 'link') {
      // 儲存連結到收藏連結工作表
      const linkSheet = getOrCreateSheet('收藏連結');
      linkSheet.appendRow([timestamp, userId, data.link]);
      
    } else if (data.type === 'image') {
      // 儲存圖片到圖片工作表
      const imageSheet = getOrCreateSheet('圖片收藏');
      imageSheet.appendRow([timestamp, userId, data.image_url, data.message_id]);
      
    } else {
      // 一般對話儲存到對話記錄工作表
      const conversationSheet = getOrCreateSheet('LINE Bot 對話記錄');
      const conversation = data.conversation || '';
      conversationSheet.appendRow([timestamp, userId, conversation]);
    }
    
    // 回傳成功訊息
    return ContentService
      .createTextOutput(JSON.stringify({ 
        status: 'success', 
        message: 'Data saved successfully',
        type: data.type || 'conversation'
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

function getOrCreateSheet(sheetName = 'LINE Bot 對話記錄') {
  const MAIN_SPREADSHEET_NAME = 'LINE Bot 資料收集';
  
  // 嘗試取得現有試算表，如果沒有就建立新的
  let spreadsheet;
  
  // 檢查是否有現有的試算表檔案
  const files = DriveApp.getFilesByName(MAIN_SPREADSHEET_NAME);
  if (files.hasNext()) {
    const file = files.next();
    spreadsheet = SpreadsheetApp.openById(file.getId());
  } else {
    // 建立新的試算表
    spreadsheet = SpreadsheetApp.create(MAIN_SPREADSHEET_NAME);
  }
  
  let sheet = spreadsheet.getSheetByName(sheetName);
  
  if (!sheet) {
    sheet = spreadsheet.insertSheet(sheetName);
  }
  
  // 根據工作表類型設定不同的標題列
  if (sheet.getLastRow() === 0) {
    if (sheetName === '收藏連結') {
      sheet.getRange(1, 1, 1, 3).setValues([['時間', '用戶ID', '連結']]);
    } else if (sheetName === '圖片收藏') {
      sheet.getRange(1, 1, 1, 4).setValues([['時間', '用戶ID', '圖片URL', '訊息ID']]);
    } else {
      sheet.getRange(1, 1, 1, 3).setValues([['時間', '用戶ID', '對話內容']]);
    }
    sheet.getRange(1, 1, 1, sheet.getLastColumn()).setFontWeight('bold');
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