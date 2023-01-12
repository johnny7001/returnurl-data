from flask import Flask, render_template, request
import json
app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return ('this is ReturnURL123')

@app.route('/ResultUrlData', methods=["GET", "POST"])
def ResultUrlData():
    # 判斷接收的結果
    if request.method == "POST":
        data_dict = request.form.to_dict() # type = dict
        print(data_dict)
        json_str = json.dumps(data_dict, indent=4)
        with open("templates/ResultUrlData.html", 'w+', encoding='utf-8') as file:
            file.write("1|OK")
        
        # return render_template("ResultUrlData.html")
        return "1|OK"
    elif request.method == "GET":
        with open("templates/ResultUrlData.html", 'w+', encoding='utf-8') as file:
            file.write("1|OK")
        return "這裡是get頁面"


if __name__=="__main__":
    app.run()