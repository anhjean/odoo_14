/**
 * Converts a JS string to a UTF-8 "byte" array.
 * @param {string} str 16-bit unicode string.
 * @return {!Array<number>} UTF-8 byte array.
 * get this code from 
 * https://github.com/google/closure-library/blob/e877b1eac410c0d842bcda118689759512e0e26f/closure/goog/crypt/crypt.js
 */


var stringToUtf8ByteArray = function(str) {
    // TODO(user): Use native implementations if/when available
    var out = [], p = 0;
    for (var i = 0; i < str.length; i++) {
      var c = str.charCodeAt(i);
      if (c < 128) {
        out[p++] = c;
      } else if (c < 2048) {
        out[p++] = (c >> 6) | 192;
        out[p++] = (c & 63) | 128;
      } else if (
          ((c & 0xFC00) == 0xD800) && (i + 1) < str.length &&
          ((str.charCodeAt(i + 1) & 0xFC00) == 0xDC00)) {
        // Surrogate Pair
        c = 0x10000 + ((c & 0x03FF) << 10) + (str.charCodeAt(++i) & 0x03FF);
        out[p++] = (c >> 18) | 240;
        out[p++] = ((c >> 12) & 63) | 128;
        out[p++] = ((c >> 6) & 63) | 128;
        out[p++] = (c & 63) | 128;
      } else {
        out[p++] = (c >> 12) | 224;
        out[p++] = ((c >> 6) & 63) | 128;
        out[p++] = (c & 63) | 128;
      }
    }
    return out;
  };

  /**
   * Function này phải dùng stringToUtf8ByteArray để convert về Byte[]
   * @param {*} str 
   * @param {*} offset 
   * @returns 
   */
  function getCrc16(str, offset) {
       let data = stringToUtf8ByteArray(str);
        if (data == null || offset < 0 || offset > data.length - 1 || offset + length > data.length) {
            return 0;
        }
    
        let crc = 0xFFFF;
        for (let i = 0; i < str.length; ++i) {
            crc ^= data[offset + i] << 8;
            for (let j = 0; j < 8; ++j) {
                crc = (crc & 0x8000) > 0 ? (crc << 1) ^ 0x1021 : crc << 1;
            }
        }
        return (crc & 0xFFFF).toString(16).toUpperCase();
  }

  
/**
 * Function này không dùng stringToUtf8ByteArray để convert về Byte[]
 * @param {Chuỗi cần check CRC} text 
 * @param {true hoặc false, mặc định là true} hex_output 
 * @returns 
 */
function getCrc16_array(text, hex_output = true) {
    // adapted from https://github.com/damonlear/CRC16-CCITT
    // by https://stackoverflow.com/users/13045193/doubleunary
    // for https://stackoverflow.com/q/68235740/13045193
    // Example: http://www.ip33.com/crc.html
    if (!Array.isArray(text))
      text = [[text]];
    const polynomial = 0x1021;
    let result = text.map(row => row.map(string => {
      if (!string.length)
        return null;
      const bytes = Array.from(String(string))
        .map(char => char.charCodeAt(0) & 0xff); // gives 8 bits; higher bits get discarded
      let crc = 0xffff;
      bytes.forEach(byte => {
        for (let i = 0; i < 8; i++) {
          let bit = 1 === (byte >> (7 - i) & 1);
          let c15 = 1 === (crc >> 15 & 1);
          crc <<= 1;
          if (c15 ^ bit)
            crc ^= polynomial;
        }
      });
      crc &= 0xffff;
      return hex_output ? crc.toString(16).toUpperCase() : crc;
    }));
    return result.toString();
  }

// import {qrcode} from "/pos_point_of_sale_logo/static/src/js/qrcode.js";
function myqrcode(qr_text) {
    var init_text = "00020101021238530010A0000007270123000697043201091290057180208QRIBFTTA53037045802VN5920NGUYEN PHAM THUY LAN62390835Thanh toan don hang cho Bean Bakery6304";
    // var CRC = "3AA2";
    let text ="";
    if (qr_text) {text = qr_text}
    else { text = init_text + getCrc16_array(init_text)}; 
    var qr = qrcode( 0, "M");
    qr.addData(text, "Byte");
    qr.make();
    console.log(getCrc16(init_text,0));
    console.log(getCrc16_array(init_text));
    return qr.createImgTag();
};

var bank_code_value ={
  ABBANK:"970425",
  ACB:"970416",
  AGRIBANK:"970405",
  BAB:"970409",
  BIDV:"970488",
  BIDV:"970418",
  BVBANK:"970438",
  COOPBANK:"970446",
  DABANK:"970406",
  EXIMBANK:"970431",
  GPBANK:"970408",
  HDBANK:"970437",
  HLBANK:"970442",
  IVB:"970434",
  KLB:"970452",
  LVB:"970449",
  MB:"970422",
  MSB:"970426",
  NAMABANK:"970428",
  NCB:"970419",
  OCB:"970448",
  PGBANK:"970430",
  PVC:"970412",
  SCB:"970429",
  SEA:"970440",
  SGBANK:"970400",
  SHINHAN:"970424",
  SHB:"970443",
  SACOMBANK:"970403",
  TECHCOMBANK:"970407",
  TIENPHONGBANK:"970423",
  UOB:"970458",
  VAB:"970427",
  VC:"970460",
  VIETCOMBANK:"970436",
  VCCB:"970454",
  VIB:"970441",
  VPBANK:"970432",
  VRB:"970421",
  VIENTINBANK:"970415",
  WRB:"970457",
}

