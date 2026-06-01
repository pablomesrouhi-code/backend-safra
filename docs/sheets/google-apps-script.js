/**
 * Safra Skin — Google Sheets order webhook (no secret)
 *
 * Sheet: https://docs.google.com/spreadsheets/d/12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw/edit
 *
 * 1. Extensions → Apps Script → paste ALL below → Save
 * 2. Run testAppendRow once (authorize when asked)
 * 3. Deploy → New deployment → Web app → Me → Anyone
 * 4. Copy /exec URL → GOOGLE_SHEETS_WEBHOOK_URL in Easypanel backend
 */

const SPREADSHEET_ID = '12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw';
const SHEET_NAME = 'Orders';

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
      const raw = e.postData.getDataAsString();
      if (raw) {
        return JSON.parse(raw);
      }
    }
  }
  throw new Error('Empty body — backend must send JSON or form field "payload"');
}

function getOrdersSheet_() {
  const ss = SpreadsheetApp.openById(SPREADSHEET_ID);
  const sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    throw new Error('Tab "' + SHEET_NAME + '" not found in spreadsheet');
  }
  return sheet;
}

function appendOrderRow_(data) {
  getOrdersSheet_().appendRow([
    data.date || '',
    data.orderid || '',
    data.country || 'KSA',
    data.name || '',
    data.phone || '',
    data.product || '',
    data.sku || '',
    data.quantity || '',
    data.total_price !== undefined && data.total_price !== null ? data.total_price : '',
    data.currency || 'SAR',
    data.status !== undefined && data.status !== null ? data.status : '',
  ]);
}

/** Run once from editor to verify sheet access */
function testAppendRow() {
  appendOrderRow_({
    date: Utilities.formatDate(new Date(), 'Asia/Riyadh', 'dd/MM/yyyy'),
    orderid: 'nama-test-manual',
    country: 'KSA',
    name: 'اختبار',
    phone: '966501234567',
    product: 'هدوء الدورة',
    sku: 'SK847291CY',
    quantity: '1',
    total_price: 199,
    currency: 'SAR',
    status: '',
  });
}

function doPost(e) {
  try {
    const data = parseBody_(e);
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

function doGet() {
  try {
    getOrdersSheet_();
    return ContentService.createTextOutput(
      JSON.stringify({
        status: 'Safra Skin order webhook active',
        spreadsheetId: SPREADSHEET_ID,
        sheet: SHEET_NAME,
      })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ status: 'error', error: String(err.message || err) })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}
