from flask import Flask, render_template, url_for, flash, redirect
import joblib
from flask import request
import numpy as np

app = Flask(__name__, template_folder='templates')

@app.route('/home')
def home():
    return render_template("home")
@app.route('/info.html')
def info():
    return render_template("Liver-info.html")
@app.route('/contact.html')
def contact():
    return render_template("contact.html")

@app.route('/')
@app.route("/liver")
def cancer():
    return render_template("liver.html")

def ValuePredictor(to_predict_list, size):
    to_predict = np.array(to_predict_list).reshape(1,size)
    if(size==7):
        loaded_model = joblib.load(r'liver_model.pkl')
        result = loaded_model.predict(to_predict)
    return result[0]

@app.route('/predict', methods = ["POST"])
def predict():
    if request.method == "POST":
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
         #liver
        if(len(to_predict_list)==7):
            result = ValuePredictor(to_predict_list,7)
    print("predicting...")
    if(int(result)==1):
        prediction = "Sorry, you have chances of getting the Liver disease. Please consult the doctor immediately!!!!"
        print("Prediction done")
    else:
        prediction = "No need to fear. You have no dangerous symptoms of the disease:)"
        print("Prediction done")
    return(render_template("result.html", prediction_text=prediction))       

if __name__ == "__main__":
    app.run(debug=True)
    from waitress import serve
    serve(app, host="0.0.0.0", port=8087)
