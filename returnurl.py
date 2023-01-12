from flask import Flask, render_template, request
import json
app = Flask(__name__, template_folder='templates')


@app.route('/')
def home():
    return ('this is ReturnURL')

@app.route('/ResultUrlData', methods=["GET", "POST"])
def ResultUrlData():
    
    data_dict = request.form.to_dict() # type = dict
    json_str = json.dumps(data_dict, indent=4)
    with open("templates/ResultUrlData.html", 'w+', encoding='utf-8') as file:
        file.write(json_str)
   
    return render_template("ResultUrlData.html")
    # return json_str

if __name__=="__main__":
    app.run()