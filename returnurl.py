from flask import Flask, request
import urllib.parse
import hashlib

app = Flask(__name__)

HashKey="pwFHCqoQZGmho4w6"
HashIV="EkRm7iFT261dpevs"

@app.route('/')
def home():
    return ('this is ReturnURL')

@app.route('/ResultUrlData', methods=["GET", "POST"])
def ResultUrlData():
    # 判斷接收的結果
    if request.method == "POST":
        data_dict = request.form.to_dict() # type = dict
        print(data_dict)

        checkStr = ""
        returnCheck = data_dict['CheckMacValue']
        print(f'收到的檢查碼 = {returnCheck}')

        # 將收到的回覆組成 data 字串
        for k, v in data_dict.items():
            if k != "CheckMacValue":
                checkStr += f"{k}={v}&"
        return_str = checkStr[:-1]
        hashStr = f"HashKey={HashKey}&{return_str}&HashIV={HashIV}"
        
        # 將整串字串進行URL encode, 並轉為小寫
        url_encodeStr = urllib.parse.quote_plus(hashStr)
        lower_encodeStr = url_encodeStr.lower()

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
        return "這裡是get頁面"

if __name__=="__main__":
    app.run()
    # app.run(host='0.0.0.0', port=3123, debug=True)