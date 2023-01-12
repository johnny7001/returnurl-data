from flask import Flask, request
import hashlib
import urllib.parse
import json
import os
from dotenv import load_dotenv
load_dotenv()
app = Flask(__name__, template_folder='templates')

HashKey = os.getenv("HashKey")
HashIV = os.getenv("HashIV")


@app.route('/')
def home():
    # 地點
    return ('this is GW_API')


@app.route('/returnData', methods=['GET', 'POST'])
def getData():
    if request.method == "POST":
        data_dict = request.form.to_dict()
        data_str = json.dumps(data_dict, indent=4)
        # 將接收到的值寫入html查看
        with open('templates/ResultUrlData.html', 'w+', encoding='utf-8') as file:
            file.write(data_str)

        checkStr = ""
        returnCheck = data_dict['CheckMacValue']
        print(f'收到的檢查碼 = {returnCheck}')
        for k, v in data_dict.items():
            if k != "CheckMacValue":
                checkStr += f"{k}={v}&"
        return_str = checkStr[:-1]
        hashStr = f"HashKey={HashKey}&{return_str}&HashIV={HashIV}"
        # 將整串字串進行URL encode, 並轉為小寫
        url_encodeStr = urllib.parse.quote_plus(hashStr)
        lower_encodeStr = url_encodeStr.lower()
        # print(lower_encodeStr)
        # 以SHA256加密方式來產生雜凑值
        hashStr256 = hashlib.sha256(
            lower_encodeStr.encode('utf-8')).hexdigest()
        # 再轉大寫產生CheckMacValue
        CheckMacValue = hashStr256.upper()
        print(f'新的檢查碼 = {CheckMacValue}')
        # 核對驗證碼是否相同
        if returnCheck == CheckMacValue:
            print("1|OK")
            return "1|OK"
        else:
            print("驗證碼不符")
            return "驗證碼不符"
    elif request.method == "GET":
        return "this is GET page!!"


app.run(host='0.0.0.0', port=3123, debug=True)
