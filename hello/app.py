from flask import Flask,request
app = Flask(__name__)

@app.route('/')
def index():
    name = request.args.get('name','Flask')
    return '<h1>hello, %s</h1>' %name
