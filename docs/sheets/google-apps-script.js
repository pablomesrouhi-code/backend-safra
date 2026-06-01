/**
 * Safra Skin — Google Sheets order webhook (no secret)
 *
 * Sheet: https://docs.google.com/spreadsheets/d/12UOny_tW2vOVclTSe-jLoMeI_KqYZPGZ3TyfjyxBWWw/edit
 *
 * Setup:
 * 1. Open the sheet → tab must be named "Orders"
 * 2. Row 1 headers (import order-template.csv):
 *    date | orderid | country | name | phone | product | sku | quantity | total_price | currency | status
 * 3. Extensions → Apps Script → paste this file → Save
 * 4. Deploy → New deployment → Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 5. Copy deployment URL → GOOGLE_SHEETS_WEBHOOK_URL in backend Easypanel env
 */

const SHEET_NAME = 'Orders';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sheet) {
      throw new Error('Sheet "Orders" not found');
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
      data.total_price !== undefined && data.total_price !== null ? data.total_price : '',
      data.currency || 'SAR',
      data.status !== undefined && data.status !== null ? data.status : '',
    ]);

    return ContentService.createTextOutput(
      JSON.stringify({ success: true, orderid: data.orderid })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, error: err.message })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput(
    JSON.stringify({ status: 'Safra Skin order webhook active', sheet: SHEET_NAME })
  ).setMimeType(ContentService.MimeType.JSON);
}
