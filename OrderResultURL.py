from flask import Flask, render_template, request
import json
app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return ('this is OrderResultUrl')

@app.route('/OrderResultUrlData', methods=["GET", "POST"])
def OrderResultUrlData():

    data_dict = request.form.to_dict() # type = dict
    # 將接收到的訊息寫到html檔案, 方便查看
    with open("templates/OrderResultUrlData.html", 'w+', encoding='utf-8') as file:
        json_str = json.dumps(data_dict, indent=4)
        file.write(json_str)
    print(data_dict)

    return render_template("OrderResultUrlData.html")

app.run(host='0.0.0.0', port=3124, debug=True)