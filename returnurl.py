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

# 測試特店資料：C2C
# MerchantID = '2000933'
# HashKey = 'XBERn1YOvpM9nfZc'
# HashIV = 'h1ONHk4P4yqbl5LK'

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
        text = cipher.decrypt(content).decode('utf-8')
        return self.pkcs7padding(text)

aes_tool = AESTool()

app = Flask(__name__)
# app.config['JSON_AS_ASCII'] = False

def SHA256_CheckMacValue(hashStr) -> str:
    """
    輸入排序好的字串, 獲得檢查碼
    """
    # 將整串字串進行URL encode, 並轉為小寫
    url_encodeStr = urllib.parse.quote_plus(hashStr).lower()
    
    # 以SHA256加密方式來產生雜凑值, 再轉大寫產生
    CheckMacValue = hashlib.sha256(url_encodeStr.encode('utf-8')).hexdigest().upper()
    return CheckMacValue

def MD5_CheckMacValue(hashStr) -> str:
    """
    輸入排序好的字串, 獲得檢查碼
    """
    # 將整串字串進行URL encode, 並轉為小寫
    url_encodeStr = urllib.parse.quote_plus(hashStr).lower()

    # 以MD5加密方式來產生雜凑值, 再轉大寫產生
    CheckMacValue = hashlib.md5(
        url_encodeStr.encode('utf-8')).hexdigest().upper()
    return CheckMacValue

@app.route('/')
def home():
    return ('this is ServerReplyURL')

# 核對CheckMacValue檢查碼使用 -> 全方位金流API
# Content Type ：application/x-www-form-urlencoded
@app.route('/ResultUrl_SHA256', methods=["GET", "POST"])
def ResultUrl_SHA256():
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
        CheckMacValue = SHA256_CheckMacValue(hashStr)

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

# AES解密使用 -> 站內付2.0, 全方位物流服務, 跨境物流API
# Content Type：application/json
@app.route('/ResultUrl_AES', methods=["GET", "POST"])
def ResultUrl_AES():
    if request.method == 'POST':
        get_data = request.get_data() # type = bytes
        # print(return_data, type(return_data))
        get_data.decode('utf-8')
        dict_data = json.loads(get_data.decode('utf-8'))
        # print(dict_data)
        # 將回傳的DATA取出後解密
        decrypt_str = aes_tool.aes_decrypt(dict_data['Data'])
        # URLDecode解碼
        data_unquote = urllib.parse.unquote(decrypt_str) # type = str
        print(data_unquote)
        if dict_data['TransCode'] == 1:
            import time
            Timestamp = {'Timestamp':int(time.time())}
            return_params = {
                'MerchantID': '2000132',
                    'RpHeader': {
                        'Timestamp': Timestamp
                    },
                    "TransCode": 1,
                    "TransMsg": "",
                    'Data': ''
                }
            Data = {
                'RtnCode':1,
                'RtnMsg':'OK'
            }

            # Data參數轉為URLEncode
            data_json = json.dumps(Data)

            urlEncode_str = urllib.parse.quote(data_json)
            # print('URLEncode: '+urlEncode_str)
            # AES 加密
            encrypt_str = aes_tool.aes_encrypt(urlEncode_str) # type = str
            # print('AES 加密: '+encrypt_str)
            # 將加密的Data加入字典
            return_params['Data'] = encrypt_str
            # dict to json 
            json_str = json.dumps(return_params, separators=(',', ':'))
            content = json_str        
            print(content)
            return content
    elif request.method == 'GET':
        content = '這裡是GET頁面'
        return content

# 核對CheckMacValue檢查碼使用 -> 物流整合API
# Content Type ：application/x-www-form-urlencoded
@app.route('/ResultUrl_MD5', methods=["GET", "POST"])
def ResultUrl_MD5():
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
        CheckMacValue = MD5_CheckMacValue(hashStr)

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

# 跨境物流API, 接收地圖資訊用
# Content Type ：application/x-www-form-urlencoded
@app.route('/CvsMap', methods=["GET", "POST"])
def CvsMap():
    print('店鋪資訊: ')
    # 判斷接收的結果
    if request.method == "POST":
        print('POST店鋪資訊: ')
        data_dict = request.form.to_dict() # type = dict
        print(data_dict)

    elif request.method == "GET":
        return "這裡是get頁面"


# 站內付2.0 綁定信用卡
# Content Type：application/json
@app.route('/ResultUrl_Credit', methods=["GET", "POST"])
def ResultUrl_Credit():
    if request.method == 'POST':
        get_data = request.get_data() # type = bytes
        # print(return_data, type(return_data))
        get_data.decode('utf-8')
        dict_data = json.loads(get_data.decode('utf-8'))
        # print(dict_data)
        # 將回傳的DATA取出後解密
        decrypt_str = aes_tool.aes_decrypt(dict_data['Data'])
        # URLDecode解碼
        data_unquote = urllib.parse.unquote(decrypt_str) # type = str
        print(data_unquote)    
        return data_unquote
    elif request.method == 'GET':
        content = '這裡是GET頁面'
        return content

if __name__=="__main__":
    app.run()