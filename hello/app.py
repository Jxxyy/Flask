from flask import Flask,redirect,url_for,jsonify,make_response,request,session,render_template
from urllib.parse import urlparse,urljoin
app = Flask(__name__)
app.secret_key='abc'


#内部地址跳转  url_for 指向的是方法 不是路由
'''
@app.route('/')
def index():
    return redirect(url_for('test2'))
'''

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

#模拟登陆
@app.route('/login')
def login():
    session['logged_in'] = True # 写入session
    return redirect(url_for('hello'))


@app.route('/hello')
def hello():
    name = request.args.get('name')
    if name is None:
        name = request.cookies.get('name', 'Human')
        response = '<h1>Hello, %s!</h1>' % name
# 根据用户认证状态返回不同的内容
    if 'logged_in' in session:
        response += '[Authenticated]'
    else:
        response += '[Not Authenticated]'
    return response

#模拟登出
@app.route('/logout')
def logout():
    if 'logged_in' in session:
        session.pop('logged_in')
    return redirect(url_for('hello'))


#request.full_path获取当前页面的相对路径，在do_someting之后重定向回去上一个页面，场景：登录之后返回之前访问的页面
#request.referrer 获取请求来源
@app.route('/foo')
def foo():
    return '<h1>Foo page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something',next=request.full_path)
@app.route('/bar')
def bar():
    return '<h1>Bar page</h1><a href="%s">Do something and redirect</a>' % url_for('do_something',next=request.full_path)
@app.route('/do_something')
def do_something():
# do something
    return redirect_back()
#封装重定向函数
def redirect_back(default='hello', **kwargs):
    for target in request.args.get('next'), request.referrer:
        if not target:
            continue
        if is_safe_url(target):
            return redirect(target)
    return redirect(url_for(default, **kwargs))
#封装，验证重定向的地址是否安全（内部地址）
def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and ref_url.netloc == test_url.netloc


user = {
'username': 'Grey Li',
'bio': 'A boy who loves movies and music.',
}
movies = [
{'name': 'My Neighbor Totoro', 'year': '1988'},
{'name': 'Three Colours trilogy', 'year': '1993'},
{'name': 'Forrest Gump', 'year': '1994'},
{'name': 'Perfect Blue', 'year': '1997'},
{'name': 'The Matrix', 'year': '1999'},
{'name': 'Memento', 'year': '2000'},
{'name': 'The Bucket list', 'year': '2007'},
{'name': 'Black Swan', 'year': '2010'},
{'name': 'Gone Girl', 'year': '2014'}]
@app.route('/watchlist')
def watchlist():
    return render_template('watchlist.html', user=user, movies=movies,test='&#9835;')

@app.route('/watchlist3')
def watchlist2():
    return render_template('watchlist2.html', user=user, movies=movies,test='&#9835;')


#添加全局变量和全局函数
def bar():
    return 'I am bar.'
foo = 'I am foo.'
app.jinja_env.globals['bar'] = bar
app.jinja_env.globals['foo'] = foo

#测试器用来测试变量和表达式，返回布尔类型，例如判断变量是否为数字
def baz(n):
    if n == 'baz':
        return True
    return False
app.jinja_env.tests['baz'] = baz


@app.route('/')
def index():
    return render_template('index.html')


180