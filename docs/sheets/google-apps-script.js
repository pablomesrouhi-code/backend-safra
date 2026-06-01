/**
 * SAFRA SKIN - Orders to Google Sheet
 * 1. Delete ALL code in Apps Script editor
 * 2. Paste this entire file
 * 3. Save
 * 4. Run testAppendRow once (authorize)
 * 5. Deploy > New deployment > Web app > Execute as: Me > Who has access: Anyone
 * 6. Copy URL ending in /exec -> GOOGLE_SHEETS_WEBHOOK_URL in Easypanel
 */

var SPREADSHEET_ID = '12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw';
var SHEET_NAME = 'Orders';

function processOrder_(data) {
  var ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
    sheet.appendRow([
      'date', 'orderid', 'country', 'name', 'phone', 'product',
      'sku', 'quantity', 'total_price', 'currency', 'status'
    ]);
    sheet.setFrozenRows(1);
  }

  var totalPrice = '';
  if (data.total_price !== undefined && data.total_price !== null) {
    totalPrice = data.total_price;
  }

  sheet.appendRow([
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
    data.status || ''
  ]);

  return data.orderid || '';
}

function readPayload_(e) {
  e = e || {};
  if (e.parameter && e.parameter.payload) {
    return JSON.parse(e.parameter.payload);
  }
  if (e.postData && e.postData.contents) {
    return JSON.parse(e.postData.contents);
  }
  throw new Error('Missing payload');
}

function jsonOut_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj))
    .setMimeType(ContentService.MimeType.JSON);
}

function testAppendRow() {
  processOrder_({
    date: '01/06/2026',
    orderid: 'nama-test-123',
    country: 'KSA',
    name: 'اختبار',
    phone: '966501234567',
    product: 'هدوء الدورة',
    sku: 'SK847291CY',
    quantity: '1',
    total_price: 199,
    currency: 'SAR',
    status: ''
  });
}

function doGet(e) {
  try {
    if (e && e.parameter && e.parameter.payload) {
      var data = readPayload_(e);
      var id = processOrder_(data);
      return jsonOut_({ success: true, orderid: id });
    }
    SpreadsheetApp.openById(SPREADSHEET_ID).getSheetByName(SHEET_NAME) ||
      SpreadsheetApp.openById(SPREADSHEET_ID).insertSheet(SHEET_NAME);
    return jsonOut_({ status: 'ok', sheet: SHEET_NAME });
  } catch (err) {
    return jsonOut_({ success: false, error: String(err.message || err) });
  }
}

function doPost(e) {
  try {
    var data = readPayload_(e);
    var id = processOrder_(data);
    return jsonOut_({ success: true, orderid: id });
  } catch (err) {
    return jsonOut_({ success: false, error: String(err.message || err) });
  }
}
