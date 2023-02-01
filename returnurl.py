# coding:utf-8 
from flask import Flask, request
import urllib
import hashlib
from Crypto.Cipher import AES
import base64
import json
# 特店測試資料:
# MerchantID = "3002607" # 模擬銀行3D驗證
# HashKey="pwFHCqoQZGmho4w6"
# HashIV="EkRm7iFT261dpevs"

MerchantID = "2000132" # 模擬無銀行3D驗證
HashKey="5294y06JbISpM5x9"
HashIV="v77hoKGq4kWxNNIS"

class AESTool:
    def __init__(self):
        self.key = HashKey.encode('utf-8')
        self.iv = HashIV.encode('utf-8')

    def pkcs7padding(self, text):
        """
        加密格式:PKCS7
        """
        bs = 16 # 長度16
        length = len(text) # 243
        bytes_length = len(text.encode('utf-8')) # 243
        padding_size = length if (bytes_length == length) else bytes_length
        # padding_size % bs = 3
        padding = bs - padding_size % bs
        # padding = 13
        padding_text = chr(padding) * padding # chr 編碼轉字符
        self.coding = chr(padding)

        return text + padding_text

    def aes_encrypt(self, content):
        """
        AES加密
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        # 整理字串
        content_padding = self.pkcs7padding(content)
        # 加密
        encrypt_bytes = cipher.encrypt(content_padding.encode('utf-8'))
        # 重新编码
        result = str(base64.b64encode(encrypt_bytes), encoding='utf-8')
        return result

    def aes_decrypt(self, content):
        """
        AES解密
        """
        cipher = AES.new(self.key, AES.MODE_CBC, self.iv)
        content = base64.b64decode(content)
        text = cipher.decrypt(content).decode('utf-8', errors='ignore')
        return self.pkcs7padding(text)

aes_tool = AESTool()

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

def get_CheckMacValue(hashStr) -> str:
    """
    輸入排序好的字串, 獲得檢查碼
    """
    # 將整串字串進行URL encode, 並轉為小寫
    url_encodeStr = urllib.parse.quote_plus(hashStr).lower()
    
    # 以SHA256加密方式來產生雜凑值, 再轉大寫產生
    CheckMacValue = hashlib.sha256(url_encodeStr.encode('utf-8')).hexdigest().upper()
    return CheckMacValue

@app.route('/')
def home():
    return ('this is ReturnURL')

# 全方位金流 AIO_ResultUrlData
@app.route('/AIO_ResultUrlData', methods=["GET", "POST"])
def AIO_ResultUrlData():
    # 判斷接收的結果
    if request.method == "POST":
        data_dict = request.form.to_dict() # type = dict
        print(data_dict)

        returnCheck = data_dict['CheckMacValue']
        print(f'收到的檢查碼 = {returnCheck}')

        # 將收到的回覆組成 data 字串
        # 檢查碼以外的字串重新排序, 形成新的字串
        sort_str = ''
        for k in sorted (data_dict) : 
            if k != 'CheckMacValue':
                sort_str += f'{k}={data_dict[k]}&'

        hashStr = f"HashKey={HashKey}&{sort_str}HashIV={HashIV}".lower()
        # 產生檢查碼
        CheckMacValue = get_CheckMacValue(hashStr)

        print(f'新的檢查碼 = {CheckMacValue}')
        # 核對驗證碼是否相同
        if returnCheck == CheckMacValue:
            print("1|OK")
            return "1|OK"
        else:
            print("驗證碼不符")
            return "驗證碼不符"

    elif request.method == "GET":
        return "這裡是get頁面"

# 全方位金流 AIO_PeriodReturnURL
@app.route('/AIO_PeriodReturnURL', methods=["GET", "POST"])
def AIO_PeriodReturnURL():
    # 特店測試資料:
    HashKey="pwFHCqoQZGmho4w6"
    HashIV="EkRm7iFT261dpevs"
    # 判斷接收的結果
    if request.method == "POST":
        data_dict = request.form.to_dict() # type = dict
        print(data_dict)

        returnCheck = data_dict['CheckMacValue']
        print(f'收到的檢查碼 = {returnCheck}')

        # 將收到的回覆組成 data 字串
        # 檢查碼以外的字串重新排序, 形成新的字串
        sort_str = ''
        for k in sorted (data_dict) : 
            if k != 'CheckMacValue':
                sort_str += f'{k}={data_dict[k]}&'

        hashStr = f"HashKey={HashKey}&{sort_str}HashIV={HashIV}".lower()
        # 產生檢查碼
        CheckMacValue = get_CheckMacValue(hashStr)

        print(f'新的檢查碼 = {CheckMacValue}')
        # 核對驗證碼是否相同
        if returnCheck == CheckMacValue:
            print("1|OK")
            return "1|OK"
        else:
            print("驗證碼不符")
            return "驗證碼不符"

    elif request.method == "GET":
        return "這裡是get頁面"

# # 全方位金流 AIO_PaymentInfoURL 取號付款結果通知
@app.route('/AIO_PaymentInfoURL', methods=["GET", "POST"])
def AIO_PaymentInfoURL():
    # 判斷接收的結果
    if request.method == "POST":
        data_dict = request.form.to_dict() # type = dict
        print(data_dict)

        returnCheck = data_dict['CheckMacValue']
        print(f'收到的檢查碼 = {returnCheck}')

        # 將收到的回覆組成 data 字串
        # 檢查碼以外的字串重新排序, 形成新的字串
        sort_str = ''
        for k in sorted (data_dict) : 
            if k != 'CheckMacValue':
                sort_str += f'{k}={data_dict[k]}&'

        hashStr = f"HashKey={HashKey}&{sort_str}HashIV={HashIV}".lower()
        # 產生檢查碼
        CheckMacValue = get_CheckMacValue(hashStr)

        print(f'新的檢查碼 = {CheckMacValue}')
        # 核對驗證碼是否相同
        if returnCheck == CheckMacValue:
            print("1|OK")
            return "1|OK"
        else:
            print("驗證碼不符")
            return "驗證碼不符"

    elif request.method == "GET":
        return "這裡是get頁面"

@app.route('/ResultUrlData', methods=["GET", "POST"])
def ResultUrlData():
    # 判斷接收的結果
    if request.method == "POST":
        data_dict = request.form.to_dict() # type = dict
        print(data_dict)

        returnCheck = data_dict['CheckMacValue']
        print(f'收到的檢查碼 = {returnCheck}')

        # 將收到的回覆組成 data 字串
        # 檢查碼以外的字串重新排序, 形成新的字串
        sort_str = ''
        for k in sorted (data_dict) : 
            if k != 'CheckMacValue':
                sort_str += f'{k}={data_dict[k]}&'

        hashStr = f"HashKey={HashKey}&{sort_str}HashIV={HashIV}".lower()
        # 產生檢查碼
        CheckMacValue = get_CheckMacValue(hashStr)

        print(f'新的檢查碼 = {CheckMacValue}')
        # 核對驗證碼是否相同
        if returnCheck == CheckMacValue:
            print("1|OK")
            return "1|OK"
        else:
            print("驗證碼不符")
            return "驗證碼不符"

    elif request.method == "GET":
        return "這裡是get頁面"


# 站內付2.0 接收用
@app.route('/PaymentResult', methods=["GET", "POST"])
def PaymentResult():
    content = ""
    # 判斷接收的結果
    if request.method == "POST":
        dict_data = request.json
        print(dict_data, type(dict_data)) # type = dict
        print('='*50)
        # print(dict_data['Data'])
        # print(return_dict)
        return_data = dict_data['Data']
        # 將回傳的DATA取出後解密
        decrypt_str = aes_tool.aes_decrypt(return_data)
        # URLDecode解碼
        data_unquote = urllib.parse.unquote(decrypt_str)
        print(data_unquote) # type = str
        # # 將回傳的DATA取出後解密
        # decrypt_str = aes_tool.aes_decrypt(dict_data['Data'])
        # # URLDecode解碼
        # content = urllib.parse.unquote(decrypt_str)
        # print('解碼後的Data: ' + content)

    elif request.method == "GET":
        content = '站內付2.0的ReturnURL, 付款結果通知'
        print(content)
    return content

# 接收門市地圖資訊
@app.route('/CvsMap', methods=["GET", "POST"])
def CvsMap():
    if request.method == 'POST':
        dict_data = request.form.to_dict()
        print('這裡是回傳資訊: ')
        print(dict_data, type(dict_data)) # type = dict
    elif request.method == 'GET':
        dict_data = '這邊是地圖回傳'
        print('這邊是地圖回傳')
    # return jsonify(dict_data)
    return json.dumps(dict_data, ensure_ascii=False)

# 物流整合API
@app.route('/ServerReplyURL', methods=["GET", "POST"])
def ServerReplyURL():
    if request.method == 'POST':
        dict_data = request.form.to_dict()
        print('這裡是回傳資訊: ')
        print(dict_data, type(dict_data)) # type = dict
    elif request.method == 'GET':
        dict_data = '物流整合API'
        print('物流整合API')
    # return jsonify(dict_data)
    return json.dumps(dict_data, ensure_ascii=False)

# 站內付2.0, 定期定額執行結果回應網址
@app.route('/PeriodReturnURL', methods=["GET", "POST"])
def PeriodReturnURL():
    if request.method == 'POST':
        dict_data = request.form.to_dict()
        print('這裡是回傳資訊: ')
        print(dict_data, type(dict_data)) # type = dict
    elif request.method == 'GET':
        dict_data = '站內付2.0, 定期定額執行結果回應'
        print('站內付2.0, 定期定額執行結果回應')
    # return jsonify(dict_data)
    return json.dumps(dict_data, ensure_ascii=False)

# 跨境物流API
@app.route('/CrossBorder', methods=["GET", "POST"])
def CrossBorder():
    if request.method == 'POST':
        dict_data = request.json
        # print(dict_data, type(dict_data)) # type = dict
        # print('='*50)
        # print(dict_data['Data'])
        # print(return_dict)
        return_data = dict_data['Data']
        # 將回傳的DATA取出後解密
        decrypt_str = aes_tool.aes_decrypt(return_data)
        # URLDecode解碼
        data_unquote = urllib.parse.unquote(decrypt_str)
        content = data_unquote # type = str
    elif request.method == 'GET':
        content = '跨境物流API'
        print('跨境物流API!')
    # return jsonify(dict_data)
    return content

# 新版全方位物流
@app.route('/New_logistic', methods=["GET", "POST"])
def New_logistic():
    if request.method == 'POST':
        # print('新版全方位物流! POST')
        return_data = request.form.to_dict() # type = dict
        key, value = list(return_data.items())[0]
        content = key + value
        dict_data = json.loads(content)
        # print(dict_data['Data'])
        # return_data = dict_data['Data']
        # 將回傳的DATA取出後解密
        decrypt_str = aes_tool.aes_decrypt(dict_data['Data'])
        # URLDecode解碼
        data_unquote = urllib.parse.unquote(decrypt_str)
        content = data_unquote # type = str
        print(content)
    elif request.method == 'GET':
        content = '新版全方位物流'
        print(content)
    # return jsonify(dict_data)
    return content

if __name__=="__main__":
    app.run()