# -*- coding: utf-8 -*-
from flask.app import Flask
from watchlist.forms import MovieForm, UserForm
from watchlist import app, db
from flask import render_template, redirect, request, flash, url_for
from flask_login import login_user, login_required, logout_user
from watchlist.models import User, Movie


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':  # 验证 POST 请求
        # if request.method == 'POST' and form.validate():  # 验证 POST 请求
        username = request.form['username']
        password = request.form['password']
        if not username or not password:
            flash('Invalid input.')
            return redirect(url_for('login'))
        user = User.query.first()
        # 验证用户名和密码是否一致
        if username == user.username and user.validate_password(password):
            login_user(user)  # 登入用户
            flash('Login success.')
            return redirect(url_for('index'))  # 重定向到主页
        flash('Invalid username or password.')  # 如果验证失败，显示错误消息
        return redirect(url_for('login'))  # 重定向回登录页面
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required  # 用于视图保护，
def logout():
    """登出用户"""
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页


@app.route('/settings', methods=['GET', 'POST'])
@login_required  # 视图保护
def settings():
    form = UserForm()
    if request.method == 'POST':  # 验证 POST 请求
        # if request.method == 'POST' and form.validate():  # 验证 POST 请求
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        # current_user.name = name
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        User.query.first().name = name
        # User.query.first().name = current_user.name
        db.session.commit()
        flash('Settings updated.')
        # return redirect(url_for('index'))  # 重定向到首页
    return render_template('settings.html', form=form)


def only_number(numStr):
    isNatural = True
    for n in numStr:
        if n not in '0123456789':
            isNatural = False
            break
    return isNatural


@app.route('/', methods=['GET', 'POST'])
def index():
    form = MovieForm()
    if request.method == 'POST':  # 验证 POST 请求
        # if request.method == 'POST' and form.validate():  # 验证 POST 请求
        # 添加新条目，用户保护
        # if not current_user.is_authenticated:  # 如果当前用户未认证
        #     flash(login_manager.login_massage)  # 传入登录提示
        #     return redirect(url_for('login'))  # 重定向到登录页面
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) != 4 or len(title) > 60 or not only_number(year):
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('index.html', movies=movies, form=form)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    form = MovieForm()
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 验证 POST 请求
        # if request.method == 'POST' and form.validate():  # 验证 POST 请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(title) > 60 or not only_number(year):
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie, form=form)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
