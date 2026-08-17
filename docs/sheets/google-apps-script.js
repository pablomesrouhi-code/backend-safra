/**
 * Safraskin — Orders → Google Sheet
 *
 * 1. Open the sheet "order safraskin"
 * 2. Extensions → Apps Script
 * 3. Delete ALL old code, paste this file, Save
 * 4. Run testAppendRow once (authorize your Google account)
 * 5. Deploy → New deployment → Web app
 *      Execute as: Me
 *      Who has access: Anyone
 * 6. Copy the URL that ends with /exec
 * 7. EasyPanel backend → env GOOGLE_SHEETS_WEBHOOK_URL = that /exec URL
 *    (no secret — the link only)
 * 8. Redeploy the backend
 *
 * Sheet columns (row 1):
 * DATE | ORDERID | COUNTRY | NAME | PHONE | PRODUCT | SKU | QUANTITY | TOTAL PRICE | CURRENCE | STATUS
 */

var SHEET_NAME = "Orders";

var HEADERS = [
  "DATE",
  "ORDERID",
  "COUNTRY",
  "NAME",
  "PHONE",
  "PRODUCT",
  "SKU",
  "QUANTITY",
  "TOTAL PRICE",
  "CURRENCE",
  "STATUS",
];

function getSheet_() {
  var ss = SpreadsheetApp.getActiveSpreadsheet();
  if (!ss) {
    throw new Error("Open Apps Script from the Google Sheet (Extensions → Apps Script)");
  }
  var sheet = ss.getSheetByName(SHEET_NAME);
  if (!sheet) {
    sheet = ss.insertSheet(SHEET_NAME);
  }
  ensureHeaders_(sheet);
  return sheet;
}

function ensureHeaders_(sheet) {
  var first = sheet.getRange(1, 1, 1, HEADERS.length).getDisplayValues()[0];
  var empty = first.every(function (cell) {
    return String(cell || "").trim() === "";
  });
  if (empty) {
    sheet.getRange(1, 1, 1, HEADERS.length).setValues([HEADERS]);
    sheet.setFrozenRows(1);
  }
}

function processOrder_(data) {
  var sheet = getSheet_();
  var totalPrice = "";
  if (data.total_price !== undefined && data.total_price !== null && data.total_price !== "") {
    totalPrice = data.total_price;
  }

  sheet.appendRow([
    data.date || "",
    data.orderid || "",
    data.country || "MAROC",
    data.name || "",
    data.phone || "",
    data.product || "",
    data.sku || "",
    data.quantity || "",
    totalPrice,
    data.currency || "DH",
    "",
  ]);

  return data.orderid || "";
}

function readPayload_(e) {
  e = e || {};
  if (e.parameter && e.parameter.payload) {
    return JSON.parse(e.parameter.payload);
  }
  if (e.postData && e.postData.contents) {
    var raw = e.postData.contents;
    try {
      return JSON.parse(raw);
    } catch (err) {
      if (e.parameter && Object.keys(e.parameter).length) {
        return e.parameter;
      }
      throw err;
    }
  }
  throw new Error("Missing payload");
}

function jsonOut_(obj) {
  return ContentService.createTextOutput(JSON.stringify(obj)).setMimeType(
    ContentService.MimeType.JSON
  );
}

function testAppendRow() {
  processOrder_({
    date: "01/05/2026",
    orderid: "nama7k2m9q1x",
    country: "MAROC",
    name: "سارة بنعلي",
    phone: "0682767535",
    product: "كريم تفتيح الوجه/زيت تساقط الشعر · 60 مل",
    sku: "SK482917CL/SK156820CP",
    quantity: "2/2",
    total_price: 438,
    currency: "DH",
    status: "",
  });
}

function doGet(e) {
  try {
    if (e && e.parameter && e.parameter.payload) {
      var data = readPayload_(e);
      var id = processOrder_(data);
      return jsonOut_({ success: true, orderid: id });
    }
    getSheet_();
    return jsonOut_({ status: "ok", sheet: SHEET_NAME });
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
