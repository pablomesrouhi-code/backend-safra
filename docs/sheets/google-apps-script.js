/**
 * Safra Skin — Google Sheets Order Webhook Receiver
 *
 * Setup:
 * 1. Create Google Sheet with tab named "Orders"
 * 2. Import order-template.csv as header row
 * 3. Extensions → Apps Script → paste this file
 * 4. Set SECRET below to match GOOGLE_SHEETS_SECRET in backend
 * 5. Deploy → New deployment → Web app
 *    - Execute as: Me
 *    - Who has access: Anyone
 * 6. Copy deployment URL → GOOGLE_SHEETS_WEBHOOK_URL in backend env
 */

const SECRET = 'your_random_secret_string'; // MUST match backend GOOGLE_SHEETS_SECRET
const SHEET_NAME = 'Orders';

function doPost(e) {
  try {
    const data = JSON.parse(e.postData.contents);

    if (data.secret !== SECRET) {
      return ContentService.createTextOutput(
        JSON.stringify({ success: false, error: 'Unauthorized' })
      ).setMimeType(ContentService.MimeType.JSON);
    }

    const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName(SHEET_NAME);
    if (!sheet) {
      throw new Error('Sheet "Orders" not found');
    }

    sheet.appendRow([
      data.order_id || '',
      data.created_at || new Date().toISOString(),
      data.customer_name || '',
      data.customer_phone || '',
      data.items_json || '',
      data.items_display || '',
      data.tier_count || '',
      data.tier_total_sar || '',
      data.upsell_accepted ? 'YES' : 'NO',
      data.upsell_product || '',
      data.upsell_price_sar || 0,
      data.grand_total_sar || '',
      data.payment || 'COD',
      data.status || 'pending_confirmation',
      data.utm_source || '',
      data.utm_campaign || '',
      data.event_id || '',
      data.notes || '',
    ]);

    return ContentService.createTextOutput(
      JSON.stringify({ success: true, order_id: data.order_id })
    ).setMimeType(ContentService.MimeType.JSON);
  } catch (err) {
    return ContentService.createTextOutput(
      JSON.stringify({ success: false, error: err.message })
    ).setMimeType(ContentService.MimeType.JSON);
  }
}

function doGet() {
  return ContentService.createTextOutput(
    JSON.stringify({ status: 'Safra Skin webhook active' })
  ).setMimeType(ContentService.MimeType.JSON);
}
