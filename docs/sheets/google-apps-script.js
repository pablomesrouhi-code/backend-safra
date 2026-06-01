/**
 * Safra Skin - Google Sheets order webhook
 * Sheet: https://docs.google.com/spreadsheets/d/12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw/edit
 *
 * 1. Extensions > Apps Script > paste ALL > Save
 * 2. Run testAppendRow (authorize)
 * 3. Deploy > New deployment > Web app > Me > Anyone
 * 4. Copy /exec URL > GOOGLE_SHEETS_WEBHOOK_URL in Easypanel
 */

var SPREADSHEET_ID = '12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw';
var SHEET_NAME = 'Orders';

function parseBody_(e) {
  if (!e) {
    throw new Error('No request data');
  }
  if (e.parameter && e.parameter.payload) {
    return JSON.parse(e.parameter.payload);
  }
  if (e.postData) {
    if (e.postData.contents) {
      return JSON.parse(e.postData.contents);
    }
    if (typeof e.postData.getDataAsString === 'function') {
      var raw = e.postData.getDataAsString();
      if (raw) {
        return JSON.parse(raw);
      }
    }
  }
  throw new Error('Empty body - send JSON or form field payload');
}

function ensureOrdersSheet_() {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.getRange(1, 1, 1, 11).setValues([[
      'date', 'orderid', 'country', 'name', 'phone', 'product',
      'sku', 'quantity', 'total_price', 'currency', 'status'
    ]]);
    sheet.setFrozenRows(1);
    sheet.getRange(1, 1, 1, 11).setFontWeight('bold');
  }
  return sheet;
}

function getOrdersSheet_() {
  return ensureOrdersSheet_();
}

function appendOrderRow_(data) {
  var totalPrice = '';
  if (data.total_price !== undefined && data.total_price !== null) {
    totalPrice = data.total_price;
  }
  var statusVal = '';
  if (data.status !== undefined && data.status !== null) {
    statusVal = data.status;
  }
  getOrdersSheet_().appendRow([
    data.date || '',
    data.orderid || '',
    data.country || 'KSA',
    data.name || '',
    data.phone || '',
    data.product || '',
    data.sku || '',
    data.quantity || '',
    totalPrice,
    data.currency || 'SAR',
    statusVal
  ]);
}

function testAppendRow() {
  appendOrderRow_({
    date: Utilities.formatDate(new Date(), 'Asia/Riyadh', 'dd/MM/yyyy'),
    orderid: 'nama-test-manual',
    country: 'KSA',
    name: 'test',
    phone: '966501234567',
    product: 'test product',
    sku: 'SK847291CY',
    quantity: '1',
    total_price: 199,
    currency: 'SAR',
    status: ''
  });
}

function doPost(e) {
  try {
    var data = parseBody_(e);
    appendOrderRow_(data);
    return ContentService.createTextOutput(
      JSON.stringify({ success: true, orderid: data.orderid })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, error: String(err.message || err) })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet(e) {
  try {
    if (e && e.parameter && e.parameter.payload) {
      var data = JSON.parse(e.parameter.payload);
      appendOrderRow_(data);
      return ContentService.createTextOutput(
        JSON.stringify({ success: true, orderid: data.orderid })
      ).setMimeType(ContentService.MimeType.JSON);
    }
    getOrdersSheet_();
    return ContentService.createTextOutput(
      JSON.stringify({
        status: 'Safra Skin order webhook active',
        spreadsheetId: SPREADSHEET_ID,
        sheet: SHEET_NAME
      })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, error: String(err.message || err) })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}
