import hashlib
from datetime import datetime
import urllib.parse
import os
from dotenv import load_dotenv
load_dotenv()

def get_CheckMacValue(hashStr) -> str:
    """
    輸入排序好的字串, 獲得檢查碼
    """
    # 將整串字串進行URL encode, 並轉為小寫
    url_encodeStr = urllib.parse.quote_plus(hashStr).lower()
    
    # 以SHA256加密方式來產生雜凑值, 再轉大寫產生
    CheckMacValue = hashlib.sha256(url_encodeStr.encode('utf-8')).hexdigest().upper()
    return CheckMacValue

# 串接金鑰
HashKey = os.getenv("HashKey")
HashIV = os.getenv("HashIV")
MerchantID = os.getenv("MerchantID")

# 參數字典
order_params = {}

# 必填
order_params['MerchantID'] = MerchantID
MerchantTradeNo = datetime.now().strftime("NO%Y%m%d%H%M%S")  # string
MerchantTradeDate = datetime.now().strftime("%Y/%m/%d %H:%M:%S")  # string
order_params['MerchantTradeNo'] = MerchantTradeNo
order_params['MerchantTradeDate'] = MerchantTradeDate
order_params['PaymentType'] = 'aio'
order_params['TotalAmount'] = 3000
order_params['TradeDesc'] = "交易測試"
order_params['ItemName'] = "商品A#商品B#商品C"
order_params['ReturnURL'] = 'https://127.0.0.1:1234'
order_params['PaymentInfoURL'] = 'https://returnurl-data.herokuapp.com/ResultUrlData'
order_params['ChoosePayment'] = 'ALL'

order_params['EncryptType'] = 1

order_params['ClientBackURL'] = 'https://www.ecpay.com.tw/client_back_url.php'
order_params['PeriodReturnURL'] = 'https://www.ecpay.com.tw/receive.php'
# CreditInstallment = '3,6,12,18,24,30N' # 分期付款

# 可選填, 若無填寫則為''
order_params['StoreID'] = ''
order_params['ClientBackURL'] = ''
order_params['ItemURL'] = ''
order_params['Remark'] = ''
order_params['ChooseSubPayment'] = ''
order_params['OrderResultURL'] = 'http://127.0.0.1:3124/OrderResultUrlData'
order_params['NeedExtraPaidInfo'] = 'Y'
order_params['IgnorePayment'] = ''
order_params['PlatformID'] = ''

# 定期定額相關參數
# period_params = {
#     'PeriodAmount': PeriodAmount, # 交易金額[TotalAmount]設定金額必須和授權金額[PeriodAmount]相同。
#     'PeriodType': PeriodType, # M = 月, D = 日, Y = 年
#     'Frequency': Frequency, # 執行頻率
#     'ExecTimes': ExecTimes, # 總共執行的次數
#     'PeriodReturnURL': PeriodReturnURL
# }   
    
# inv_params = {
#     'RelateNumber': 'Tea0001', # 特店自訂編號
#     'CustomerID': 'TEA_0000001', # 客戶編號
#     'CustomerIdentifier': '53348111', # 統一編號
#     'CustomerName': '客戶名稱',
#     'CustomerAddr': '客戶地址',
#     'CustomerPhone': '0912345678', # 客戶手機號碼
#     'CustomerEmail': 'abc@ecpay.com.tw',
#     'ClearanceMark': '2', # 通關方式
#     'TaxType': '1', # 課稅類別
#     'CarruerType': '', # 載具類別
#     'CarruerNum': '', # 載具編號
#     'Donation': '1', # 捐贈註記
#     'LoveCode': '168001', # 捐贈碼
#     'Print': '1',
#     'InvoiceItemName': '測試商品1|測試商品2',
#     'InvoiceItemCount': '2|3',
#     'InvoiceItemWord': '個|包',
#     'InvoiceItemPrice': '35|10',
#     'InvoiceItemTaxType': '1|1',
#     'InvoiceRemark': '測試商品1的說明|測試商品2的說明',
#     'DelayDay': '0', # 延遲天數
#     'InvType': '07', # 字軌類別
# }

# 合併參數
# order_params.update(period_params)
# order_params.update(inv_params)

# 排序字串 -> 頭尾加上HashKey跟HashTV -> 轉小寫
sort_str = ''
for k in sorted (order_params) : 
    sort_str += f'{k}={order_params[k]}&'

hashStr = f"HashKey={HashKey}&{sort_str}HashIV={HashIV}".lower()
# 產生檢查碼
CheckMacValue = get_CheckMacValue(hashStr)
# 將檢查碼加入字典, 產生新字典
order_params['CheckMacValue'] = CheckMacValue

def main(pay_url, payload):
    html = '<form id="data_set" action="' + pay_url + '" method="post">'
    for k, v in payload.items():
        html += '<input type="hidden" name="' + \
            str(k) + '" value="' + str(v) + '" />'

    html += '<script type="text/javascript">document.getElementById("data_set").submit();</script>'
    html += "</form>"

    # 將產生代碼寫入html檔案
    with open('templates/create_order_creditCard_period.html', 'w+', encoding='utf-8') as file:
        file.write(html)
    
    # 打開html檔案
    import webbrowser
    file_path = os.path.abspath('templates/create_order_creditCard_period.html')
    webbrowser.open_new_tab(file_path)

if __name__=="__main__":
    main(payload = order_params,pay_url = "https://payment-stage.ecpay.com.tw/Cashier/AioCheckOut/V5")
