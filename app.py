from flask import Flask,redirect,url_for,render_template,request

app = Flask(__name__)

@app.route('/',methods=['GET','POST'])
def index():
    return render_template('index.html')

@app.route("/cadastrar")
def cadastrar():
    return ""

@app.route("/login")
def login():
    return ""


if __name__ == '__main__':
    app.run(debug=True)