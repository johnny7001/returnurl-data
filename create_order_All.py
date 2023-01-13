import hashlib
from datetime import datetime
import urllib.parse
import os
def main():
    MerchantID = '3002607'
    MerchantTradeNo = datetime.now().strftime("NO%Y%m%d%H%M%S")  # string
    MerchantTradeDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")  # string
    TotalAmount = 3000
    TradeDesc = "交易測試"

    # 串接金鑰
    HashKey="pwFHCqoQZGmho4w6"
    HashIV="EkRm7iFT261dpevs"

    ItemName = "商品A#商品B#商品C"
    ReturnURL = 'https://returnurl-data.herokuapp.com/ResultUrlData'
    ClientBackURL = 'https://www.ecpay.com.tw/client_back_url.php'
    OrderResultURL = 'http://127.0.0.1:3124/OrderResultUrlData'
    PaymentInfoURL = 'https://www.ecpay.com.tw/payment_info_url.php'

    # 將加密字串檢核碼計算順序
    ChoosePaymen = f"ChoosePayment=ALL&ClientBackURL={ClientBackURL}&EncryptType=1&ItemName={ItemName}&MerchantID={MerchantID}&MerchantTradeDate={MerchantTradeDate}&MerchantTradeNo={MerchantTradeNo}&OrderResultURL={OrderResultURL}&PaymentInfoURL={PaymentInfoURL}&PaymentType=aio&ReturnURL={ReturnURL}&TotalAmount={TotalAmount}&TradeDesc={TradeDesc}"
    # 參數最前面加上HashKey、最後面加上HashIV
    hashStr = f"HashKey={HashKey}&{ChoosePaymen}&HashIV={HashIV}"
    # 將整串字串進行URL encode, 並轉為小寫
    url_encodeStr = urllib.parse.quote_plus(hashStr).lower()

    # 以SHA256加密方式來產生雜凑值, 再轉大寫產生
    hashStr256 = hashlib.sha256(url_encodeStr.encode('utf-8')).hexdigest().upper()

    # print(CheckMacValue)
    pay_url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5"

    payload = {
        'MerchantID': MerchantID,  # string
        'MerchantTradeNo': MerchantTradeNo,  # string
        'MerchantTradeDate': MerchantTradeDate,  # string
        'PaymentType': 'aio',
        'TotalAmount': TotalAmount,
        'TradeDesc': TradeDesc,
        'ItemName': ItemName,
        'ReturnURL': ReturnURL,  # 如何取得回覆網址, 此為必填欄位
        'ChoosePayment': 'ALL',  # 不指定付款方式
        'CheckMacValue': hashStr256,  # 如何取得檢查碼機制
        'EncryptType': 1,  # 請固定填入1，使用SHA256加密
        # 'StoreID':'', # 特店旗下店舖代號
        'ClientBackURL': ClientBackURL,  # Client端返回特店的按鈕連結
        # 'ItemURL':'', # 商品銷售網址
        # 'Remark':'交易備註', # 備註欄位
        # 'ChooseSubPayment':'', # 付款子項目
        'OrderResultURL': OrderResultURL,  # Client端回傳付款結果網址
        # 'NeedExtraPaidInfo':'N', # 是否需要額外的付款資訊
        # 'IgnorePayment':'', # 隱藏付款方式
        # 'PlatformID':'', # 特約合作平台商代號
        # 'CustomField1':'', # 自訂名稱欄位1, 提供合作廠商使用記錄用客製化使用欄位
        # 'Language': '',  # 預設語系為中文, ENG：英語, KOR：韓語, JPN：日語, CHI：簡體中文
        'PaymentInfoURL': PaymentInfoURL,
    }

    html = '<form id="data_set" action="' + pay_url + '" method="post">'
    for k, v in payload.items():
        html += '<input type="hidden" name="' + \
            str(k) + '" value="' + str(v) + '" />'

    html += '<script type="text/javascript">document.getElementById("data_set").submit();</script>'
    html += "</form>"

    # 將產生代碼寫入html檔案
    with open('templates/create_order.html', 'w+', encoding='utf-8') as file:
        file.write(html)
    
    # 打開html檔案
    import webbrowser
    file_path = os.path.abspath('templates/create_order.html')
    webbrowser.open_new_tab(file_path)

if __name__=="__main__":
    main()
