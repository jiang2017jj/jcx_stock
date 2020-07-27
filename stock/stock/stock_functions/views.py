# -*- coding = utf-8 -*-
from flask import render_template, request
from stock import app
from flask import make_response
from flask import redirect


# 1.基本路由
@app.route('/')
def index():
    pass


# 2.带参数的路由
@app.route('/<username>')
def show_user(username):
    pass


# 3.带参数类型的路由
@app.route('/post/<int:post_id>')
def show_post(post_id):
    pass


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'),404



@app.route('/xxx')
def xxx():
    resp = make_response('响应内容')
    resp = make_response(render_template('xxx.html'))
    #允许调用resp中的属性或方法们以便完成更多的响应行为
    return resp




@app.route('/xxx')
def xxx():
    return redirect('重定向地址')


@app.route('/03-request')
def request_views():
    # print(dir(request))
    # 获取请求方案(协议)
    scheme = request.scheme
    # 获取请求方式
    method = request.method
    # 获取使用get请求方式提交过来的数据
    args = request.args
    # 获取使用post请求方式提交过来的数据
    form = request.form
    # 获取cookies中的相关信息
    cookies = request.cookies
    # 获取请求消息头的相关信息
    headers = request.headers
    # 获取请求资源的路径(不带参数)
    path = request.path
    # 获取请求资源的路径(带参数)
    full_path = request.full_path
    # 获取请求路径
    url = request.url
    # 获取请求源地址
    referer = request.headers.get('Referer','/')
    return render_template('03-request.html',params=locals())

@app.route('/06-form',methods=['POST','GET'],strict_slashes=False)
def form06_views():
    if request.method == 'GET':
        return render_template('06-form.html')
    else:
        uname = request.form['uname']
        upwd = request.form['upwd']
        uemail = request.form['uemail']
        tname = request.form['tname']

        print(uname,upwd,uemail,tname)
        return "Post OK"