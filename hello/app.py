from flask import Flask,redirect,url_for,jsonify,make_response,request
app = Flask(__name__)


#内部地址跳转
@app.route('/')
def index():
    return redirect(url_for('test1'))


#flask 封装的json处理
@app.route('/test1')
def hi():
    return jsonify(name= 'test1')


#定义响应格式
@app.route('/test2')
def test2():
    response = make_response('<h1>iiii</h1>')
    response.mimetype = 'text/plain'
    return response

#设置cookie（有安全漏洞）
@app.route('/test3')
def test3():
    #获取请求参数
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')  # 从Cookie中获取name值
    return '<h1>Hello, %s</h1>' % name
@app.route('/test3/<name>')
def set_cookie(name):
    response = make_response(redirect(url_for('test3')))
    response.set_cookie('name', name)
    return response


