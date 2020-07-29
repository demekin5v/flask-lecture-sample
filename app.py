from flask import Flask,render_template,request,redirect
import sqlite3
app = Flask(__name__)

@app.route('/')
def hello():
    return "Hello World!"

@app.route('/top')
def top():
    return"ここはトップだよ"

@app.route('/hello/<text>')
def  namehello(text):
    return text +"さんこんにちわ"

@app.route('/index')
def index():
    name="sunabaco"
    age = 20
    address="田町"

    return render_template('index.html',user_name = name, user_address = address , user_age = age)

@app.route('/weather')
def  weather():
    py_weather = "曇り"
    address="雨"

    return render_template('weather.html',html_weather = py_weather)

@app.route('/dbtest')
def dbtest():
    #dbに接続する二行
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    #SQLの命令を描く
    c.execute("SELECT name,age,address FROM user WHERE id = 1")
    user_info = c.fetchone()
    #dbの処理終了
    c.close()
    print(user_info)
    return render_template('dbtest.html',db_userinfo = user_info)

#ここからTODOアプリ
@app.route('/add')
def add_get():
    return render_template('add.html')

@app.route('/add',methods = ['post'])
def app_post():
    py_task = request.form.get("task")
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("INSERT INTO task VALUES (null,?)",(py_task,))
    conn.commit()
    c.close()
    return redirect('/list')

@app.route('/list')
def task_list():
    conn = sqlite3.connect('flasktest.db')
    c = conn.cursor()
    c.execute("SELECT id ,task FROM task")
    task_list_py = []
    for row in c.fetchall():
        task_list_py.append({"id":row[0],"task":row[1]})
    c.close()
    print(task_list_py)
    return render_template("tasklist.html",task_list = task_list_py)

@app.errorhandler(404)
def notfound(code):
    return "404エラーだお(´;ω;｀)"

if __name__ == '__main__':
    app.run(debug=True)