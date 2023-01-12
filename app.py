from flask import Flask, render_template, request
import json
app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return ('this is ReturnURL')

@app.route('/ResultUrlData', methods=["GET", "POST"])
def ResultUrlData():
    data_dict = request.form.to_dict() # type = dict
    with open("templates/ResultUrlData.html", 'w+', encoding='utf-8') as file:
        json_str = json.dumps(data_dict, indent=4)
        file.write(json_str)
    print(data_dict)
   
    return render_template("ResultUrlData.html")

if __name__=="__main__":
    app.run()