function dynamicQrcode( bank_holder = "NGUYEN PHAM THUY LAN", bank_account = "129005718", bank_code = "VPBank", bill_value="10000",bill_no="", bill_detail="Thanh toan don hang cho Bean Bakery",account_type = true, dynamic_qrcode = true ){
  // console.log (bank_holder + '-'+ bank_account + '-'+ bank_code+"-" + bill_value+'-'+bill_detail)
  
  let init_qrcode = dynamic_qrcode ?"000201010212":"000201010211";
  let napas_GUID = "0010A000000727";
  let napas_account_transfer = account_type ? "0208QRIBFTTA":"0208QRIBFTTC"
  let currency_code = "5303704";
  (bill_value.length>0)? bill_value = bill_value.replace(".","").replace(",",""): bill_value = "";
  let txn_value = "54"+ (bill_value.length < 10 ? "0" + bill_value.length.toString(): bill_value.length.toString()) + bill_value;
  let country_code = "5802VN";
  let merchant_name = "59"+ bank_holder.length.toString() + bank_holder;
  let crc_begin_code = "6304";
  
  let acquirer_code = "0006" +  bank_code_value[bank_code.toUpperCase()];
  let merchant_id = "01" + (bank_account.length<10? "0"+bank_account.length.toString() : bank_account.length.toString()) + bank_account;
  console.log('data:',acquirer_code.length,' ',merchant_id.length,' ',napas_account_transfer.length,' ',(acquirer_code.length+merchant_id.length+napas_account_transfer.length).toString() )
  let beneficiary= "01" + (acquirer_code.length+merchant_id.length+napas_account_transfer.length -12).toString() + acquirer_code + merchant_id + napas_account_transfer;
  let merchant_account_info = "38" + (napas_GUID.length+beneficiary.length).toString() + napas_GUID + beneficiary;
  let txn_purpose = "08" + (bill_detail.length<10? "0"+bill_detail.length.toString() : bill_detail.length.toString()) + bill_detail;
  let bill_number = bill_no.length >0 ? "01" + (bill_no.length < 10 ? "0"+ bill_no.length.toString() : bill_no.length.toString()) + bill_no : ""
  let additional_data="62" + (txn_purpose.length + bill_number.length).toString()  + bill_number +  txn_purpose

  let qrcode_data = init_qrcode + merchant_account_info + currency_code + txn_value + country_code + merchant_name + additional_data + crc_begin_code
  // let qrcode_data = init_qrcode + merchant_account_info + currency_code + txn_value + country_code  + additional_data + crc_begin_code
  qrcode_data = qrcode_data + getCrc16_array(qrcode_data);
  console.log(qrcode_data);
  var qr = qrcode( 0, "M");
    qr.addData(qrcode_data, "Byte");
    qr.make();
    
    return qr.createImgTag();

}

function nonAccentVietnamese(str) {
  str = str.toLowerCase();
//     We can also use this instead of from line 11 to line 17
//     str = str.replace(/\u00E0|\u00E1|\u1EA1|\u1EA3|\u00E3|\u00E2|\u1EA7|\u1EA5|\u1EAD|\u1EA9|\u1EAB|\u0103|\u1EB1|\u1EAF|\u1EB7|\u1EB3|\u1EB5/g, "a");
//     str = str.replace(/\u00E8|\u00E9|\u1EB9|\u1EBB|\u1EBD|\u00EA|\u1EC1|\u1EBF|\u1EC7|\u1EC3|\u1EC5/g, "e");
//     str = str.replace(/\u00EC|\u00ED|\u1ECB|\u1EC9|\u0129/g, "i");
//     str = str.replace(/\u00F2|\u00F3|\u1ECD|\u1ECF|\u00F5|\u00F4|\u1ED3|\u1ED1|\u1ED9|\u1ED5|\u1ED7|\u01A1|\u1EDD|\u1EDB|\u1EE3|\u1EDF|\u1EE1/g, "o");
//     str = str.replace(/\u00F9|\u00FA|\u1EE5|\u1EE7|\u0169|\u01B0|\u1EEB|\u1EE9|\u1EF1|\u1EED|\u1EEF/g, "u");
//     str = str.replace(/\u1EF3|\u00FD|\u1EF5|\u1EF7|\u1EF9/g, "y");
//     str = str.replace(/\u0111/g, "d");
  str = str.replace(/à|á|ạ|ả|ã|â|ầ|ấ|ậ|ẩ|ẫ|ă|ằ|ắ|ặ|ẳ|ẵ/g, "a");
  str = str.replace(/è|é|ẹ|ẻ|ẽ|ê|ề|ế|ệ|ể|ễ/g, "e");
  str = str.replace(/ì|í|ị|ỉ|ĩ/g, "i");
  str = str.replace(/ò|ó|ọ|ỏ|õ|ô|ồ|ố|ộ|ổ|ỗ|ơ|ờ|ớ|ợ|ở|ỡ/g, "o");
  str = str.replace(/ù|ú|ụ|ủ|ũ|ư|ừ|ứ|ự|ử|ữ/g, "u");
  str = str.replace(/ỳ|ý|ỵ|ỷ|ỹ/g, "y");
  str = str.replace(/đ/g, "d");
  // Some system encode vietnamese combining accent as individual utf-8 characters
  str = str.replace(/\u0300|\u0301|\u0303|\u0309|\u0323/g, ""); // Huyền sắc hỏi ngã nặng 
  str = str.replace(/\u02C6|\u0306|\u031B/g, ""); // Â, Ê, Ă, Ơ, Ư
  return str.toUpperCase();
}