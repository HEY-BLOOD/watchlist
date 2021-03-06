[toc]

## 简介

这是一篇 Flask 的笔记，是我在学习 [Flask 入门教程](http://helloflask.com/tutorial/) 时所写下的，为的是当我需要用到某个知识点却又想不起来时能够在这里快速的找到解决方案。

## 第 1 章：准备工作

### 安装编辑器和浏览器
[Visual Studio Code](https://code.visualstudio.com/) 和 [Microsoft Edge Insider](https://www.microsoftedgeinsider.com/zh-cn)

### 使用命令行

因为是 Windows 系统，所以我使用 PowerShell  任务自动化和配置管理框架。

创建工作目录 `mkdir watchlist`

### 使用 Git
1. 用户信息：

    ```powershell
    git config --global user.name "blood"
    git config --global user.email "blood1740@aliyun.com"
    ```

2. 初始化 Git 仓库：

    ```powershell
    git init
    ```

3. 忽略文件规则：

    项目根目录新建文件 `touch .gitignore`

4. 写入常见的可忽略文件规则：

    ```
    *.pyc
    *~
    __pycache__
    .DS_Store
    ```

### 将程序托管到 GitHub
1. 设置 SSH 密钥：

   ```powershell
   ssh-keygen
   ```

   一路按下 Enter 采用默认值，最后会在用户根目录创建一个 .ssh 文件夹，其中包含两个文件，id_rsa 和 id_rsa.pub，前者是私钥，不能泄露出去，后者是公钥，用于认证身份，就是我们要保存到 GitHub 上的密钥值。再次使用前面提到的命令获得文件内容：

   ```powershell
   $ cat ~/.ssh/id_rsa.pub
   ssh-rsa AAAAB3Nza...省略 N 个字符...3aph book@greyli
   ```

   选中并复制输出的内容，访问 GitHub 的 SSH 设置页面（导航栏头像 - Settings -SSH and GPG keys），点击 New SSH key 按钮，将复制的内容粘贴到 Key 输入框里，再填一个标题，比如“My PC”，最后点击“Add SSH key”按钮保存。


2. 创建远程仓库：

   访问新建仓库页面（导航栏“+” - New repository），在“Repository name”处填写仓库名称，这里填“watchlist”即可，接着选择仓库类型（公开或私有）等选项，最后点击“Create repository”按钮创建仓库。

   因为我们已经提前创建了本地仓库，所以需要指定仓库的远程仓库地址（如果还没有创建，则可以直接将远程仓库克隆到本地）：

   ```powershell
   git remote add origin git@github.com:HEY-BLOOD/watchlist.git # 注意更换地址中的用户名
   ```

   这会为本地仓库关联一个名为“origin”的远程仓库。

### 创建虚拟环境

我的电脑上安装的是 [Miniconda](https://docs.conda.io/en/latest/miniconda.html) 因此使用 conda 创建虚拟环境：

```powershell
conda create -n myenv python=3.6 flask
```

激活虚拟环境：

```powershell
conda activate myenv
```

退出虚拟环境：

```powershell
conda deactivate
```

### 本章小结

项目的准备已经完成，使用 `git status` 命令可以查看当前仓库的文件变动状态：

```powershell
(myenv) PS E:\PyCode\watchlist> git status
On branch master

No commits yet

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        .gitignore
        README.md

nothing added to commit but untracked files present (use "git add" to track)
```

提交进 Git 仓库，并推送到在 GitHub 上创建的远程仓库：

```powershell
git add . # 暂存所有更改
git commit -m "I'm ready!"
git push -u origin master
```

最后一行命令添加了 -u 参数，会将推送的目标仓库和分支设为默认值，后续的推送直接 `git push` 命令即可。



## 第 2 章：Hello, Flask!

### 主页

主页的 URL 一般就是根地址，即 `/` 。

在项目根目录新建 app.py 文件：程序主页

```python
from flask import Flask
app = Flask(__name__)

@app.route('/')
def hello():
	return 'Welcome to My Watchlist!'
```

在命令行窗口执行 flask run 命令启动程序（按下 Control + C 可以退出）

```powershell
(myenv) PS E:\PyCode\watchlist> flask run
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
```

打开浏览器，访问 http://localhost:5000 即可访问程序主页，执行 flask run 命令时，Flask 会使用内置的开发服务器来运行程序。这个服务器默认监听本机的 5000 端口，可以在地址栏输入 http://127.0.0.1:5000 访问程序。

> 注意 内置的开发服务器只能用于开发时使用，部署上线时要用性能更好的服务器，这在最后一章学习。

### 解剖时间

下面分解这个 Flask 程序，了解它的基本构成。

首先我们从 flask 包导入 Flask 类，通过实例化这个类，创建一个程序对象 app ：

```python
from flask import Flask
app = Flask(__name__)
```

注册一个处理函数，这个函数是处理某个请求的处理函数，Flask 官方把它叫做视图函数（view funciton），使用 `app.route()` 装饰器来为这个函数绑定对应的 URL，当用户在浏览器访问这个 URL 的时候，就会触发这个函数，获取返回值，并把返回值显示到浏览器窗口：

```python
@app.route('/')
def hello():
    return 'Welcome to My Watchlist!'
```

`app.route()` 装饰器的第一个参数是 URL 规则字符串，其中 `/` 代表根地址，也就是  http://127.0.0.1:5000/ 。

### 程序发现机制

如果把程序 app.py 保存成其他的名字，比如 hello.py，接着执行 flask run 命令会返回一个错误提示。因为 Flask 默认会假设你把程序存储在名为 app.py 或 wsgi.py 的文件中。如果你使用了其他名称，就要设置系统环境变量 FLASK_APP 来告诉 Flask 你要启动哪个程序。

Flask 通过读取这个环境变量值对应的模块寻找要运行的程序实例，你可以把它设置成下面这些值：

* 模块名
* Python 导入路径
* 文件目录路径

**管理环境变量**

启动 Flask 程序时通常要和两个环境变量打交道： `FLASK_APP` 和 `FLASK_ENV` 。

因为程序程序现在名字是 app.py，暂时不需要设置 `FLASK_APP `； `FLASK_ENV` 用来设置程序运行的环境，默认为 production 。在开发时，需要开启调试模式（debug mode）。调试模式可以通过将系统环境变量 `FLASK_ENV` 设为 development 来开启。调试模式开启后，当程序出错，浏览器页面上会显示错误信息；代码出现变动后，程序会自动重载。

**管理系统环境变量的 python-dotenv：**

```powershell
(env) $ pip install python-dotenv
```

当 python-dotenv 安装后，当 python-dotenv 安装后，Flask 会从项目根目录的 .flaskenv 和 .env 文件读取环
境变量并设置。

**创建这两个文件：**

```powershell
New-Item .env
New-Item .flaskenv
```

把文件名 .env 添加到 .gitignore 文件，让 Git 忽略它：

```powershell
*.pyc
*~
__pycache__
.DS_Store
.env
```

**更改 `.flaskenv` 开启调试模式：**

```powershell
"FLASK_ENV=development" >> .\.flaskenv
```

> 其实在集成开发环境中有更好的解决方案，比如 PyCharm 或 VS Code 等。

### 实验时间

1. **修改视图函数返回值**

   首先，你可以自由修改视图函数的返回值，比如：

   ```python
   @app.route('/')
   def hello():
   	return u'欢迎来到我的 Watchlist！'
   ```

   返回值作为响应的主体，默认会被浏览器作为 HTML 格式解析，所以可以添加 HTML 元素标记：

   ```python
   @app.route('/')
   def hello():
       return '<h1>Hello Totoro!</h1><img src="http://helloflask.com/totoro.gif">'
   ```

   保存修改后，只需要在浏览器里刷新页面，你就会看到页面上的内容也会随之变化。

2. **修改 URL 规则**

   **另外，也可以自由修改传入 `app.route()` 装饰器里的 URL 规则字符串，但要注意以斜线 `/` 作为开头。比如：**

   ```python
   @app.route('/home')
   def hello():
   	return 'Welcome to My Watchlist!'
   ```

   保存修改，这时刷新浏览器，则会看到一个 404 错误提示，因为视图函数的 URL 改成了 `/home` ，而我们刷新后访问的地址仍然是旧的 `/` 。把访问地址改成 http://localhost:5000/home，就会看到正确返回值。

   **一个视图函数也可以绑定多个 URL，这通过附加多个装饰器实现，比如：**

   ```python
   @app.route('/')
   @app.route('/index')
   @app.route('/home')
   def hello():
       return u'欢迎来到我的 Watchlist！'
   ```

   无论是访问 http://localhost:5000/、http://localhost:5000/home 还是 http://localhost:5000/index 都可以看到返回值。

   **所以把传入 `app.route()` 装饰器的参数称为 URL 规则，因为可以在 URL 里定义变量部分，比如：**

   ```python
   @app.route('/user/<name>')
   def user_page(name):
       return 'User: %s' % name
   ```

   无论是访问 http://localhost:5000/user/12a、http://localhost:5000/user/HEY-BLOOD 还是 `http://localhost:5000/user/哈哈哈` 都会触发该函数，通过这种方式可以在视图函数里获取到这个变量值。

3. **修改视图函数名？**

   视图函数的名字是自由定义的，和 URL 规则无关。

   除此之外，还有一个重要作用：作为代表某个路由的端点 (endpoint)，同时用来生成 URL。为了避免手写，Flask 提供了一个 `url_for` 函数来生成 URL，它接受的第一个参数就是端点值，默认为视图函数名称：

   ```python
   from flask import url_for
   
   @app.route('/test')
   def test_url_for():
       # 下面是一些调用示例（请在命令行窗口查看输出的 URL）：
       print(url_for('hello'))  # 输出：/home，离视图函数最近的 装饰器
       # 注意下面两个调用是如何生成包含 URL 变量的 URL 的
       print(url_for('user_page', name='greyli'))  # 输出：/user/greyli
       print(url_for('user_page', name='peter'))  # 输出：/user/peter
       print(url_for('test_url_for'))  # 输出：/test
       # 下面这个调用传入了多余的关键字参数，它们会被作为查询字符串附加到 URL 后面。
       print(url_for('test_url_for', num=2))  # 输出：/test?num=2
       return 'Test page'
   ```

   

### 本章小结

这一章我们为程序编写了主页，同时学习了 Flask 视图函数的基本编写方式。结束前，让我们提交代码：

```powershell
$ git add .
$ git commit -m "Add minimal home page"
$ git push
```

### 进阶提示

如果你使用 Python 2.7，为了使程序正常工作，需要在脚本首行添加编码声明 `# -*- coding: utf-8-*-` ，并在包含中文的字符串前面添加 u 前缀。这在 Python 3 中并不需要。

对于 URL 变量，Flask 还支持在 URL 规则字符串里对变量设置处理器，对变量进行预处理。比如 `/user/<int:number>` 会将 URL 中的 number 部分处理成整型，同时这个变量值接收传入数字。

因为 Flask 的上下文机制，有一些变量和函数（比如 url_for 函数）只能在特定的情况下才能正确执行，比如视图函数内。我们先暂时不用纠结，后面再慢慢了解。

名字以 . 开头的文件默认会被隐藏，执行 ls 命令时会看不到它们，这时你可以使用 `ls *` 命令来列出所有文件。



## 第 3 章：模板

页面需要在用户访问时根据程序逻辑动态生成。访问一个地址通常会返回一个包含各类信息的 HTML 页面。包含变量和运算逻辑的 HTML 或其他格式的文本叫做模板，这些变量替换和逻辑计算工作的过程被称为渲染，Flask 通过模板渲染引擎——Jinja2 来完成。

按照默认的设置，Flask 会从程序实例所在模块同级目录的 templates 文件夹中寻找模板，所以在程序 `app.py` 的同级目录 (项目根目录) 新建 templates 文件夹：

```powershell
mkdir directory
```

### 模板基本语法

在社交网站上，每个人都有一个主页，借助 Jinja2 就可以写出一个通用的模板，例如：

```jinja2
<h1>{{ username }}的个人主页</h1>
{% if bio %}
	<p>{{ bio }}</p> {# 这里的缩进只是为了可读性，不是必须的 #}
{% else %}
	<p>自我介绍为空。</p>
{% endif %} {# 大部分 Jinja 语句都需要声明关闭 #}
```

Jinja2 的语法和 Python 大致相同，在模板里，需要添加特定的定界符将 Jinja2 语句和变量标记出来。

模板中使用的变量需要在渲染的时候传递进去，下面是三种常用的定界符：

* {{ ... }} 用来标记变量。
* {% ... %} 用来标记语句，比如 if 语句，for 语句等。
* {# ... #} 用来写注释。

### 编写主页模板

在 templates 目录下创建一个 index.html 作为主页模板。主页需显示电影条目列表和个人信息，代码如下：

```jinja2
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>{{ name }}'s Watchlist</title>
</head>

<body>
    <h2>{{ name }}'s Watchlist</h2>
    {# 使用 length 过滤器获取 movies 变量的长度 #}
    <p>{{ movies|length }} Titles</p>
    <ul>
        {% for movie in movies %} {# 迭代 movies 变量 #}
        <li>{{ movie.title }} - {{ movie.year }}</li> {# 等同于 movie['title'] #}
        {% endfor %} {# 使用 endfor 标签结束 for 语句 #}
    </ul>
    <footer>
        <small>&copy; 2018 <a href="https://github.com/HEY-BLOOD/watchlist">BLOOD's Watchlist</a></small>
    </footer>
</body>

</html>
```

为了方便对变量进行处理，Jinja2 提供了一些过滤器，语法形式如下：

```jinja2
{{ 变量|过滤器 }}
```

左侧是变量，右侧是过滤器名。比如 `index.html` 模板中使用 `length` 过滤器来获取 `movies` 的长度，类似 Python 里的 `len()` 函数。

> 提示 访问 http://jinja.pocoo.org/docs/2.10/templates/#list-of-builtin-filters 查看所有可用的过滤器。

### 准备虚拟数据

为了模拟页面渲染，需要先创建一些虚拟数据，用来填充页面内容，在 app.py 中定义：

```python
name = 'BLOOD'
movies = [
{'title': 'My Neighbor Totoro', 'year': '1988'},
{'title': 'Dead Poets Society', 'year': '1989'},
{'title': 'A Perfect World', 'year': '1993'},
{'title': 'Leon', 'year': '1994'},
{'title': 'Mahjong', 'year': '1996'},
{'title': 'Swallowtail Butterfly', 'year': '1996'},
{'title': 'King of Comedy', 'year': '1999'},
{'title': 'Devils on the Doorstep', 'year': '1999'},
{'title': 'WALL-E', 'year': '2008'},
{'title': 'The Pork of Music', 'year': '2012'},
]
```

### 渲染主页模板

使用 flask 模块中的 `render_template()` 函数可以把模板渲染出来，必须传入的参数为模板文件名（相对于 templates 根目录的文件路径），这里即 'index.html' 。为了让模板正确渲染，我们还要把模板内部使用的变量通过关键字参数传入这个函数，如下所示：
app.py：返回渲染好的模板作为响应

```python
from flask import Flask, render_template

# ...

@app.route('/')
def index():
	return render_template('index.html', name=name, movies=movies)
```

为了更好的表示这个视图函数的作用，我们把原来的函数名 `hello` 改为 `index` ，意思是“索引”，即主页。

这里传入模板的 `name` 是字符串， `movies` 是列表，但能够在模板里使用的不只这两种 Python 数据结构，你也可以传入元组、字典、函数等。

`render_template()` 函数在调用时会识别并执行 index.html 里所有的 Jinja2 语句，返回渲染好的模板内容。

现在访问 http://localhost:5000/ 看到的程序主页如下图所示：


<h2>BLOOD's Watchlist</h2>
<p>10 Titles</p>
<ul>
<li>My Neighbor Totoro - 1988</li> 
<li>Dead Poets Society - 1989</li> 
<li>A Perfect World - 1993</li> 
<li>Leon - 1994</li>  
<li>Mahjong - 1996</li>    
<li>Swallowtail Butterfly - 1996</li> 
<li>King of Comedy - 1999</li>
<li>Devils on the Doorstep - 1999</li> 
<li>WALL-E - 2008</li> 
<li>The Pork of Music - 2012</li> 
</ul>
<footer>
    <small>&copy; 2020 <a href="https://github.com/HEY-BLOOD/watchlist">BLOOD's Watchlist</a></small>
</footer>

### 本章小结

这一章编写了一个简单的主页。结束前，提交代码：

```powershell
$ git add .
$ git commit -m "Add index page"
$ git push
```

### 进阶提示

使用 [Faker](https://github.com/joke2k/faker) 可以实现自动生成虚拟数据，它支持丰富的数据类型，比如时间、人名、地名、随机字符等等……

除了过滤器，Jinja2 还在模板中提供了一些测试器、全局函数可以使用；以及更丰富的控制结构支持。
更多内容则可以访问 [Jinja2 文档](https://jinja.palletsprojects.com/en/2.11.x/templates/) 学习。



## 第 4 章：静态文件

静态文件（static files）和我们的模板概念相反，指的是内容不需要动态生成的文件。比如图片、CSS 文件和 JavaScript 脚本等。

在 Flask 中，我们需要创建一个 static 文件夹来保存静态文件，它应该和程序模块、templates 文件夹在同一目录层级，所以我们在项目根目录创建它：

```powershell
mkdir static
```

### 生成静态文件 URL

在 HTML 文件里，引入这些静态文件需要给出资源所在的 URL。为了更加灵活，这些文件的 URL 可以通过 Flask 提供的 `url_for()` 函数来生成。

对于静态文件，需要传入的端点值是static ，同时使用 filename 参数来传入相对于 static 文件夹的文件路径。

假如在 static 文件夹的根目录下面放了一个 foo.jpg 文件，下面的调用可以获取它的 URL：

```jinja2
<img src="{{ url_for('static', filename='foo.jpg') }}">
```

花括号部分的调用会返回 `/static/foo.jpg` 。

> 提示 在 Python 脚本里， `url_for()` 函数需要从 flask 包中导入，而在模板中则可以直接使用，因为 Flask 把一些常用的函数和对象添加到了模板上下文（环境）里。

### 添加 Favicon

Favicon（favourite icon） 是显示在标签页和书签栏的网站头像。你需要准备一个ICO、PNG 或 GIF 格式的图片，大小一般为 16×16、32×32、48×48 或 64×64 像素 [ICO图标在线生成](http://www.ico51.cn/)。把这个图片放到 static 目录下，然后像下面这样在 HTML 模板里引入它：

templates/index.html：引入 Favicon

```jinja2
<head>
	...
	<link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
</head>
```

保存后刷新页面，即可在浏览器标签页上看到这个图片。

### 添加图片

为了让页面不那么单调，来添加两个图片：一个是显示在页面标题旁边的头像，另一个是显示在页面底部的龙猫动图。我们在 static 目录下面创建一个子文件夹 images，把这两个图片都放到这个文件夹里：

```powershell
$ cd static
$ mkdir images
```

创建子文件夹并不是必须的，这里只是为了更好的组织同类文件。同样的，如果你
有多个 CSS 文件，也可以创建一个 css 文件夹来组织他们。下面我们在页面模板
中添加这两个图片，注意填写正确的文件路径：

templates/index.html：添加图片

```jinja2
<h2>
	<img alt="Avatar" src="{{ url_for('static', filename='images/avatar.png') }}">{{ name }}'s Watchlist
</h2>
...
<img alt="Walking Totoro" src="{{ url_for('static', filename='images/totoro.gif') }}">
<footer>...</footer>
```

### 添加 CSS

虽然添加了图片，但页面还是非常简陋，因为我们还没有添加 CSS 定义。下面在static 目录下创建一个 CSS 文件 style.css，内容如下：
static/style.css：定义页面样式

```css
/* 页面整体 */
body {
    margin: auto;
    max-width: 580px;
    font-size: 14px;
    font-family: Helvetica, Arial, sans-serif;
}

/* 页脚 */
footer {
    color: #888;
    margin-top: 15px;
    text-align: center;
    padding: 10px;
}

/* 头像 */
.avatar {
    width: 40px;
}

/* 电影列表 */
.movie-list {
    list-style-type: none;
    padding: 0;
    margin-bottom: 10px;
    box-shadow: 0 2px 5px 0 rgba(0, 0, 0, 0.16), 0 2px 10px 0 rgba(0, 0, 0, 0.12);
}

.movie-list li {
    padding: 12px 24px;
    border-bottom: 1px solid #ddd;
}

.movie-list li:last-child {
    border-bottom: none;
}

.movie-list li:hover {
    background-color: #f8f9fa;
}

/* 龙猫图片 */
.totoro {
    display: block;
    margin: 0 auto;
    height: 100px;
}
```

接着在页面的 <head> 标签内引入这个 CSS 文件：

```jinja2
<head>
	...
	<link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>
```

最后要为对应的元素设置 class 属性值，以便和对应的 CSS 定义关联起来：
templates/index.html：添加 class 属性

```jinja2
<h2>
	<img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">{{ name }}'s Watchlist
</h2>
...
<ul class="movie-list">
    ...
</ul>
<img alt="Walking Totoro" class="totoro" src="{{ url_for('static', filename='images/totoro.gif') }}">
```

### 本章小结

主页现在基本成型了，接下来会慢慢完成程序的功能。结束前，提交代码：

```powershell
$ git add .
$ git commit -m "Add static files"
$ git push
```

### 进阶提示

* 如果对 CSS 很头疼，可以借助前端框架来完善页面样式，比如 [Bootstrap](https://getbootstrap.com/)、[Semantic-UI](http://semantic-ui.com/)、[Foundation](https://get.foundation/) 等。它们提供了大量的 CSS 定义和动态效果，使用起来非常简单。
* 扩展 Bootstrap-Flask 可以简化在 Flask 项目里使用 [Bootstrap 4](https://github.com/greyli/bootstrap-flask) 的步骤。



## 第 5 章：数据库

大部分程序都需要保存数据，所以不可避免要使用数据库。用来操作数据库的数据库管理系统（DBMS）有很多选择，对于不同类型的程序，不同的使用场景，都会有不同的选择。在这个项目中，选择了属于关系型数据库管理系统（RDBMS）的 SQLite，它基于文件，不需要单独启动数据库服务器，适合在开发时使用，或是在数据库操作简单、访问量低的程序中使用。

### 使用 SQLAlchemy 操作数据库

为了简化数据库操作，我们将使用 [SQLAlchemy]( https://www.sqlalchemy.org/ ) 一个 Python 数据库工具（ORM，即对象关系映射）。借助 SQLAlchemy，你可以通过定义 Python 类来表示数据库里的一张表（类属性表示表中的字段 / 列），通过对这个类进行各种操作来代替写 SQL 语句。这个类我们称之为模型类，类中的属性我们将称之为字段。

Flask 有大量的第三方扩展，这些扩展可以简化和第三方库的集成工作。下面使用一个叫做 Flask-SQLAlchemy 的官方扩展来集成 SQLAlchemy。首先安装它：

```powershell
pip install flask-sqlalchemy
```

大部分扩展都需要执行一个“初始化”操作。需要导入扩展类，实例化并传入 Flask 程序实例：

```python
from flask_sqlalchemy import SQLAlchemy # 导入扩展类
app = Flask(__name__)
db = SQLAlchemy(app) # 初始化扩展，传入程序实例 app
```

### 设置数据库 URI

为了设置 Flask、扩展或是我们程序本身的一些行为，我们需要设置和定义一些配置变量。Flask 提供了一个统一的接口来写入和获取这些配置变量： `Flask.config` 字典。配置变量的名称必须使用大写，写入配置的语句一般会放到扩展类实例化语句之前。
下面写入了一个 `SQLALCHEMY_DATABASE_URI` 变量来告诉 SQLAlchemy 数据库连接地址：

```python
import os
# ...
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////' + os.path.join(app.root_path, 'data.db')
```

> 注意 这个配置变量的最后一个单词是 URI，而不是 URL。

对于这个变量值，不同的 DBMS 有不同的格式，对于 SQLite 来说，这个值的格式如下：

```python
'sqlite:////数据库文件的绝对地址'
```

数据库文件一般放到项目根目录即可， `app.root_path` 返回程序实例所在模块的路径（目前来说，即项目根目录），使用它来构建文件路径。数据库文件的名称和后缀可以自由定义，一般使用 .db、.sqlite 和 .sqlite3 。

另外，如果使用 Windows 系统，上面的 URI 前缀部分需要写入三个斜线（即 `'sqlite:///数据库文件路径'` ），app.py：数据库配置

```python
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
import os
import sys

app = Flask(__name__)

WIN = sys.platform.startswith('win')
if WIN:  # Windows 环境下，三个斜杠
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型的修改监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
```

> 提示 
>
> 可以访问 [Flask 文档的配置页面](https://flask.palletsprojects.com/en/1.1.x/config/) 查看 Flask 内置的配置变量；同样的，在 [Flask-SQLAlchemy 文档的配置页面](https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/) 可以看到 Flask-SQLAlchemy 提供的配置变量。

### 创建数据库模型

在 Watchlist 程序里，目前有两类数据要保存：用户信息和电影条目信息。下面创建两个模型类来表示这两张表：
app.py：创建数据库模型

```python
class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))  # 用户名

class Movie(db.Model):  # 表名 movie
    id = db.Coloumn(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
```

模型类的编写有一些限制：

* 模型类要声明继承 `db.Model` 。每一个类属性（字段）要实例化 `db.Column` ，传入的参数为字段的类型，下
  面的表格列出了常用的字段类。

* 在 `db.Column()` 中添加额外的选项（参数）可以对字段进行设置。

  比如， primary_key 设置当前字段是否为主键。除此之外，常用的选项还有nullable （布尔值，是否允许为空值）、 index （布尔值，是否设置索引）、 unique （布尔值，是否允许重复值）、 default （设置默认值）等。

常用的字段类型如下表所示：

|     字段类      |               说明               |
| :-------------: | :------------------------------: |
|   db.Integer    |               整形               |
| db.String(size) |      字符串，size 最大长度       |
|     db.Text     |              长文本              |
|   db.DateTime   | 日期时间型，Python datetime 对象 |
|    db.Float     |              浮点型              |
|   db.Boolean    |              布尔值              |

### 创建数据库表

模型类创建后，还不能对数据库进行操作，因为还没有真实地创建表和数据库文件。
下面在 Python Shell 中创建了它们：

```python
(myenv) PS E:\PyCode\watchlist> flask.exe shell
App: app [production]
Instance: E:\PyCode\watchlist\instance
>>> from app import db
>>> db.create_all()
```

打开文件管理器，会发现项目根目录下出现了新创建的数据库文件 `data.db`。这个文件不需要提交到 Git 仓库，我们在 .gitignore 文件最后添加一行新规则：

```
*.db
```

如果改动了模型类，想重新生成表模式，那么需要先使用  db.drop_all() 删除表，然后重新创建：

```python
>>> db.drop_all()
>>> db.create_all()
```


注意这会一并删除所有数据，如果想在不破坏数据库内的数据的前提下变更表的结构，需要使用数据库迁移工具，比如集成了 [Alembic](https://alembic.sqlalchemy.org/en/latest/) 的 [Flask-Migrate](https://github.com/miguelgrinberg/Flask-Migrate) 扩展。

> 提示 
>
> 打开 Python Shell 使用的是 `flask shell` 命令，而不是 python 。使用这个命令启动的 Python Shell 激活了“程序上下文”，它包含一些特殊变量，这对于某些操作是必须的（比如上面的 db.create_all() 调用）。
>
> 后续的 Python Shell 都会使用这个命令打开。

和 flask shell 类似，可以编写一个自定义命令来自动执行创建数据库表操作：
app.py：自定义命令 `initdb`

```python
import click

# 自定义创建数据库命令
@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the dataabase"""
    if drop:
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.')  # 输出提示信息
```

默认情况下，函数名称就是命令的名字，执行 `flask initdb` 命令就可以创建数据库表：

```powershell
(myenv) PS E:\PyCode\watchlist> flask initdb
```

使用 `--drop` 选项可以删除表后重新创建：

```power
(myenv) PS E:\PyCode\watchlist> flask initdb --drop
```

### 数据库操作 (练习)

在 Python Shell 里，测试一下常见的数据库操作，目的是熟悉 SQLAlchemy 对数据库的操作方式。

#### **创建数据**

下面的操作演示了如何向数据库中添加记录：

```python
>>> from app import db, User, Movie
>>> from app import db, User, Movie # 导入数据库对象、模型类型
>>> 
>>> user = User(name='Blood H') # 新建 User 记录
>>> m1 = Movie(title='Mahjong', year='1996') # 创建 Movie 记录
>>> m2 = Movie(title='Leon', year='1994')
>>> 
>>> db.session.add(user) # 把新创建的记录添加到数据库会话
>>> db.session.add(m1)
>>> db.session.add(m1)
>>> db.session.add(m2)
>>> db.session.commit() # 提交数据库会话，最后调用
```

> 提示 
>
> 在实例化模型类的时候，并没有传入 id 字段（主键），因为 SQLAlchemy 会自动处理这个字段。（自增长）

最后一行 `db.session.commit()` 很重要，只有调用了这一行才会真正把记录提交进数据库，前面的  `db.session.add()` 调用是将改动添加进数据库会话（一个临时区域）中。

#### **读取数据**

通过对模型类的 `query` 属性调用可选的过滤方法和查询方法，我们就可以获取到对应的单个或多个记录（记录以模型类实例的形式表示）。查询语句的格式如下：

```python
<模型类>.query.<过滤方法（可选）>.<查询方法>
```

**常用的过滤方法：**

| 过滤方法    | 说明                                                         |
| ----------- | ------------------------------------------------------------ |
| filter()    | 使用指定的规则过滤记录，返回新产生的查询对象                 |
| filter_by() | 使用指定规则过滤记录（以关键字表达式的形式），返回新产生的查询对象 |
| order_by()  | 根据指定条件对记录进行排序，返回新产生的查询对象             |
| group_by()  | 根据指定条件对记录进行分组，返回新产生的查询对象             |

**常用的查询方法：**

| 查询方法       | 说明                                                         |
| -------------- | ------------------------------------------------------------ |
| all()          | 返回包含所有查询记录的列表                                   |
| first()        | 返回查询的第一条记录，如果未找到，则返回None                 |
| get(id)        | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回None |
| count()        | 返回查询结果的数量                                           |
| first_or_404() | 返回查询的第一条记录，如果未找到，则返回404错误响应          |
| get_or_404(id) | 传入主键值作为参数，返回指定主键值的记录，如果未找到，则返回404错误响应 |
| paginate()     | 返回一个Pagination对象，可以对记录进行分页处理               |

**下面的操作演示了如何从数据库中读取记录，并进行简单的查询：**

```python
>>> from app import User, Movie # 导入模型类
>>> 
>>> ms = Movie.query.all() # 获取所有 Movie 记录
>>> len(ms), ms # Movie 总数 和 列表
(2, [<Movie 1>, <Movie 2>])
>>> User.query.count() # User 总数
1
>>> m = Movie.query.first() # 第一条 Movie
>>> m.title, m.year
('Mahjong', '1996')
>>> m = Movie.query.all()[-1] # 第二条 Movie
>>> m.title, m.year
('Leon', '1994')
>>> 
>>> user = User.query.get(1) # 获取主键值为 1 的User
>>> user.id, user.name
(1, 'Blood H')
>>> m = Movie.query.filter_by(title='Mahjong').first() # 查询第一个 Mahjong 的 Movie
>>> m.id, m.title, m.year
(1, 'Mahjong', '1996')
>>> m = Movie.query.filter(Movie.title=='Mahjong').first()# 同上，使用不同的过滤方法
>>> m.id, m.title, m.year
(1, 'Mahjong', '1996')
```

>  提示 谈到 Movie 模型的时，实际指的是数据库中的 movie 表。表的实际名称是模型类的小写形式（自动生成），如果想自己指定表名，可以在模型类中定义 `__tablename__` 属性。 

对于最基础的 `filter()` 过滤方法，SQLAlchemy 支持丰富的查询操作符，具体可以访问 [文档相关页面](http://docs.sqlalchemy.org/en/latest/core/sqlelement.html#sqlalchemy.sql.operators.ColumnOperators) 查看。除此之外，还有更多的查询方法、过滤方法和数据库函数可以使用，具体可以访问文档的 [Query API](https://docs.sqlalchemy.org/en/latest/orm/query.html) 部分查看。

#### 更新数据

下面的操作更新了 Movie 模型中主键为 2 的记录：
```python
>>> from app import db, Movie # 导入模型类
>>> movie = Movie.query.get(2)
>>> movie.title = 'WALL-E' # 直接对实例属性赋予新的值即可
>>> movie.year = '2008'
>>> db.session.commit() # 提交改动，将更新写入数据库
>>> [(m.id, m.title, m.year) for m in Movie.query.all()]
[(1, 'Mahjong', '1996'), (2, 'WALL-E', '2008')]
```

#### 删除数据

下面的操作删除了 Movie 模型中主键为 1 的记录：
```python
>>> from app import db, Movie # 导入模型类
>>> movie = Movie.query.get(1)
>>> db.session.delete(movie) # 使用 db.session.delete() 方法删除记录，传入模型实例
>>> db.session.commit() # 提交改动，从数据库删除记录
>>> [(m.id, m.title, m.year) for m in Movie.query.all()]
[(2, 'WALL-E', '2008')]
```

### 在程序里操作数据库

经过上面的一番练习，可以在 Watchlist 里进行实际的数据库操作了。

#### 在主页视图读取数据库记录

因为设置了数据库，负责显示主页的 `index` 视图函数可以从数据库里读取真实的数据：

```python
@app.route('/')
# ...
def index():
    user = User.query.first()  # 读取用户
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', user=user.name, movies=movies)
```

在 index 视图中，原来传入模板的 `name` 变量被 `user` 实例取代，模板 `index.html` 中的两处 `name` 变量也要相应的更新为 `user.name` 属性。

```html
<title>{{ user.name }}'s Watchlist</title>

<h2><img ...>&nbsp;{{ user.name }}'s Watchlist</h2>
```

#### 生产虚拟数据

因为有了数据库，可以编写一个命令函数把虚拟数据添加到数据库里。下面是用来生成虚拟数据的命令函数：

app.py：创建自定义命令 forge

```python
import click

@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()  # 创建数据表

    # 全局的两个变量移动到这个函数内
    name = 'Blood H'
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit() # 提交更改
    click.echo('Generate fake data, finished!')
```

现在执行 flask forge 命令就会把所有虚拟数据添加到数据库里：

```powershell
(myenv) PS E:\PyCode\watchlist> flask.exe forge  
Generate fake data, finished!
```

### 本章小结

本章使用 SQLAlchemy 操作数据库，现在提交代码：

```powershell
$ git add .
$ git commit -m "Add database support with Flask-SQLAlchemy"
$ git push
```

### 进阶提示

* 在生产环境，可以更换更合适的 DBMS，因为 SQLAlchemy 支持多种 SQL数据库引擎，通常只需要改动非常少的代码。
* 这个程序只有一个用户，所以没有将 User 表和 Movie 表建立关联。Flask-SQLAlchemy 文档中的 [声明模型](https://flask-sqlalchemy.palletsprojects.com/en/2.x/models/#one-to-many-relationships) 章节可以看到相关内容。
* 阅读 [SQLAlchemy 官方文档和教程](https://docs.sqlalchemy.org/zh/latest/) 详细了解它的用法。注意在这里使用 Flask-SQLAlchemy 来集成它，所以用法和单独使用 SQLAlchemy 有一些不同。作为参考，可以同时阅读 [Flask-SQLAlchemy 官方文档](https://flask-sqlalchemy.palletsprojects.com/en/2.x/) 。



## 第 6 章：模板优化

这一章继续完善模板，利用几个非常实用的模板编写技巧，为下一章实现创建、编辑电影条目打下基础。

### 自定义错误页面

首先要为 Watchlist 编写一个错误页面。目前的程序中，如果你访问一个不存在的 URL，比如 `/hello`，Flask 会自动返回一个 404 错误响应。默认的错误页面非常简陋，如下所示：

<h1>Not Found</h1>
<p>The requested URL was not found on the server. If you entered the URL manually please check your spelling and try again.</p>
在 Flask 程序中自定义错误页面非常简单，先编写一个 404 错误页面模板，如下所示：
templates/404.html：404 错误页面模板

```html
<!DOCTYPE html>
<html lang="en">

<head>
    <meta charset="utf-8">
    <title>{{ user.name }}'s Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
</head>

<body>
    <h2>
        <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
        {{ user.name }}'s Watchlist
    </h2>
    <ul class="movie-list">
        <li>
            Page Not Found - 404
            <span class="float-right">
                <a href="{{ url_for('index') }}">Go Home</a>
            </span>
        </li>
    </ul>
    <footer>
        <small>&copy; 2020 <a href="https://github.com/HEY-BLOOD/watchlist">Watchlist</a></small>
    </footer>
</body>

</html>
```

接着使用 `app.errorhandler()` 装饰器注册一个错误处理函数 `page_not_found`，它的作用和视图函数类似，当 404 错误发生时，这个函数会被触发，返回值会作为响应主体返回给客户端：

app.py：404 错误处理函数

```python
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    user = User.query.fisrt()
    response = render_template('404.html', user=user)
    return response, 404  # 返回响应和状态码
```

> 提示 
>
> 与之前编写的视图函数相比，这个函数返回了状态码作为第二个参数，普通的视图函数之所以不用写出状态码，是因为默认会使用 200 状态码，表示成功。

这个视图返回渲染好的错误模板，因为模板中使用了 user 变量，这里也要 User 类型的对象。现在访问一个不存在的 URL，会显示自定义的错误页面，访问  http://127.0.0.1:5000/PYFY77ZNA8KYV0i1 试试。

编写完这部分代码后，会发现两个问题：

* 错误页面和主页都需要使用 user 变量，所以在对应的处理函数里都要查询数据库并传入 user 变量。因为每一个页面都需要获取用户名显示在页面顶部，如果有更多的页面，那么每一个对应的视图函数都要重复传入这个变量。

* 错误页面模板和主页模板有大量重复的代码，比如 <head> 标签的内容，页首的标题，页脚信息等。这种重复不仅带来不必要的工作量，而且会让修改变得更加麻烦。举例来说，如果页脚信息需要更新，那么每个页面都要一一进行修改。

显而易见，这两个问题有更优雅的处理方法。

### 模板上下文处理函数

对于多个模板内都需要使用的变量，可以使用 `app.context_processor` 装饰器注册一个模板上下文处理函数，如下所示：
app.py：模板上下文处理函数

```python
@app.context_processor
def inject_vars():  # 函数名可以随意修
    user = User.query.first()  # 用户对象
    return locals()  # 需要返回字典
```

这个函数返回的变量（字典键值对形式）将会统一注入到每个模板的上下文环境中，因此可以直接在模板中使用。

现在可以删除 404 错误处理函数和主页视图函数中的 user 变量定义，并删除在 `render_template()` 函数里传入的关键字参数：

```python
@app.route('/')
def index():
    movies = Movie.query.all()  # 读取所有电影
    return render_template('index.html', movies=movies)

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    """Custom 404 Errors page"""
    response = render_template('404.html')
    return response, 404  # 返回响应和状态码

@app.context_processor
def inject_vars():  # 函数名可以随意修改
    """模板上下文处理函数"""
    user = User.query.first()  # 用户对象
    if not user:
        user.name = 'Blood H'
    return locals()  # 需要返回字典
```

同样的，之后创建的任意一个模板，都可以在模板中直接使用 `user` 变量。

### 使用模板继承组织模板

对于模板内容重复的问题，Jinja2 提供了模板继承的支持。可以定义一个父模板，一般会称之为基模板（base
template）。基模板中包含完整的 HTML 结构和导航栏、页首、页脚都通用部分。在子模板里，我们可以使用 `extends` 标签来声明继承自某个基模板。

基模板中将要在子模板中追加或重写的部分定义成块 (block)。块使用 `block` 标签创建， `{% block 块名称 %}` 作为开始标记， {% endblock %} 或 {% endblock 块名称 %} 作为结束标记。通过在子模板里定义一个同样名称的块，可以实现向基模板的对应块位置追加或重写内容。

#### 编写基础模板

下面是新编写的基模板 base.html：
templates/base.html：基模板

```jinja2
<!DOCTYPE html>
<html lang="en">

<head>
    {% block head %}
    <meta charset="utf-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ user.name }}'s Watchlist</title>
    <link rel="icon" href="{{ url_for('static', filename='favicon.ico') }}">
    <link rel="stylesheet" href="{{ url_for('static', filename='style.css') }}" type="text/css">
    {% endblock %}
</head>

<body>
    <h2>
        <img alt="Avatar" class="avatar" src="{{ url_for('static', filename='images/avatar.png') }}">
        {{ user.name }}'s Watchlist
    </h2>
    <nav>
        <ul>
            <li><a href="{{ url_for('index') }}">Home</a></li>
        </ul>
    </nav>
    {% block content %}<h2>Content ...</h2>{% endblock %}
    <footer>
        <small>&copy; 2020 <a href="https://github.com/HEY-BLOOD/watchlist">Watchlist</a></small>
    </footer>
</body>

</html>
```

在基模板里，一共添加了两个块，一个是包含 <head></head> 内容的 `head` 块，另一个是用来在子模板中插入页面主体内容的 `content` 块。

**基模板中的两处新变化：**

1. 添加了一个新的 `<meta>` 元素，这个元素会设置页面的视口，让页面根据设备的宽度来自动缩放页面，让移动设备拥有更好的浏览体验：

   ```html
   <meta name="viewport" content="width=device-width, initial-scale=1.0">
   ```

2. 为页面添加了一个导航栏：

   ```html
   <nav>
       <ul>
           <li><a href="{{ url_for('index') }}">Home</a></li>
       </ul>
   </nav>
   ```

**导航栏对应的 CSS 代码如下所示：**

```css
/* 导航栏 */
nav ul {
    list-style-type: none;
    margin: 0;
    padding: 0;
    overflow: hidden;
    background-color: #333;
}

nav li {
    float: left;
}

nav li a {
    display: block;
    color: white;
    text-align: center;
    padding: 8px 12px;
    text-decoration: none;
}

nav li a:hover {
    background-color: #111;
}
```

#### 编写子模板

创建了基模板后，子模板的编写会变得非常简单。下面是新的主页模板（index.html）：
templates/index.html：继承基模板的主页模板

```html
{% extends 'base.html' %}

{% block content %}>
{# 使用 length 过滤器获取 movies 变量的长度 #}
<p>{{ movies|length }} Titles</p>
<ul class="movie-list">
    {% for movie in movies %} {# 迭代 movies 变量 #}
    <li>{{ movie.title }} - {{ movie.year }}
        <span class="float-right">
            <a class="imdb" href="https://www.imdb.com/find?q={{ movie.title }}" target="_blank"
                title="Find this movie on IMDb">IMDb</a>
        </span>
    </li> {# 等同于 movie['title'] #}
    {% endfor %} {# 使用 endfor 标签结束 for 语句 #}
</ul>
<img alt="Walking Totoro" class="totoro" src="{{ url_for('static', filename='images/totoro.gif') }}" title="to~to~ro~">
{% endblock %}
```

第一行使用 `extends` 标签声明扩展自模板 base.html，可以理解成“这个模板继承自 base.html“。接着定义了 `content` 块，这里的内容会插入到基模板中 `content` 块的位置。

> 提示 
>
> 默认的块重写行为是覆盖，如果想向父块里追加内容，可以在子块中使用 super() 声明，即 {{ super() }} 。

404 错误页面的模板类似，如下所示：
templates/404.html：继承基模板的 404 错误页面模板

```html
{% extends 'base.html' %}

{% block content %}
<ul class="movie-list">
    <li>
        Page Not Found - 404
        <span class="float-right">
            <a href="{{ url_for('index') }}">Go Home</a>
        </span>
    </li>
</ul>
{% endblock %}
```

#### **添加 IMDb 链接**

在主页模板里，为每一个电影条目右侧都添加了一个 IMDb 链接：

```html
<span class="float-right">
	<a class="imdb" href="https://www.imdb.com/find?q={{ movie.title }}" target="_blank" title="Find this movie on IMDb">IMDb</a>
</span>
```

这个链接的 `href` 属性的值为 IMDb 搜索页面的 URL，搜索关键词通过查询参数 `q` 传入，传入电影的标题。
对应的 CSS 定义如下所示：

```css
/* IMDb 链接 */
.float-right {
    float: right;
}

.imdb {
    font-size: 12px;
    font-weight: bold;
    color: black;
    text-decoration: none;
    background: #F5C518;
    border-radius: 5px;
    padding: 3px 5px;
}
```

### 本章小结

本章主要学习了 Jinja2 的模板继承机制，去掉了大量的重复代码，这让后续的模板编写工作变得更加轻松。

现在提交代码：

```powershell
$ git add .
$ git commit -m "Add base template and error template"
$ git push
```

### 进阶提示

* 自定义错误页面是为了引出两个重要的知识点，因此并没有着重介绍错误页面本身。这里只为 404 错误编写了自定义错误页面，对于另外两个常见的错误 400 错误和 500 错误，可以自己试着为它们编写错误处理函数和对应的模板。
* 因为示例程序的语言和电影标题使用了英文，所以电影网站的搜索链接使用了 IMDb，对于中文，可以使用豆瓣电影或时光网。以豆瓣电影为例，它的搜索链接为 https://movie.douban.com/subject_search?search_text=，即 `href="https://movie.douban.com/subject_search?search_text={{ movie.title }}"` 。
* 因为基模板会被所有其他页面模板继承，如果你在基模板中使用了某个变量，那么这个变量也需要使用模板上下文处理函数注入到模板里。



## 第 7 章：表单

在 HTML 页面里，需要编写表单来获取用户输入。典型的表单如下所示：

<form method="post"> <!-- 指定提交方法为 POST -->
	<label for="name">名字</label>
	<input type="text" name="name" id="name"> <!-- 文本输入框 -->
    <br>
	<label for="occupation">职业</label>
	<input type="text" name="occupation" id="occupation"> <!-- 文本输入框 -->
    <br>
	<input type="submit" name="submit" value="登录"> <!-- 提交按钮 -->
</form>

编写表单的 HTML 代码有下面几点需要注意：

* 在` <form>` 标签里使用 method 属性将提交表单数据的 HTTP 请求方法指定为 POST。如果不指定，则会默认使用 GET 方法，这会将表单数据通过URL 提交，容易导致数据泄露，而且不适用于包含大量数据的情况。
* `<input>` 元素必须要指定 `name` 属性，否则无法提交数据，在服务器端，我们也需要通过这个 `name` 属性值来获取对应字段的数据。

> 提示 
>
> 填写输入框标签文字的 `<label>` 元素不是必须的，只是为了辅助鼠标用户。 `for` 属性填入要绑定的 `<input>` 元素的 `id` 属性值。当使用鼠标点击标签文字时，会自动激活对应的输入框，这对复选框来说比较有用。

### 创建新条目

创建新条目可以放到一个新的页面来实现，也可以直接在主页实现。这里采用后者，首先在主页模板里添加一个表单：
templates/index.html：添加创建新条目表单

```html
<p>{{ movies|length }} Titles</p>
<form method="post">
    Name <input type="text" name="title" autocomplete="off" required>&nbsp;
    Year <input type="text" name="year" autocomplete="off" required>&nbsp;
    <input class="btn" type="submit" name="submit" value="Add">&nbsp;
</form>
```

在这两个输入字段中， `autocomplete` 属性设为 `off` 来关闭自动完成（按下输入框不显示历史输入记录）；另外还添加了 `required` 标志属性，如果用户没有输入内容就按下了提交按钮，浏览器会显示错误提示。

两个输入框和提交按钮相关的 CSS 定义如下：

```css
/* 新建条目表单，覆盖某些浏览器对 input 元素定义的字体 */
input[type=submit] {
    font-family: inherit;
}
input[type=text] {
    border: 1px solid #ddd;
}
input[name=year] {
    width: 50px;
}
.btn {
    font-size: 12px;
    padding: 3px 5px;
    text-decoration: none;
    cursor: pointer;
    background-color: white;
    color: black;
    border: 1px solid #555555;
    border-radius: 5px;
}
.btn:hover {
    text-decoration: none;
    background-color: black;
    color: white;
    border: 1px solid black;
}
```

接下来，需要考虑如何获取提交的表单数据。

### 处理表单数据

默认情况下，当表单中的提交按钮被按下，浏览器会创建一个新的请求，默认发往当前 URL（在 `<form>` 元素使用 `action` 属性可以自定义目标 URL）。

因为在模板里为表单定义了 `POST` 方法，输入数据，按下提交按钮，一个携带输入信息的 `POST` 请求会发往根地址。接着，会看到一个 `405 Method Not Allowed` 错误提示。这是因为处理根地址请求的 `inde` 视图默认只接受 `GET` 请求。

提示 在 HTTP 中，`GET` 和 `POST` 是两种最常见的请求方法，其中 `GET` 请求用来获取资源，而 `POST` 则用来创建 / 更新资源。访问一个链接时会发送 `GET` 请求，而提交表单通常会发送 `POST` 请求。

为了能够处理 POST 请求，我们需要修改一下视图函数：

```python
@app.route('/', methods=['GET', 'POST'])
```

在 `app.route()` 装饰器里，我们可以用 `methods` 关键字传递一个包含 HTTP 方法字符串的列表，表示这个视图函数处理哪种方法类型的请求。默认只接受 `GET` 请求，上面的写法表示同时接受 `GET` 和 `POST` 请求。

两种方法的请求有不同的处理逻辑：对于 `GET` 请求，返回渲染后的页面；对于 `POST` 请求，则获取提交的表单数据并保存。为了在函数内加以区分，可以使用 `if` 语句加以判断：

app.py：创建电影条目

```python
from flask import Flask, render_template, request, redirect, flash
# ...
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('index.html',  movies=movies)
```

在 `if` 语句内，编写了处理表单数据的代码，其中涉及 3 个新的知识点，下面来一一了解。

#### 请求对象

Flask 会在请求触发后把请求信息放到 `request` 对象里，你可以从 `flask` 包导入它：

```python
from flask import request
```

因为它在请求触发时才会包含数据，所以只能在视图函数内部调用它。它包含请求相关的所有信息，比如请求路径 `request.path`、请求方法 `request.method` 、表单数据 `request.form`、查询字符串 `request.args` 等。

在上面的 `i`f 语句中，首先通过 `request.method` 的值来判断请求方法。在 `if` 语句内，通过 `request.form` 来获取表单数据。 `request.form` 是一个特殊的字典，用表单字段的 `name` 属性值可以获取用户填入的对应数据：

```python
if request.method == 'POST':
	title = request.form.get('title')
	year = request.form.get('year')
```

#### flash 消息

在用户执行某些动作后，通常在页面上显示一个提示消息。最简单的实现就是在视图函数里定义一个包含消息内容的变量，传入模板，然后在模板里渲染显示它。因为这个需求很常用，Flask 内置了相关的函数。其中 `flash()` 函数用来在视图函数里向模板传递提示消息， `get_flashed_messages()` 函数则用来在模板中获取提示消息。

`flash()` 的用法很简单，首先从 `flask` 包导入 `flash` 函数：

```python
from flask import flash
```

然后在视图函数里调用，传入要显示的消息内容：

```python
flash('Item Created.')
```

`flash()` 函数在内部会把消息存储到 Flask 提供的 `session` 对象里。 `session` 用来在请求间存储数据，它会把数据签名后存储到浏览器的Cookie 中，所以需要设置签名所需的密钥：

```python
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'
```

> 提示 
>
> 这个密钥的值在开发时可以随便设置。基于安全的考虑，在部署时应该设置为随机字符，且不应该明文写在代码里， 在部署章节会详细介绍。

在基模板 base.html 里使用 `get_flashed_messages()` 函数获取 flash 提示消息并显示，插入在页面标题上方：

```html
<!-- flash提示消息 -->
{% for message in get_flashed_messages() %}
<div class="alert">{{ message }}</div>
{% endfor %}
<h2> ... </h2>
```

`alert` 类为提示消息增加样式：

```css
/* flash 提示消息 */
.alert {
    position: relative;
    padding: 7px;
    margin: 7px 0;
    border: 1px solid transparent;
    color: #004085;
    background-color: #cce5ff;
    border-color: #b8daff;
    border-radius: 5px;
}
```

通过在 `<input>` 元素内添加 `required` 属性实现的客户端验证并不完全可靠，还需要在服务器端追加验证：

```python
if not title or not year or len(year) > 4 or len(title) > 60:
    flash('Invalid input.')  # 显示错误提示
    return redirect(url_for('index'))  # 重定向回主页
# ...
flash('Item created.')  # 显示成功创建的提示
```

> 提示 
>
> 在真实世界里，会进行更严苛的验证，比如对数据去除首尾的空格。一般情况下，会使用第三方库来实现表单数据的验证工作。比如  `WTForms` 

如果输入的某个数据为空，或是长度不符合要求，就显示错误提示“Invalid input.”，否则显示成功创建的提示“Item Created.”。

#### 重定向响应

重定向响应是一类特殊的响应，它会返回一个新的 URL，浏览器在接受到这样的响应后会向这个新 URL 再次发起一个新的请求。Flask 提供了 `redirect()` 函数来快捷生成这种响应，传入重定向的目标 URL 作为参数，比如 `redirect('http://helloflask.com')` 。根据验证情况，我们发送不同的提示消息，最后都把页面重定向到主页，这里的主页 URL 均使用 `url_for()` 函数生成：

```python
if not title or not year or len(year) > 4 or len(title) > 60:
	flash('Invalid title or year!')
	return redirect(url_for('index')) # 重定向回主页
# ...
flash('Item created.')
return redirect(url_for('index')) # 重定向回主页
```

### 编辑条目

编辑的实现和创建类似，先创建一个用于显示编辑页面和处理编辑表单提交请求的视图函数：
app.py：编辑电影条目

```python
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))
        # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录
```

这个视图函数的 URL 规则有一些特殊，其中的 `<int:movie_id>` 部分表示URL 变量，而 `int` 则是将变量转换成整型的 URL 变量转换器。生成这个视图的 URL 时需要传入对应的变量，比如 `url_for('edit', movie_id=2)` 会生成 `/movie/edit/2`。

`movie_id` 变量是电影条目记录在数据库中的主键值，这个值用来在视图函数里查询到对应的电影记录。查询的时候使用了 `get_or_404()` 方法，它会返回对应主键的记录，如果没有找到，则返回 404 错误响应。

为什么要在最后把电影记录传入模板？既然要编辑某个条目，那么必然要在输入框里提前把对应的数据放进去，以便于进行更新。在模板里，通过表单 `<input>` 元素的 `value` 属性即可将它们提前写到输入框里。完整的编辑页面模板如下所示：

```html
{% extends 'base.html' %}

{% block content %}
<h3>Edit item</h3>
<form method="post">
    Name <input type="text" name="title" autocomplete="off" required value="{{ movie.title }}">&nbsp;
    Year <input type="text" name="year" autocomplete="off" required value="{{ movie.year }}">&nbsp;
    <input class="btn" type="submit" name="submit" value="Update">&nbsp;
</form>
{% endblock %}
```

最后在主页每一个电影条目右侧都添加一个指向该条目编辑页面的链接：
index.html：编辑电影条目的链接

```html
<span class="float-right">
	<a class="btn" href="{{ url_for('edit', movie_id=movie.id) }}">Edit</a>
    ...
</span>
```

### 删除条目

因为不涉及数据的传递，删除条目的实现更加简单。首先创建一个视图函数执行删除操作，如下所示：
app.py：删除电影条目

```python
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
```

为了安全的考虑，一般会使用 POST 请求来提交删除请求，也就是使用表单来实现（而不是创建删除链接）：
index.html：删除电影条目表单

```html
<span class="float-right">
	<form class="inline-form" method="post" action="{{ url_for('delete', movie_id=movie.id) }}">
		<input class="btn" type="submit" name="delete" value="Delete" onclick="return confirm('Are you sure?')">
	</form>&nbsp;
	...
</span>
```

为了让表单中的删除按钮和旁边的编辑链接排成一行，为表单元素添加了下面的 CSS 定义：

```css
/* 删除条目 */
.inline-form {
	display: inline;
}
```

### 本章小结

本章我们完成了程序的主要功能：添加、编辑和删除电影条目。提交代码：

```powershell
$ git add .
$ git commit -m "Create, edit and delete item by form"
$ git push
```

> 提示
>
> 在后续的 commit 里，将为另外两个常见的 HTTP 错误：400（Bad Request） 和 500（Internal Server Error） 错误编写了错误处理函数和对应的模板，前者会在请求格式不符要求时返回，后者则会在程序内部出现任意错误时返回（关闭调试模式的情况下）。

### 进阶提示

* 从上面的代码可以看出，手动验证表单数据既麻烦又不可靠。对于复杂的程序，一般会使用集成了 WTForms 的扩展 [Flask-WTF](https://github.com/lepture/flask-wtf) 来简化表单处理。通过编写表单类，定义表单字段和验证器，它可以自动生成表单对应的 HTML 代码，并在表单提交时验证表单数据，返回对应的错误消息。更重要的，它还内置了 CSRF（跨站请求伪造） 保护功能。你可以阅读 [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) 文档和 Hello, Flask! 专栏上的 [表单系列文章](https://zhuanlan.zhihu.com/p/23577026) 了解具体用法。
* CSRF 是一种常见的攻击手段。以删除表单为例，某恶意网站的页面中内嵌了一段代码，访问时会自动发送一个删除某个电影条目的 POST 请求到程序。如果访问了这个恶意网站，就会导致电影条目被删除，因为程序没法分辨请求发自哪里。解决方法通常是在表单里添加一个包含随机字符串的隐藏字段，同时在 Cookie 中也创建一个同样的随机字符串，在提交时通过对比两个值是否一致来判断是否是用户自己发送的请求。在这个程序中没有实现 CSRF 保护。
* 使用 Flask-WTF 时，表单类在模板中的渲染代码基本相同，可以编写宏来渲染表单字段。若使用 Bootstap，那么扩展 [Bootstrap-Flask](https://github.com/greyli/bootstrap-flask) 内置了多个表单相关的宏，可以简化渲染工作。
* 可以把删除按钮的行内 JavaScript 代码改为事件监听函数，写到单独的 JavaScript 文件里。再进一步，也可以使用 JavaScript 来监听点击删除按钮的动作，并发送删除条目的 POST 请求，这样删除按钮就可以使用普通 `<a>` 标签（CSRF 令牌存储在元素属性里），而不用创建表单元素。



## 第 8 章：用户认证

目前为止，虽然程序的功能大部分已经实现，但还缺少一个非常重要的部分——**用户认证保护**。页面上的编辑和删除按钮是公开的，所有人都可以看到。假如我们现在把程序部署到网络上，那么任何人都可以执行编辑和删除条目的操作，这显然是不合理的。

这一章会为程序添加用户认证功能，这会把用户分成两类，一类是管理员，通过用户名和密码登入程序，可以执行数据相关的操作；另一个是访客，只能浏览页面。在此之前，先来看看密码应该如何安全的存储到数据库中。

### 安全存储密码

把密码明文存储在数据库中是极其危险的，假如攻击者窃取了你的数据库，那么用户的账号和密码就会被直接泄露。更保险的方式是对每个密码进行计算生成独一无二的密码散列值，这样即使攻击者拿到了散列值，也几乎无法逆向获取到密码。

Flask 的依赖 Werkzeug 内置了用于生成和验证密码散列值的函数： 

*  `werkzeug.security.generate_password_hash()` 用来为给定的密码生成密码散列值
* `werkzeug.security.check_password_hash()` 则用来检查给定的散列值和密码是否对应

使用示例如下：

```python
>>> from werkzeug.security import generate_password_hash, check_password_hash 
>>> pw_hash = generate_password_hash('admin')  # 为密码 admin 生成密码散列值
>>> pw_hash  # 查看密码散列值
'pbkdf2:sha256:150000$4CMpiuQS$8636daf2c823f51bd680c8984fc11bbe387ed5c40f84e32e2aea010f6b6486fe'
>>> check_password_hash(pw_hash, 'admin')  # 检查散列值是否对应密码 admin
True
>>> check_password_hash(pw_hash, 'admin12345')  # 检查散列值是否对应密码 admin12345
False
```

在存储用户信息的 `User` 模型类添加 `username` 字段和 `password_hash` 字段，分别用来存储登录所需的用户名和密码散列值，同时添加两个方法来实现设置密码和验证密码的功能：

```python
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值
```

因为模型（表结构）发生变化，所以需要重新生成数据库（这会清空数据）：

```powershell
(myenv) PS E:\PyCode\watchlist> flask initdb --drop
Initialized database.
```

### 生成管理员账户

因为程序只允许一个人使用，没有必要编写一个注册页面。可以编写一个命令来创建管理员账户，下面是实现这个功能的 `admin()` 函数：

```python
import click

@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Blood Wong')
        user.set_password(password)  # 设置密码
    db.session.add(user)
    db.session.commit()  # 提交数据库会话
    click.echo('Completed.')
```

使用 `click.option()` 装饰器设置的两个选项分别用来接受输入用户名和密码。执行 `flask admin` 命令，输入用户名和密码后，即可创建管理员账户。如果执行这个命令时账户已存在，则更新相关信息：

```powershell
(myenv) PS E:\PyCode\watchlist> flask.exe admin
Username: admin
Password: admin  # hide_input=True 密码输入隐藏
Repeat for confirmation:admin  # confirmation_prompt=True 二次确认，输入隐藏
Updating user...
Completed.
```

既然已经可以创建管理员账户，那么初始化虚拟数据中的 User 对象则不再需要，更改 `forge()` 视图函数如下：

以 `-` 开头的表示删除，`$` 开头的表示更改，app.py：更改虚拟数据

```python
@app.cli.command()
def forge():
-   name = 'Blood H'
$   # 虚拟电影条目数据
    movies = [
		# ...
    ]
-   user = User(name=name)
-   db.session.add(user)
```



### 使用 Flask-Login 实现用户认证

扩展 [Flask-Login](https://github.com/maxcountryman/flask-login) 提供了实现用户认证需要的各类功能函数，使用它来实现程序的用户认证，首先来安装它：

```powershell
(myenv) PS E:\PyCode\watchlist> pip install flask-login
# ...
Successfully installed flask-login-0.5.0
```

这个扩展的初始化步骤稍微有些不同，除了实例化扩展类之外，还要实现一个“用户加载回调函数”，代码如下：
app.py：初始化 Flask-Login

```python
from flask_login import LoginManager

login_manager = LoginManager(app)  # 实例化扩展类

@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象
```

Flask-Login 提供了一个 `current_user` 变量，注册这个函数的目的是，当程序运行后，如果用户已登录， `current_user` 变量的值会是当前用户的用户模型对象。

另一个步骤是让存储用户的 User 模型类继承 Flask-Login 提供的 `UserMixin` 类：

```python
from flask_login import UserMixin

class User(db.Model, UserMixin):
	# ...
```

继承这个类会让 **User** 类拥有几个用于判断认证状态的属性和方法，其中最常用的是 `is_authenticated` 属性：如果当前用户已经登录，那么 `current_user.is_authenticated` 会返回 `True` ， 否则返回 `False` 。有了`current_user` 变量和这几个验证方法和属性，我们可以很轻松的判断当前用户的认证状态。

### 登入与登出

登录用户使用 Flask-Login 提供的 `login_user()` 函数实现，需要传入用户模型类对象作为参数。下面是用于显示登录页面和处理登录表单提交请求的视图函数：
app.py：用户登录

```python
from flask_login import login_user

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    return render_template('login.html')
```

下面是包含登录表单的登录页面模板：
templates/login.html：登录页面

```html
{% extends 'base.html' %}

{% block content %}
<h3>Login</h3>
<form method="post">
    Username<br>
    <input type="text" name="username" required><br><br>
    Password<br>
    <!-- 密码输入框的 type 属性使用 password，会将输入值显示为圆点 -->
    <input type="password" name="password" required><br><br>
    <input class="btn" type="submit" name="submit" value="Submit">
</form>
{% endblock %}
```

登出和登录相对，登出操作则需要调用 logout_user() 函数，使用下面的视图函数实现：

```python
from flask_login import login_required, logout_user

# ...

@app.route('/logout')
@login_required  # 用于视图保护，
def logout():
    """登出用户"""
    logout_user()  # 登出用户
    flash('Goodbye.')
    return redirect(url_for('index'))  # 重定向回首页
```

实现了登录和登出后，先看看认证保护，最后再把对应这两个视图函数的登录/登出链接放到导航栏上。

### 认证保护

在 Web 程序中，有些页面或 URL 不允许未登录的用户访问，而页面上有些内容则需要对未登陆的用户隐藏，这就是认证保护。

#### 视图保护

在视图保护层面来说，未登录用户不能执行下面的操作：

* 访问编辑页面
* 访问设置页面
* 执行注销操作
* 执行删除操作
* 执行添加新条目操作

对于不允许未登录用户访问的视图，只需要为视图函数附加一个 `login_required` 装饰器就可以将未登录用户拒之门外。以删除条目视图为例：

```python
@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    # ...
```

添加这个装饰器后，未登录用户访问对应的 URL，Flask-Login 会把用户重定向到登录页面，并显示错误提示。

为了让这个重定向操作正确执行，把 `login_manager.login_view` 的值设为程序的登录视图端点（函数名）：

```python
login_manager.login_view = 'login'
```

> 提示 
>
> 如果需要的话，可以通过设置 `login_manager.login_message` 来自定义错误提示消息，比如：
>
> ```python
> login_manager.login_massage = 'You are not currently logged in, please log in your account first.'
> ```

编辑视图同样需要附加这个装饰器：

```python
@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    # ...
```

创建新条目的操作稍微有些不同，因为对应的视图同时处理显示页面的 GET 请求和创建新条目的 POST 请求，而现在仅需要禁止未登录用户创建新条目，因此不能使用 `login_required` ，而是在函数内部的 POST 请求处理代码前进行过滤：

```python
from flask_login import login_required, current_user

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 添加新条目，用户保护
        if not current_user.is_authenticated:  # 如果当前用户未认证
            return redirect(url_for('login'))  # 重定向到登录页面
        # ...
```

最后，为程序添加一个设置页面，支持修改用户的名字 ：
app.py：支持设置用户名字

```python
from flask_login import login_required, current_user

@app.route('/settings', methods=['GET', 'POST'])
@login_required  # 视图保护
def settings():
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        print(current_user is User.query.first())
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        db.session.commit()
        flash('Updated name.')
    return render_template('settings.html')
```

下面是对应的模板：
templates/settings.html：设置页面模板

```python
{% extends 'base.html' %}

{% block content %}
<h3>Settings</h3>
<form method="post">
    Your Name <input type="text" name="name" autocomplete="off" required value="{{ current_user.name }}">
    <input class="btn" type="submit" name="submit" value="Save">
</form>
{% endblock %}
```

#### 模板内容保护

认证保护的另一形式是页面模板内容的保护。比如，不能对未登录用户显示下列内容：

* 创建新条目表单
* 编辑按钮
* 删除按钮

这几个元素的定义都在首页模板（index.html）中，以创建新条目表单为例，在表单外部添加一个 if 判断：

```html
<!-- 模板内容保护，在模板中可以直接使用 current_user 变量 -->
{% if current_user.is_authenticated %}
<form method="post">
    <!-- ………… -->
</form>
{% endif %}
```

在模板渲染时，会先判断当前用户的登录状态，如果用户没有登录 `current_user.is_authenticated` 返回 `False` ，就不会渲染表单部分的HTML 代码，即上面代码块中 `{% if ... %}` 和 `{% endif %}` 之间的代码。
类似的还有编辑和删除按钮，在 `<li>` 元素中更改：

```html
<li>{{ movie.title }} - {{ movie.year }}
    <span class="float-right">

        <!-- 模板内容保护，未登录账户时不可见 -->
        {% if current_user.is_authenticated %}
        <form class="inline-form" method="post" action="{{ url_for('delete', movie_id=movie.id) }}">
            <input class="btn" type="submit" name="delete" value="Delete" onclick="return confirm('Are you sure?')">
        </form>
        <a class="btn" href="{{ url_for('edit', movie_id=movie.id) }}">Edit</a>
        {% endif %}
		
        <!-- ………… -->
    </span>
</li> {# 等同于 movie['title'] #}
```

有些地方则需要根据登录状态分别显示不同的内容，比如基模板（base.html）中的导航栏。如果用户已经登录，就显示设置和登出链接，否则显示登录链接：

base.html ：登录登出模板内容保护

```html
<ul>
    <li><a href="{{ url_for('index') }}">Home</a></li>
    
    <!-- 登录登出模板内容保护，未登录账户时不可见 -->
    {% if current_user.is_authenticated %}
    <li><a href="{{ url_for('settings') }}">Settings</a></li>
    <li><a href="{{ url_for('logout') }}">Logout</a></li>
    {% else %}
    <li><a href="{{ url_for('login') }}">Login</a></li>
    {% endif %}
    
</ul>
```

现在的程序中，登录与未登录的可用功能如下：

<center><strong>已登录账号功能介绍</strong></center>
|      功能       |                     说明                     |
| :-------------: | :------------------------------------------: |
|   index 首页    | 显示 Movie 条目列表（Watchlist），index.html |
|  settings 设置  |           全局设置，settings.html            |
|   logout 注销   |        注销已认证的用户，logout.html         |
|  add 添加条目   |    添加新的 Movie 条目，集成在 index.html    |
|  edit 编辑条目  |      更改已存在的 Movie 条目，edit.html      |
| delete 删除条目 |     删除已存在的 Movie 条目，delete.html     |

<center><strong>未登录账号功能介绍</strong></center>
|    功能    |                     说明                     |
| :--------: | :------------------------------------------: |
| index 首页 | 显示 Movie 条目列表（Watchlist），index.html |
| login 登录 |         用户认证（登录），login.html         |

### 本章小结

添加用户认证后，在功能层面，基本算是完成了。提交代码：

```powershell
$ git add .
$ git commit -m "User authentication with Flask-Login"
$ git push
```

### 进阶提示

* 访问 [Flask-Login 文档](https://github.com/maxcountryman/flask-login) 了解更多细节和用法。



## 第 9 章：测试

在此之前，每次为程序添加了新功能，都要手动在浏览器里访问程序进行测试。除了测试新添加的功能，还要确保旧的功能依然正常工作。在功能复杂的大型程序里，如果每次修改代码或添加新功能后手动测试所有功能，那会产生很大的工作量。另一方面，手动测试并不可靠，重复进行测试操作也很枯燥。基于这些原因，为程序编写自动化测试就变得非常重要。

> 注意 
>
> 为了便于介绍，统一在这里介绍关于测试的内容。在实际的项目开发中，应该在开发每一个功能后立刻编写相应的测试，确保测试通过后再开发下一个功能。

### 单元测试

单元测试指对程序中的函数等独立单元编写的测试，它是自动化测试最主要的形式。这一章将使用 Python 标准库中的测试框架 `unittest` 来编写单元测试，通过一个简单的例子了解一些基本概念。

假设 `module_foo.py` 文件中编写了下面这个函数：

```python
def sayhello(to=None):
	if to:
		return 'Hello, %s!' % to
	return 'Hello!'
```

`test_sayhello.py` 为这个函数编写的单元测试：

```python
import unittest
from module_foo import sayhello


class SayHelloTestCase(unittest.TestCase):
    """测试用例"""

    def setUp(self):
        """测试固件，每个测试方法执行前被调用"""
        pass

    def tearDown(self):
        """测试固件，每个测试方法执行后被调用"""
        pass

    def test_sayhello(self):  # 第 1 个测试方法
        rv = sayhello()
        self.assertEqual(rv, 'Hello!')

    def test_sayhello_to_somebody(self):  # 第 2 个测试方法
        rv = sayhello(to='Blood')
        self.assertEqual(rv, 'Hello, Blood!')


if __name__ == "__main__":
    unittest.main()
```

测试用例继承 `unittest.TestCase` 类，在这个类中创建的以 `test_` 开头的方法将会被视为测试方法。

内容为空的两个方法很特殊，它们是测试固件，用来执行一些特殊操作。比如 `setUp()` 方法会在每个测试方法执行前被调用，而 `tearDown()` 方法则会在每一个测试方法执行后被调用（注意这两个方法名称的大小写）。

如果把执行测试方法比作战斗， `setUp()` 就是准备弹药、规划战术的工作，`tearDown()` 则是打扫战场。

每一个测试方法（以 `test_` 开头的）对应一个要测试的函数/功能/使用场景。上面创建了两个测试方法，`test_sayhello()` 方法测试 `sayhello()` 函数，`test_sayhello_to_somebody()` 方法测试传入参数时的 `sayhello()` 函数。

在测试方法里，使用断言方法来判断程序功能是否正常。以第一个测试方法为例，先把 `sayhello()` 函数调用的返回值保存为 `rv` 变量，然后使用 `self.assertEqual(rv, 'Hello!')` 来判断返回值内容是否符合预期。如果断言方法出错，就表示该测试方法未通过。

常用的断言方法：

- assertEqual(a, b)
- assertNotEqual(a, b)
- assertTrue(x)
- assertFalse(x)
- assertIs(a, b)
- assertIsNot(a, b)
- assertIsNone(x)
- assertIsNotNone(x)
- assertIn(a, b)
- assertNotIn(a, b)

这些方法的作用从方法名称上基本可以得知。

执行 `python test_sayhello.py` 执行所有测试，并输出测试的结果、通过情况、总耗时等信息。

```powershell
(myenv) PS E:\PyCode\watchlist> python.exe .\test_sayhello.py
..
----------------------------------------------------------------------
Ran 2 tests in 0.001s

OK
```

单元测试通过，并无发生异常。现在将第 22 行的 `'Blood'` 更改为 `'abc'` (不同的字符串) 后再次测试：

```powershell
(myenv) PS E:\PyCode\watchlist> python.exe .\test_sayhello.py
.F
======================================================================
FAIL: test_sayhello_to_somebody (__main__.SayHelloTestCase)
----------------------------------------------------------------------
Traceback (most recent call last):
  File ".\test_sayhello.py", line 22, in test_sayhello_to_somebody
    self.assertEqual(rv, 'Hello, Blood!')
AssertionError: 'Hello, abc!' != 'Hello, Blood!'
- Hello, abc!
+ Hello, Blood!


----------------------------------------------------------------------
Ran 2 tests in 0.002s

FAILED (failures=1)
```

结果显示第 22 行所在的 `test_sayhello_to_somebody` 测试函数发生了异常，测试结果 `'Hello, abc!'` 与预期的结果 `'Hello, Blood!'` 不一样。

### 测试 Flask 程序

在项目根目录创建一个 test_watchlist.py 脚本来存储测试代码，先编写测试固件和两个简单的基础测试：
test_watchlist.py：测试固件

```python
import unittest
from app import app, db, User, Movie


class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""

    def setUp(self):
        # 更新配置
        app.config.update(
            TESTING=True,  # 开启测试模式，在出错时不会输出多余信息
            SQLALCHEMY_DATABASE_URI='sqlite:///:memory:'  # 使用 SQLite 内存型数据库
        )
        # 创建数据库和表
        db.create_all()
        # 创建测试数据，一个用户，一个电影条目
        user = User(name='TestName', username='TestUsername')
        user.set_password('TestPassword')
        movie = Movie(title='Test Movie Title', year='2019')
        # 使用 add_all() 方法一次添加多个模型类实例，传入列表
        db.session.add_all([user, movie])
        db.session.commit()
        self.client = app.test_client()  # 创建测试客户端
        self.runner = app.test_cli_runner()  # 创建测试命令运行器

    def tearDown(self):
        db.session.remove()  # 清除数据库会话
        db.drop_all()  # 删除数据库表
        
    def test_app_exist(self):
        """ 测试程序实例是否存在 """
        self.assertIsNotNone(app)
        
    def test_app_is_testing(self):
        """ 测试程序是否处于测试模式 """
        self.assertTrue(app.config['TESTING'])
```

某些配置，在开发和测试时通常需要使用不同的值。在 `setUp()` 方法中，更新了两个配置变量的值，首先将 `TESTING` 设为 `True` 来开启测试模式，这样在出错时不会输出多余信息；然后将 `SQLALCHEMY_DATABASE_URI` 设为 `'sqlite:///:memory:'`，这会使用 SQLite 内存型数据库，不会干扰开发时使用的数据库文件。你也可以使用不同文件名的 SQLite 数据库文件，但内存型数据库速度更快。

接着，调用 `db.create_all()` 创建数据库和表，然后添加测试数据到数据库。在 `setUp()` 方法最后创建的两个类属性分别为测试客户端和测试命令运行器，前者用来模拟客户端请求，后者用来触发自定义命令，之后介绍。

在 `tearDown()` 方法中，调用 `db.session.remove()` 清除数据库会话并调用 `db.drop_all()` 删除数据库表。测试时的程序状态和真实的程序运行状态不同，所以调用 `db.session.remove()` 来确保数据库会话被清除。

#### 测试客户端

`app.test_client()` 返回一个测试客户端对象，可以用来模拟客户端（浏览器），创建类属性 `self.client` 来保存它。对它调用 get() 方法就相当于浏览器向服务器发送 GET 请求，调用 post() 则相当于浏览器向服务器发送
POST 请求，以此类推。下面是两个发送 GET 请求的测试方法，分别测试 404 页面和主页：

test_watchlist.py：测试固件

```python
import unittest
from app import app, db, User, Movie


class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""
    # ......

    def test_404_page(self):
        """ Page not fount Test Function """
        response = self.client.get('/nothing')  # Get 方法访问 URL 路由
        data = response.get_data(as_text=True)  # 获取 Unicode 格式的响应主体
        self.assertIn('Page Not Found - 404', data)  # 判断是否包含预期值
        self.assertIn('Go Home', data)
        self.assertEqual(response.status_code, 404)  # 判断响应状态码

    def test_index_page(self):
        """ Home page Test Function """
        response = self.client.get('/')  # Get 方法访问 '/' 路由
        data = response.get_data(as_text=True)
        self.assertIn('TestName\'s Watchlist', data)
        self.assertIn('Test Movie Title', data)
        self.assertEqual(response.status_code, 200)

```

调用这类方法返回包含响应数据的响应对象，对这个响应对象调用 `get_data()` 方法并把 `as_text` 参数设为 `True` 可以获取 `Unicode` 格式的响应主体。通过判断响应主体中是否包含预期的内容来测试程序是否正常工作，比如 404 页面响应是否包含 `Go Home`，主页响应是否包含标题 `Test Name's Watchlist`。

接下来测试数据库操作相关的功能，比如创建、更新和删除电影条目。这些操作对应的请求都需要登录账户后才能发送，先编写一个用于登录账户的辅助方法 `login()`：

非 `test_` 开头的方法，不会自动的被调用

```python
class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""
    # ......
    
    def login(self):
    """ 辅助方法，用于登入用户 """
    self.client.post('/login', data=dict(  # Post 方法，发送请求，登录账户
        username='TestUsername',
        password='TestPassword'
    ), follow_redirects=True)  # 跟随重定向
```

在 `login()` 方法中，使用 `post()` 方法发送提交登录表单的 POST 请求。和 `get()` 方法类似，需要先传入目标 URL，然后使用 `data` 关键字以字典的形式传入请求数据（字典中的键为表单 `<input>` 元素的 `name` 属性
值），作为登录表单的输入数据；而将 `follow_redirects` 参数设为 `True` 可以跟随重定向，最终返回的会是重定向后的响应。

test_watchlist.py：测试创建、更新和删除条目的方法

```python
class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""
    # ......
    
    def test_add_item(self):
        ''' 测试创建条目 '''
        self.login()  # 首先在客户端登录用户

        # 测试创建条目操作
        response = self.client.post(
            '/', data=dict(title='New Movie', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item created.', data)  # 创建成功提示
        self.assertIn('New Movie', data)  # 新条目的名称

        # 测试创建条目操作，电影标题 title 为空
        response = self.client.post(
            '/', data=dict(title='', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)  # 没有创建成功提示
        self.assertIn('Invalid input.', data)  # 输入不合法

        # 测试创建条目操作，电影年份 year 为空
        response = self.client.post(
            '/', data=dict(title='New Movie', year=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item created.', data)  # 没有创建成功提示
        self.assertIn('Invalid input.', data)  # 输入不合法

    def test_update_item(self):
        """ 测试更新条目 """
        self.login()  # 首先在客户端登录用户

        # 测试更新条目页面
        response = self.client.get('/movie/edit/1')
        data = response.get_data(as_text=True)
        self.assertIn('Test Movie Title', data)
        self.assertIn('2019', data)

        # 测试更新条目操作
        response = self.client.post(
            '/movie/edit/1', data=dict(title='New Movie Edited', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item updated.', data)
        self.assertNotIn('Invalid input.', data)

        # 测试更新条目操作，电影标题 title 为空
        response = self.client.post(
            '/movie/edit/1', data=dict(title='', year='2019'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertIn('Invalid input.', data)
        self.assertNotIn('Test Movie Title', data)  # 显示条目 1 的原标题

        # 测试更新条目操作，电影年份 year 为空
        response = self.client.post(
            '/movie/edit/1', data=dict(title='New Movie Edited Again', year=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Item updated.', data)
        self.assertIn('Invalid input.', data)
        self.assertNotIn('Test Movie Title', data)  # 显示条目 1 的原标题
        self.assertNotIn('New Movie Edited Again', data)

    def test_delete_item(self):
        """ 测试删除条目 """
        self.login()  # 首先在客户端登录用户

        # 测试删除条目
        response = self.client.post('/movie/delete/1', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Item deleted.', data)
        self.assertNotIn('Test Movie Title', data)
```

在这几个测试方法中，大部分的断言都是在判断响应主体是否包含正确的提示消息和电影条目信息。

test_watchlist.py：测试认证相关功能 (登录、登出和认证保护等功能)

```python
class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""
    # ......
    
    def test_login_protect(self):
        """ 测试登录保护 """
        response = self.client.get('/')
        data = response.get_data(as_text=True)
        self.assertIn('Login', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('<form method="post">', data)

    def test_login(self):
        """ 测试用户登录 """

        # 测试登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password='TestPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('TestName', data)
        self.assertIn('Edit', data)
        self.assertIn('Delete', data)
        self.assertIn('Settings', data)
        self.assertIn('Logout', data)
        self.assertIn('Login success.', data)  # 已经有 Login 字符串
        self.assertNotIn('<a href="/login">Login</a>', data)  # Login 超链接
        self.assertNotIn('Invalid input.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.client.get('/logout')  # 退出登录

        # 测试使用错误的密码登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password='TestInvalidPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid input.', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('TestName', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用错误的用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestInvalidUsername', password='TestPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid input.', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用错误的密码和错误的用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestInvalidUsername', password='TestInvalidPassword'), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid input.', data)
        self.assertIn('<h3>Login</h3>', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('Invalid username or password.', data)

        # 测试使用空密码登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.assertIn('Invalid input.', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('<h3>Login</h3>', data)

        # 测试使用空用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.assertIn('Invalid input.', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('<h3>Login</h3>', data)

        # 测试使用空密码和空用户名登录
        response = self.client.post(
            '/login', data=dict(username='TestUsername', password=''), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('Login success.', data)
        self.assertNotIn('Invalid username or password.', data)
        self.assertIn('Invalid input.', data)
        self.assertIn('TestName', data)
        self.assertIn('Login', data)
        self.assertIn('<h3>Login</h3>', data)

    def test_logout(self):
        """ 测试登出 """
        self.login()  # 首先在客户端登录用户

        response = self.client.get('/logout', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Goodbye.', data)
        self.assertIn('Login', data)
        self.assertNotIn('Edit', data)
        self.assertNotIn('Delete', data)
        self.assertNotIn('Settings', data)
        self.assertNotIn('Logout', data)
        self.assertNotIn('<form method="post">', data)
        self.assertNotIn('<h3>Login</h3>', data)

    def test_settings(self):
        """ 测试设置 """
        self.login()  # 首先在客户端登录用户

        # 测试设置页面
        response = self.client.get('/settings', follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('<h3>Settings</h3>', data)
        self.assertIn('Your Name', data)

        # 测试更新设置
        response = self.client.post('/settings', data=dict(
            name='Blood Wong',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Updated name.', data)
        self.assertIn('Blood Wong', data)

        # 测试更新设置，姓名为空
        response = self.client.post('/settings', data=dict(
            name='',
        ), follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn('Blood Wong', data)  # 上面更新成功后的名称
        self.assertIn('Invalid input.', data)
        self.assertNotIn('Updated name.', data)
```

#### 测试命令

除了测试程序的各个视图函数，还需要测试自定义命令。 `app.test_cli_runner()` 方法返回一个命令运行器对象，创建类属性 `self.runner` 来保存它。通过对它调用 `invoke()` 方法可以执行命令，传入命令函数对象，或是使用 `args` 关键字直接给出命令参数列表。 `invoke()` 方法返回的命令执行结果对象，它的 `output` 属性返回命令的输出信息。首先在 `setUp()` 测试固件中添加以下代码：

```python
def setUp(self):
    # …………
    self.runner = app.test_cli_runner()  # 创建测试命令运行器
```

下面是为各个自定义命令编写的测试方法：

test_watchlist.py：测试自定义命令行命令

```python
from app import app, db, Movie, User, forge, initdb  # 导入命令函数

class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""
	# …………

    def test_forge_command(self):
        """ 测试 forge 命令，创建虚拟数据 """
        result = self.runner.invoke(forge)  # 在控制台执行 forge 命令
        self.assertIn('Generate fake data completed!',
                      result.output)  # 比较执行命令后的输出

    def test_initdb_command(self):
        """ 测试 initdb 命令，初始化数据库 """

        # 初始化数据库，无参数
        result = self.runner.invoke(initdb)
        self.assertIn('Initialized database.', result.output)

        # 初始化数据库，参数 --drop
        result = self.runner.invoke(args=['initdb', '--drop'])
        self.assertIn('Initialized database.', result.output)

    def test_admin_command(self):
        """ 测试 admin 命令，生成管理员用户 """

        # 没有创建过管理员用户
        self.runner.invoke(args=['initdb', '--drop'])  # 初始化数据库，删除 setUp中创建的用户
        result = self.runner.invoke(
            args=['admin', '--username', 'admin_username', '--password', 'admin_password'])
        self.assertIn('Creating user...', result.output)
        self.assertIn('Completed.', result.output)
        self.assertEqual(User.query.count(), 1)  # 唯一的管理员用户
        self.assertEqual(User.query.first().username, 'admin_username')
        self.assertTrue(User.query.first().validate_password('admin_password'))

        # 已经创建过管理员用户
        result = self.runner.invoke(
            args=['admin', '--username', 'admin_username_again', '--password', 'admin_password_again'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Completed.', result.output)
        self.assertEqual(User.query.count(), 1)  # 唯一的管理员用户
        self.assertEqual(User.query.first().username, 'admin_username_again')
        self.assertTrue(User.query.first().validate_password(
            'admin_password_again'))

    def test_admin_command_update(self):
        """ 测试更新管理员账户 """
        # 使用 args 参数给出完整的命令参数列表
        result = self.runner.invoke(args=['admin', '--username',
                                          'peter', '--password', 'updated_password'])
        self.assertIn('Updating user...', result.output)
        self.assertIn('Completed.', result.output)
        self.assertEqual(User.query.count(), 1)
        self.assertEqual(User.query.first().username, 'peter')
        self.assertTrue(
            User.query.first().validate_password('updated_password'))
```

在这几个测试中，大部分的断言是在检查执行命令后的数据库数据是否发生了正确的变化，或是判断命令行输出（ `result.output` ）的内容是否包含预期的字符。

### 运行测试

最后，在程序结尾添加下面的代码：

```python
if __name__ == "__main__":
    unittest.main()
```

在命令行下执行测试：

```powershell
(myenv) PS E:\PyCode\watchlist> python.exe .\test_watchlist.py
.............False
..
----------------------------------------------------------------------
Ran 15 tests in 3.028s

OK
```

如果测试出错，控制台会输出会看到详细的错误信息，就像之前的 `test_sayhello_to_somebody（）` 测试函数一样，进而可以有针对性的修复对应的程序代码，或是调整测试方法。

### 测试覆盖率

为了让程序更加强壮，可以添加更多、更完善的测试。那么，如何才能知道程序里有哪些代码还没有被测试？整体的测试覆盖率情况如何？我们可以使用 [Coverage.py](https://coverage.readthedocs.io/en/latest/) 来检查测试覆盖率，首先安装它：

```powershell
(myenv) PS E:\PyCode\watchlist> pip install coverage
# …………
Successfully installed coverage-5.2.1
```

使用下面的命令执行测试并检查测试覆盖率：

```powershell
(myenv) PS E:\PyCode\watchlist> coverage run --source=app .\test_watchlist.py
.............False
..
----------------------------------------------------------------------
Ran 15 tests in 3.538s

OK
```

因为只需要检查程序脚本 app.py 的测试覆盖率，所以使用 `--source=app` 选项来指定要检查的模块或包。

最后使用下面的命令查看覆盖率报告：

```powershell
(myenv) PS E:\PyCode\watchlist> coverage report
Name     Stmts   Miss  Cover
----------------------------
app.py     146      4    97%
```

从表格可以看出，一共有 157 行代码，没测试到的代码有 12 行，测试覆盖率为 92%。

还可以使用 `coverage html` 命令获取详细的 HTML 格式的覆盖率报告，它会在当前目录生成一个 htmlcov 文件夹，打开其中的 `index.html` 即可查看覆盖率报告。

同时在 `.gitignore` 文件后追加下面两行，忽略掉生成的覆盖率报告文件：

```
htmlcov/
.coverage
```

### 本章小结

通过测试后，我们就可以准备上线程序了。结束前，提交代码：

```powershell
$ git add .
$ git commit -m "Add unit test with unittest"
$ git push
```

### 进阶提示

* 访问 Coverage.py 文档（https://coverage.readthedocs.io）或执行 `coverage help` 命令来查看更多用法。
* 使用标准库中的 `unittest` 编写单元测试不是唯一选择，也可以使用第三方测试框架，比如 [pytest](https://pytest.org/) 。



## 第 10 章：组织你的代码

虽然程序开发已经完成，但随着功能的增多，把所有代码放在 app.py 里会让后续的开发和维护变得麻烦。这一章，对项目代码进行一次重构，让项目组织变得更加合理。

Flask 对项目结构没有固定要求，可以使用单脚本，也可以使用包。这一章通过使用包来组织程序。
先来看看目前的项目文件结构：

```powershell
(myenv) PS E:\PyCode\watchlist> tree /F
卷 作业 的文件夹 E:\PyCode\watchlist\ 列表
卷序列号为 2D97-AD94
│  .flaskenv
│  .gitignore
│  app.py
│  test_watchlist.py
├─static
│  │  favicon.ico
│  │  style.css
│  │
│  └─images
│          avatar.png
│          totoro.gif
└─templates
       404.html
       base.html
       edit.html
       index.html
       login.html
       settings.html
```

### 使用包组织代码

先在项目根目录创建一个 `watchlist` 文件夹作为包 (项目根目录可能也叫 `watchlist`，这并不冲突，到后面就会理解了)：

```powershell
mkdir watchlist
```

把 `static` 静态文件夹和 `templates` 模板文件夹移动到 `watchlist` 包文件夹中：

```powershell
watchlist
│
├─static
└─templates
```

把 app.py 中的代码按照类别分别放到多个模块，并把模块都放到包里，各模块和作用如下表所示：

|     模块      |           作业           |
| :-----------: | :----------------------: |
| `__init__.py` | 包构造文件，创建程序实例 |
|   views.py    |         视图函数         |
|   errors.py   |       错误处理函数       |
|   models.py   |          模型类          |
|  commands.py  |         命令函数         |

> 提示 除了包构造文件外，其他的模块文件名可以自由修改，比如 views.py 也可以叫 routes.py。

创建程序实例，初始化扩展的代码放到包构造文件里（`__init__.py`），如下所示：

```python
# -*- coding: utf-8 -*-
import os
import sys
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

WIN = sys.platform.startswith('win')
if WIN:  # Windows 环境下，三个斜杠
    prefix = 'sqlite:///'
else:
    prefix = 'sqlite:////'

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev'  # 等同于 app.secret_key = 'dev'

# 把 app.root_path 添加到 os.path.dirname() 中，以便把文件定位到项目根目录
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + \
    os.path.join(os.path.dirname(app.root_path), 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  # 关闭对模型的修改监控

# 在扩展类实例化前加载配置
db = SQLAlchemy(app)
login_manager = LoginManager(app)  # 实例化扩展类


@login_manager.user_loader
def load_user(user_id):  # 创建用户加载回调函数，接受用户 ID 作为参数
    from watchlist.models import User
    user = User.query.get(int(user_id))  # 用 ID 作为 User 模型的主键查询对应的用户
    return user  # 返回用户对象


login_manager.login_view = 'login'  # 重定向登录页面
login_manager.login_massage = 'You are not currently logged in, please log in your account first'  # 重定向登录页面提示


@app.context_processor
def inject_vars():  # 函数名可以随意修改
    """模板上下文处理函数"""
    from watchlist.models import User
    user = User.query.first()  # 用户对象
    if not user:
        user.name = 'Blood H'
    return locals()  # 需要返回字典


from watchlist import views, errors, commands
```

在构造文件中，为了让视图函数、错误处理函数和命令函数注册到程序实例上，需要在这里导入这几个模块。但是因为这几个模块同时也要导入构造文件中的程序实例，为了避免循环依赖（A 导入 B，B 导入 A），把这一行导入语句放到构造文件的结尾。同样的， `load_user()` 函数和 `inject_user()` 函数中使用的模型类也在函数内进行导入。

其他代码则按照分类分别放到各自的模块中，在移动代码之后，注意添加并更新导入语句，比如使用下面的导入语句来导入程序实例和扩展对象：

views.py：视图函数模块

```python
# -*- coding: utf-8 -*-
from flask.templating import render_template
from watchlist import app, db, login_manager
from flask import render_template, redirect, request, flash, url_for,
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from watchlist.models import User, Movie


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
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
    return render_template('login.html')


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
    if request.method == 'POST':
        name = request.form['name']
        if not name or len(name) > 20:
            flash('Invalid input.')
            return redirect(url_for('settings'))
        current_user.name = name
        print(current_user is User.query.first())
        # current_user 会返回当前登录用户的数据库记录对象
        # 等同于下面的用法
        # user = User.query.first()
        # user.name = name
        User.query.first().name = current_user.name
        db.session.commit()
        flash('Updated name.')
        # return redirect(url_for('index'))  # 重定向到首页
    return render_template('settings.html')


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':  # 判断是否是 POST 请求
        # 添加新条目，用户保护
        if not current_user.is_authenticated:  # 如果当前用户未认证
            flash(login_manager.login_massage)  # 传入登录提示
            return redirect(url_for('login'))  # 重定向到登录页面
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')  # 显示错误提示
            return redirect(url_for('index'))  # 重定向回主页
        # 保存表单数据到数据库
        movie = Movie(title=title, year=year)  # 创建记录
        db.session.add(movie)  # 添加到数据库会话
        db.session.commit()  # 提交数据库会话
        flash('Item created.')  # 显示成功创建的提示
        return redirect(url_for('index'))  # 重定向回主页
    movies = Movie.query.all()
    return render_template('index.html',  movies=movies)


@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 处理编辑表单的提交请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) > 4 or len(title) > 60:
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie)  # 传入被编辑的电影记录


@app.route('/movie/delete/<int:movie_id>', methods=['POST'])  # 限定只接受 POST 请求
@login_required  # 登录保护
def delete(movie_id):
    movie = Movie.query.get_or_404(movie_id)  # 获取电影记录
    db.session.delete(movie)  # 删除对应的记录
    db.session.commit()  # 提交数据库会话
    flash('Item deleted.')
    return redirect(url_for('index'))  # 重定向回主页
```

errors.py：错误处理模块

```python
# -*- coding: utf-8 -*-
from watchlist import app
from flask import render_template

@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    """Custom 404 Errors page"""
    response = render_template('404.html')
    return response, 404  # 返回响应和状态码
```

models.py：数据模型模块

```python
# -*- coding: utf-8 -*-
from watchlist import db
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)  # 主键
    name = db.Column(db.String(20))
    username = db.Column(db.String(20))  # 用户名
    password_hash = db.Column(db.String(128))  # 密码散列值

    def set_password(self, password):  # 用来设置密码的方法，接受密码作为参数
        self.password_hash = generate_password_hash(password)  # 将生成的密码保持到对应字段

    def validate_password(self, password):  # 用于验证密码的方法，接受密码作为参数
        return check_password_hash(self.password_hash, password)  # 返回布尔值


class Movie(db.Model):  # 表名 movie
    id = db.Column(db.Integer, primary_key=True)  # 主键
    title = db.Column(db.String(60))  # 电影标题
    year = db.Column(db.String(4))  # 电影年份
```

commands.py：命令函数模块

```python
# -*- coding: utf-8 -*-
import click
from watchlist import app, db
from watchlist.models import User, Movie

@app.cli.command()  # 注册为命令
@click.option('--drop', is_flag=True, help='Create after drop.')  # 设置选项
def initdb(drop):
    """Initialize the database"""
    if drop:
        db.drop_all()  # 删除数据表
    db.create_all()  # 创建数据表
    click.echo('Initialized database.')  # 输出提示信息


@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()  # 创建数据表

    # 虚拟电影条目数据
    movies = [
        {'title': 'My Neighbor Totoro', 'year': '1988'},
        {'title': 'Dead Poets Society', 'year': '1989'},
        {'title': 'A Perfect World', 'year': '1993'},
        {'title': 'Leon', 'year': '1994'},
        {'title': 'Mahjong', 'year': '1996'},
        {'title': 'Swallowtail Butterfly', 'year': '1996'},
        {'title': 'King of Comedy', 'year': '1999'},
        {'title': 'Devils on the Doorstep', 'year': '1999'},
        {'title': 'WALL-E', 'year': '2008'},
        {'title': 'The Pork of Music', 'year': '2012'},
    ]
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)
    db.session.commit()  # 提交更改
    click.echo('Generate fake data completed!')


@app.cli.command()
@click.option('--username', prompt=True, help='The username used to login.')
@click.option('--password', prompt=True, hide_input=True, confirmation_prompt=True, help='The password used to login.')
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    if user is not None:
        click.echo('Updating user...')
        user.username = username
        user.set_password(password)  # 设置密码
    else:
        click.echo('Creating user...')
        user = User(username=username, name='Blood Wong')
        user.set_password(password)  # 设置密码
    db.session.add(user)
    db.session.commit()  # 提交数据库会话
    click.echo('Completed.')
```

### 组织模板

模块文件夹 templates 下包含了多个模板文件，我们可以创建子文件夹来更好的组织它们。下面的操作创建了一个 errors 子文件夹，并把错误页面模板都移动到这个 errors 文件夹内（这些操作也可以使用文件管理器或编辑器完成）：

```powershell
$ cd templates # 切换到 templates 目录
$ mkdir errors # 创建 errors 文件夹
$ mv 404.html errors
```

因为错误页面放到了新的路径，所以需要修改错误处理函数中的模板文件路径，比如：

```python
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    """Custom 404 Errors page"""
    response = render_template('errors/404.html')
    return response, 404  # 返回响应和状态码
```

### 单元测试

也可以将测试文件拆分成多个模块，创建一个 tests 包来存储这些模块。但是因为目前的测试代码还比较少，所以暂时不做改动，只需要更新导入语句即可：

```python
from watchlist import app, db
from watchlist.models import User, Movie
from watchlist.commands import initdb, forge
```

因为要测试的目标改变，测试时的 `--source` 选项的值也要更新为包的名称 `watchlist` ：

```powershell
(myenv) PS E:\PyCode\watchlist> coverage run --source=watchlist test_watchlist.py
.............False
..
----------------------------------------------------------------------
Ran 15 tests in 3.896s

OK
```

> **提示：**可以创建配置文件来预先定义 `--source` 选项，避免每次执行命令都给出这个选项，具体可参考文档[配置文件章节](https://coverage.readthedocs.io/en/coverage-5.2.1/config.html)。

现在的测试覆盖率报告会显示包内的多个文件的覆盖率情况：

```powershell
(myenv) PS E:\PyCode\watchlist> coverage.exe report
Name                    Stmts   Miss  Cover
-------------------------------------------
watchlist\__init__.py      28      2    93%
watchlist\commands.py      32      0   100%
watchlist\errors.py         5      0   100%
watchlist\models.py        16      0   100%
watchlist\views.py         76      2    97%
-------------------------------------------
TOTAL                     157      4    97%
```

### 启动程序

因为现在使用包来组织程序，不再是 Flask 默认识别的 app.py，所以在启动开发服务器前需要使用环境变量 `FLASK_APP` 来给出程序实例所在的模块路径。因为程序实例在包构造文件内，所以直接写出包名称即可。在 `.flaskenv` 文件中添加下面这行代码：

```
FLASK_APP=watchlist
```

最终的项目文件结构如下所示：

```powershell
(myenv) PS E:\PyCode\watchlist> tree /F
卷 作业 的文件夹 PATH 列表
卷序列号为 2D97-AD94
E:.
│  .flaskenv
│  .gitignore
│  app.py  # 之前的单文件程序
│  test_watchlist.py
│
├─test_demo
│      module_foo.py
│      test_sayhello.py
│
└─watchlist  # 程序包
   │  commands.py
   │  errors.py
   │  models.py
   │  views.py
   │  __init__.py
   │
   ├─static
   │  │  favicon.ico
   │  │  style.css
   │  │
   │  └─images
   │          avatar.png
   │          totoro.gif
   │
   └─templates
      │  base.html
      │  edit.html
      │  index.html
      │  login.html
      │  settings.html
      │
      └─errors
              404.html

```

### 本章小结

对这个程序来说，这样的项目结构已经足够了。但对于大型项目，可以使用蓝本和工厂函数来进一步组织程序。

提交代码：

```powershell
$ git add .
$ git commit -m "Organize application with package"
$ git push
```

### 进阶提示

* [蓝本](https://flask.palletsprojects.com/en/1.0.x/blueprints/) 类似于子程序的概念，借助蓝本你可以把程序不同部分的代码分离开（比如按照功能划分为用户认证、管理后台等多个部分），即对程序进行模块化处理。每个蓝本可以拥有独立的子域名、URL 前缀、错误处理函数、模板和静态文件。
* [工厂函数](https://flask.palletsprojects.com/en/1.0.x/patterns/appfactories/) 就是创建程序的函数。在工厂函数内，我们先创建程序实例，并在函数内完成初始化扩展、注册视图函数等一系列操作，最后返回可以直接运行的程序实例。工厂函数可以接受配置名称作为参数，在内部加载对应的配置文件，这样就可以实现按需创建加载不同配置的程序实例，比如在测试时调用工厂函数创建一个测试用的程序实例。



## 第 10.1 章：项目完善

现在这个程序已经差不多了，但仍然有些地方需要改进，比如：

* 只处理了 404 HTTP 异常，还有 400、500 等 HTPP 异常 需要处理
* 没有创建管理员用户时，页面标题的名称不显示，还有用户名和密码的不规范，应该限制敏感字符，如空格，斜线等特殊字符。
* 添加、编辑条目、更改设置、用户登录功能的表单均使用 HTML 代码实现，应该使用 [Flask-WTF](https://flask-wtf.readthedocs.io/en/stable/) 扩展来简化表单的处理 【自动生成表单、验证表单数据、CSRF (跨站请求伪造) 保护】
* 使用 静态代码检查工具 [Flake8](https://flake8.pycqa.org/en/latest/) 和 代码格式化工具 [yapf](https://github.com/google/yapf) 来提高代码的质量

### HTTP 错误处理

之前在视图函数 `page_not_found()` 中对 `404 Page Not Found` 错误进行了处理，编写了 404 错误的模板 `404.html` ，并在产生该错误时渲染返回响应到客户端。

 通常我们会为不同的 HTTP 错误编写各自的的错误处理函数，以便返回不同的响应。 但也也可以编写一个统一的错误处理函数，这个函数会处理所有的 HTTP 错误，只需要在装饰器内传入 Exception 类即可 。

下面更改原本的 `page_not_found()` 视图函数改为 `app.errorhandler()` (包括装饰器)，`errors.py` 模块中：

```python
from werkzeug.exceptions import HTTPException  # HTTP 异常类

@app.errorhandler(Exception)
def all_exception_handler(e):
    """ 处理所有的 HTTP 错误 """
    # 对于 HTTP 异常，返回自带的错误描述和状态码
    # 这些异常类在 Werkzeug 中定义，均继承 HTTPException 类
    if isinstance(e, HTTPException):
        result = render_template(
            'errors/error.html', description=e.description), e.code
    else:
        # 500 未知异常
        result = render_template(
            'errors/error.html', description='Sorry, internal error.'), 500
    return result  # 返回响应和 状态码
```

首先导入 `werkzeug.exceptions` 中的 `HTTPException` 异常类 ，然后使用 `app.errorhandler()` 装饰器注册错误处理函数，传入 HTTP 错误状态码或是特定的异常类， 这里传入了 异常基类 `Exception` 来捕捉所有的错误，因为任何错误都是 `Exception`  类的子类，接受再判断当前发生的错误实例 `e` 是否为 HTTP 错误 `HTTPException` 的实例，从而区分 HTTP 错误和未知错误的区分。（未知错误是指 500 错误）

 错误处理的小知识： 

*  对于一般的程序异常（如 `NameError`），如果没有特定的异常处理函数，默认都会触发 500 错误处理函数。 
*  开启调试模式的时候，500 错误会显示错误调试页面。 

*  500 错误发生时传入错误处理函数的是真正的异常对象，不是 Werkzeug 内置的 HTTP 异常类。 
*  开启调试模式的时候，500 错误会显示错误调试页面。 
*  Werkzeug 内置的 HTTP 异常类的 description 和 code 属性分别返回错误描述和状态码。 

因此，只需要将捕捉到的 HTTP 错误的 错误描述传入 `error.html` 错误模板渲染，并将渲染后的响应和状态码返回到客户端，下面编辑 错误模板 `error.html`：

直接重命名之前的 404 错误模板 `404.html` 为 `error.html`，内容如下：

```html
{% extends 'base.html' %}

{% block content %}
<ul class="movie-list">
    <li>
        <h3>{{ description }}</h3>
    </li>
    <li class="error-gohome">
        <a href="{{ url_for('index') }}">
            Go Home
        </a>
    </li>
</ul>
{% endblock %}
```

`class` 属性 `"error-gohemo"` 的 css 样式：

```css
.movie-list .error-gohome{  /* HTTP 异常，返回首页 */
    display: flex;
    flex-direction: row;
    justify-content: center;
}
```

现在，每当有错误产生时都会被 `all_exception_handle()` 函数捕捉，并错误实例 `e` 的错误描述 `e.exception` 和 错误状态码 `e.code` 渲染后返回给客户端。不同的错误所产生的实例也是不同的，模板渲染的结果也不相同。

这样子就只使用一个错误处理函数和一个错误模板，实现了所有异常的处理。

* 最后，可以将 `error.html` 移到 templates 目录下，errors 子目录就不需要了，因为仅有一个模板。
* 那么 `all_exception_handle()` 函数中的模板路径也要随之更改为 `'error.html'` 。

下面是对 HTTP 错误 的单元测试，将 `test_404_page()` 测试函数改为 `test_exception_handler()` 函数：

```python
class WatchlistTestCase(unittest.TestCase):
    """ watchlist 程序测试"""
	# …………

    def test_exception_handler(self):
        """ All HTTP Exception Test Function """
        # 测试 404 错误，访问页面不存在
        response = self.client.get('/nothing')  # Get 方法访问 URL 路由
        data = response.get_data(as_text=True)  # 获取 Unicode 格式的响应主体
        # 判断是否包含预期值
        self.assertIn('The requested URL was not found on the server.', data)
        self.assertIn('Go Home', data)
        self.assertEqual(response.status_code, 404)  # 判断响应状态码

        # 测试 405 错误，请求方法不接受
        response = self.client.post('/logout')
        data = response.get_data(as_text=True)
        self.assertIn('The method is not allowed for the requested URL.', data)
        self.assertEqual(response.status_code, 405)  # 判断响应状态码

        # 测试 400 错误，语义有误 或请求参数有误、
        response = self.client.post('/login',
                                    data=dict(title='admin', year='admin'),
                                    follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertIn(
            'The browser (or proxy) sent a request that this server could not understand.',
            data)
        self.assertEqual(response.status_code, 400)  # 判断响应状态码

        # 测试 500 错误，通常是服务器端的源代码出现错误时出现
        response = self.client.post('/movie/edit/1',
                                    data=dict(title='Annie Hall', year='1977'),
                                    follow_redirects=True)
        data = response.get_data(as_text=True)
        self.assertNotEqual(response.status_code, 500)  # 判断响应状态码
```

### 用户模型修复

在程序的每个页面中 `<title>` 标签中的标签名 和 `<h2>` 标签中的页面标题的名称都来自于首个 User 对象的字段属性 `name` ，这就存在一个问题，当没有创建管理员用户名的时候 页面标题中的名称就就会报错，因为这时候的 User 对象根本就不存在，其属性 `name` 自然也就不存在。

为了解决这一问题，不妨在没有任何用户名时将传入基模板一个保护 `name` 属性的 用户对象即可。

#### 页面标题名称

传入基模板的用户对象只需在上下文函数中创建即可，不需要更改用户模型

`__init__.py` ：模板上下文函数

```python
@app.context_processor
def inject_vars():  # 函数名可以随意修改
    """模板上下文处理函数"""
    name = None
    from watchlist.models import User
    user = User.query.first()  # 用户对象
    if not user:
        name = 'BL00D'
    else:
        name = user.name
    return locals()  # 需要返回字典
```

这样当数据库中没有管理员用户时页面标题则会显示在上下文函数中已经预定义的页面标题名称。

#### 用户名和密码规范

用户名：大小写字母与阿拉伯数字的组合，无空格和字符

密码：密码的对方与用户名规范相同

models.py：在 User 用户模型类中定义用户名和密码的验证方法 `valid_username()` 和 `valid_password()`，同时在增加 `set_username()` 和 `set_name()` 方法实现用户名和页面名称的设置，User 模型更改如下：

```python
# …………

class User(db.Model, UserMixin):  # 表名将会是 user（自动生成，小写处理）
    # …………

    def set_name(self, name):
        self.name = name

    def set_username(self, username):
        self.username = username

    def valid_username(self, username):
        valid_length = 0 < len(username) and len(username) <= 20
        ret = valid_length and username.isalnum()  # 内置函数，判断字符串是否只含字母和数字
        return ret

    def valid_password(self, password):
        valid_length = 0 < len(password) and len(password) <= 20
        ret = valid_length and password.isalnum()  # 判断字符串是否为字母和数字组合
        return ret
```

**更改初始化管理员用户**

`commands.py` ：`admin()` 命令函数，设置管理员

```python
# …………
def admin(username, password):
    """Create user."""
    db.create_all()
    user = User.query.first()
    massage = 'Invalid username or password.'
    if user is not None:
        click.echo('Updating user...')
    else:
        user = User()
        click.echo('Creating user...')
    if user.valid_username(username) and user.valid_password(password):
        user.set_name('BL00D')
        user.set_username(username)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()  # 提交数据库会话
        massage = 'The superuser definition successful.'
    else:
        massage = 'The superuser definition failed.'
    click.echo(str(massage))
```

创建管理员的命令并提供页面标题名称 的输入，而是为它初始化了一个值。这样当上下文函数在获取数据库中用户的时候就 `name` 属性始终未这个 预设的值，同时也可以登录过后在 `/settings` URL 中 对 其进行修改。

### Flask-WTF 实现表单

Flask-WTF 是集成 WTForms，并带有 `csrf` 令牌的安全表单和全局的 `csrf `保护的功能。 每次当在建立表单所创建的类都是继承与 `flask_wtf` 中的 FlaskForm，而 FlaskForm 是继承 WTForms 中 forms。

使用 WTForms 能够极大的简化表单的编写，不必为每一个表单编写 HTML 代码，WTForms 会根据 定义的表单模型来自动生成表单。每个 WTForms 模型都由一个或多个字段组成（也就是 HTML 表单中的控件），使用同一个表单模型，渲染模型中不同的字段，即可生成不同的表单。例如：电影条目 `Movie` 的添加和编辑操作就只需要定义一个表单模板即可实现。

首先在环境中安装 Flask-WTF 扩展：

```powershell
pip install flask-wtf
```

**创建基础表单，form.py**

```python
class LoginForm(FlaskForm):
    username = StringField()
    password = PasswordField()
    remember_me = BooleanField(label='Keep me logged in')
```

**CSRF保护**

任何使用 FlaskForm 创建的表单发送请求，都会有 CSRF 的全部保护，在对应的 template 中HTML渲染表单时，可以加入 `{{ form.csrf_token }}`：

```xml
<form method="post">
    {{ form.csrf_token }}
</form
```

但是如果模板中没有表单，则可以使用一个隐藏的 input 标签加入 `{{ form.csrf_token }}`。

```xml
<form method="post">
    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>
</form>
```

**验证表单**

在视图处理程序中验证请求：view.py

```python
def login():
    form = LoginForm()
    if form.validate_on_submit():
        return redirect('/success')
    return render_template('login.html', form=form)
```

使用`validate_on_submit` 来检查是否是一个 POST 请求并且请求是否有效。

**文件上传**

Flask-WTF 提供 [`FileField`](https://wizardforcel.gitbooks.io/flask-extension-docs/content/api.html#flask_wtf.file.FileField) 来处理文件上传，它在表单提交后，自动从 `flask.request.files` 中抽取数据。[`FileField`](https://wizardforcel.gitbooks.io/flask-extension-docs/content/api.html#flask_wtf.file.FileField) 的 `data` 属性是一个 Werkzeug FileStorage 实例。

```python
from werkzeug import secure_filename
from flask_wtf.file import FileField

class PhotoForm(Form):
    photo = FileField('Your photo')

@app.route('/upload/', methods=('GET', 'POST'))
def upload():
    form = PhotoForm()
    if form.validate_on_submit():
        filename = secure_filename(form.photo.data.filename)
        form.photo.data.save('uploads/' + filename)
    else:
        filename = None
    return render_template('upload.html', form=form, filename=filename)
```

注意：在 HTML 表单的 enctype 设置成 multipart/form-data，如下:

```xml
<form action="/upload/" method="POST" enctype="multipart/form-data">
    ....
</form>
```

**验证码**

Flask-WTF 通过 `RecaptchaField` 也提供对验证码的支持:

```python
from flask_wtf import Form, RecaptchaField
from wtforms import TextField

class SignupForm(Form):
    username = TextField('Username')
    recaptcha = RecaptchaField()
```

还需要配置一下信息：

| 字段                  | 配置                                                         |
| --------------------- | ------------------------------------------------------------ |
| RECAPTCHA_PUBLIC_KEY  | **必须** 公钥                                                |
| RECAPTCHA_PRIVATE_KEY | **必须** 私钥                                                |
| RECAPTCHA_API_SERVER  | **可选** 验证码 API 服务器                                   |
| RECAPTCHA_PARAMETERS  | **可选** 一个 JavaScript（api.js）参数的字典                 |
| bRECAPTCHA_DATA_ATTRS | **可选** 一个数据属性项列表 https://developers.google.com/recaptcha/docs/display |

**由于表单不止一个，可能很多，所以在 包文件夹 `watchlist` 中新建表单模块 `forms.py` ，用于存放所有表单的模型和自定义函数等。**

#### 添加条目表单

forms.py：添加条目表单模型

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired, ValidationError


class MovieForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    year = StringField('Year', validators=[DataRequired()])
    submit_add = SubmitField('Add')
    submit_edit = SubmitField('Edit')
```

这里的电影条目表单有两个按钮控件 `submit_add` 和 `submit_edit` ，作为添加条目 和 编辑条目的触发按钮，

在 view.html 模块中更改 视图函数 `index()` 如下：

```python
from watchlist.forms import MovieForm

# …………

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
        # 获取表单数据
        title = request.form.get('title')  # 传入表单对应输入字段的 name 值
        year = request.form.get('year')
        # 验证数据
        if not title or not year or len(year) != 4 or len(
                title) > 60 or not only_number(year):
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
```

下面是模板中更改条目表单的定义：index.html

```html
<p>{{ movies|length }} Titles</p>

{% if current_user.is_authenticated %}
<form method="post">
    {{ form.hidden_tag() }}
    {{ form.title.label }}&nbsp;{{ form.title() }}&nbsp;
    {{ form.year.label }}&nbsp;{{ form.year() }}&nbsp;
    {{ form.submit_add() }}
</form>
{% endif %}
```

渲染结果如下：

<form method="post">
    <input id="csrf_token" name="csrf_token" type="hidden" value="IjkwMzJmODRmN2QxZmM4ZGI5MzA5NzllOWM2NGY4MTIxYWIzYTNhY2Ui.XywJWw.kPsB-GaxZS4cWcmppYslKaLr0FQ">
    <input id="csrf_token" name="csrf_token" type="hidden" value="IjkwMzJmODRmN2QxZmM4ZGI5MzA5NzllOWM2NGY4MTIxYWIzYTNhY2Ui.XywJWw.kPsB-GaxZS4cWcmppYslKaLr0FQ">
    <label for="title">Title</label>&nbsp;<input id="title" name="title" required type="text" value="">&nbsp;
    <label for="year">Year</label>&nbsp;<input id="year" name="year" required type="text" value="">&nbsp;
    <input id="submit_add" name="submit_add" type="submit" value="Add">
</form>

#### 编辑条目表单

编辑条目表单直接使用 电影条目表单模型 `MovieForm` ，只需在模板中为其渲染 `submit_edit` 按钮即可。

index.py：更改编辑条目视图函数定义：

```python
from watchlist.forms import MovieForm
# …………

@app.route('/movie/edit/<int:movie_id>', methods=['GET', 'POST'])
@login_required  # 登录保护
def edit(movie_id):
    form = MovieForm()
    movie = Movie.query.get_or_404(movie_id)
    if request.method == 'POST':  # 验证 POST 请求
        # if request.method == 'POST' and form.validate():  # 验证 POST 请求
        title = request.form['title']
        year = request.form['year']
        if not title or not year or len(year) != 4 or len(
                title) > 60 or not only_number(year):
            flash('Invalid input.')
            return redirect(url_for('edit', movie_id=movie_id))  # 重定向回对应的编辑页面
        movie.title = title  # 更新标题
        movie.year = year  # 更新年份
        db.session.commit()  # 提交数据库会话
        flash('Item updated.')
        return redirect(url_for('index'))  # 重定向回主页
    return render_template('edit.html', movie=movie, form=form)  # 传入被编辑的电影记录
```

edit.html：更改编辑条目表单的模板定义，默认显示当前条目的信息

```html
# …………

{% block content %}
<h3>Edit item</h3>
<form method="post">
    {{ form.hidden_tag() }}
    {{ form.title.label }}&nbsp;{{ form.title(value=movie.title) }}&nbsp;
    {{ form.year.label }}&nbsp;{{ form.year(value=movie.year) }}&nbsp;
    {{ form.submit_edit() }}
</form>
{% endblock %}
```

渲染结果如下：

<form method="post">
    <input id="csrf_token" name="csrf_token" type="hidden" value="IjkwMzJmODRmN2QxZmM4ZGI5MzA5NzllOWM2NGY4MTIxYWIzYTNhY2Ui.XyxEwQ.XThBN6Y2HV8yqDQJB3_pXs8sV-E">
    <input id="csrf_token" name="csrf_token" type="hidden" value="IjkwMzJmODRmN2QxZmM4ZGI5MzA5NzllOWM2NGY4MTIxYWIzYTNhY2Ui.XyxEwQ.XThBN6Y2HV8yqDQJB3_pXs8sV-E">
    <label for="title">Title</label>&nbsp;<input id="title" name="title" required type="text" value="Annie Hall">&nbsp;
    <label for="year">Year</label>&nbsp;<input id="year" name="year" required type="text" value="1977">&nbsp;
    <input id="submit_edit" name="submit_edit" type="submit" value="Edit">
</form>

#### settings 页面表单

新建用户对象的表单模型 `UserForm` ，因为单用户系统 所以不需要提高更新用户名和密码的功能。

forms.py：用户表单模型

```python
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField
# …………

class UserForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired()])
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')
```

settings.html：在模板中更改表单的定义

```html
<!-- 略………… -->

<form method="post">
    {{ form.hidden_tag() }}
    <p>
        {{ form.name.label }}&nbsp;
        {{ form.name(value=user.name) }}
    </p>
    <p>{{ form.submit() }}</p>
</form>
```

views.py：更改 `settings()` 视图函数，创建并生成表单

```python
from watchlist.forms import UserForm
# …………

@app.route('/settings', methods=['GET', 'POST'])
@login_required  # 视图保护
def settings():
    form = UserForm()
    if form.validate_on_submit():  # 验证 POST 请求
        # …………
    return render_template('settings.html', form=form)
```

渲染结果（需登录用户）：

<h3>Settings</h3>
<form method="post">
    <input id="csrf_token" name="csrf_token" type="hidden" value="IjNjZjY5OWViNTBmZDAwZjY2YjllYWRlOWFkYWRjN2QxOTg1OGM4MTMi.XzO1JA.0aakQF-W16JTuadJ7tMSv8Sf5ds">
    <p>
        <label for="name">Your Name</label>&nbsp;
        <input id="name" name="name" required type="text" value="BL00D">
    </p>
    <p><input id="submit" name="submit" type="submit" value="Submit"></p>
</form>

#### login 登录页面

login.html：在模板中更改表单的定义

```html
<!-- 略………… -->

<h3>Login</h3>
<form method="post">
    {{ form.hidden_tag() }}
    {{ form.csrf_token }}
    <p>
        {{ form.username.label }}<br>
        {{ form.username() }}
    </p>
    <p>
        {{ form.password.label }}<br>
        {{ form.password() }}
    </p>
    <p>{{ form.submit() }}</p>
</form>
```

利用 `UserForm` 表单模型生成用户登录页面

views.py：更改 `login()` 视图函数，创建并生成表单

```python
from watchlist.forms import UserForm
# …………

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = UserForm()
    if request.method == 'POST':  # 验证 POST 请求
        # …………
    return render_template('login.html', form=form)
```

渲染结果（未登录用户时可见）：

<h3>Login</h3>
<form method="post">
    <input id="csrf_token" name="csrf_token" type="hidden" value="Ijk2Y2U4YTQ4OTNmMjQ5MGM5M2JkMGJiY2M2ZWI1OGFkZGQ1ZGViZmYi.XzFhIA.24ROJdHXxO3-FPnGLSjGEKBGx2U">
    <input id="csrf_token" name="csrf_token" type="hidden" value="Ijk2Y2U4YTQ4OTNmMjQ5MGM5M2JkMGJiY2M2ZWI1OGFkZGQ1ZGViZmYi.XzFhIA.24ROJdHXxO3-FPnGLSjGEKBGx2U">
    <p>
        <label for="username">Username</label><br>
        <input id="username" name="username" required type="text" value="">
    </p>
    <p>
        <label for="password">Password</label><br>
        <input id="password" name="password" required type="password" value="">
    </p>
    <p><input id="submit" name="submit" type="submit" value="Submit"></p>
</form>

### 代码质量优化

随着程序功能不断的完善，代码量也慢慢变大，为了写出优美且工整的代码，可以使用 静态代码检查工具 和 代码格式化工具 的组合来提高代码的质量。

**Flake8 - 静态代码检查**

> **Flake8** 是由Python官方发布的一款辅助检测Python代码是否规范的工具，相对于目前热度比较高的Pylint来说，Flake8检查规则灵活，支持集成额外插件，扩展性强。Flake8是对下面三个工具的封装：
>
> - PyFlakes：静态检查Python代码逻辑错误的工具。
> - Pep8： 静态检查PEP8编码风格的工具。
> - NedBatchelder’s McCabe script：静态分析Python代码复杂度的工具。
>
> 不光对以上三个工具的封装，Flake8还提供了扩展的开发接口。
>
> 官方文档：https://pypi.python.org/pypi/flake8/

**yapf - 代码格式化工具**

YAPF（Yet Another Python Formatter）是Google开源的一个用来格式化Python代码的工具，可以一键美化代码。支持2种代码规范：

- PEP8
- Google style

**安装 flake8 和 yapf**

打开命令行，按照下面的安装步骤：

- ① 在 命令行 输入`pip3 list`，检查是否已存在需要的包
- ② 继续输入`pip3 install flake8`，下载安装 flake8
- ③ 继续输入`pip3 install yapf`，下载安装 yapf

安装好 flake8 和 yapf 后（这里默认VS Code已经装好了Python插件），打开VS Code的 **用户设置（setting.json）**，在里面添加下面的代码：

```json
{
    // …………
    
    "python.linting.flake8Enabled": true,
    "python.formatting.provider": "yapf",
    "python.linting.flake8Args": ["--max-line-length=248"], # 设置单行最长字符限制
    "python.linting.pylintEnabled": false # 关闭pylint工具
}
```

**为什么需要设置单行最长字符限制？** 

在使用静态代码检查工具 flake8 来规范python代码时，当 **一行字符超过79个** 时会出现提示 

flake8有个 `--max-line-length=n` 配置选项可用来 **设置单行最长字符限制** 

所以要在 flake8 的参数设置中更改单行最大字符数，` "python.linting.flake8Args": [ 参数列表 ]` 

**代码格式化**

VS Code 格式化代码的快捷键 **Shift + Alt + F**

### 本章小结

完善项目后，对新的功能或操作进行单元测试，通过测试信息来修复程序中出现的错误。

```powershell
(myenv) PS E:\PyCode\watchlist> coverage.exe run --source=watchlist .\test_watchlist.py
...............
----------------------------------------------------------------------
Ran 15 tests in 3.814s

OK
(myenv) PS E:\PyCode\watchlist> coverage.exe report
Name                    Stmts   Miss  Cover
-------------------------------------------
watchlist\__init__.py      29      0   100%
watchlist\commands.py      36      0   100%
watchlist\errors.py         8      0   100%
watchlist\forms.py         13      0   100%
watchlist\models.py        28      0   100%
watchlist\views.py         85      0   100%
-------------------------------------------
TOTAL                     199      0   100%
```

程序没有问题就可以提交代码了：

```powershell
$ git add .
$ git commit -m "Add HTTP errors, Page title name and Forms with Flask-WTF."
$ git push
```

```powershell
 (myenv) PS E:\PyCode\watchlist> pip freeze > requirements.txt
```



##  第 11 章：部署上线

把程序部署到互联网上，让网络中的其他所有人都可以访问到。

Web 程序通常有两种部署方式：传统部署和云部署。传统部署指的是在使用物理主机或虚拟主机上部署程序，这通常需要在一个 Linux 系统上完成所有的部署操作；云部署则是使用其他公司提供的云平台，这些平台为你设置好了底层服务，包括Web 服务器、数据库等等，只需要上传代码并进行一些简单设置即可完成部署。这一章介绍使用云平台 [PythonAnywhere](https://www.pythonanywhere.com/) 来部署程序。

### 部署前的准备

首先，需要生成一个依赖列表，方便在部署环境里安装。使用下面的命令把当前依赖列表写到一个requirements.txt 文件里：

```powershell
 (myenv) PS E:\PyCode\watchlist> pip freeze > requirements.txt
```

requirements.txt：

```bash
click==7.1.2
Flask==1.1.2
Flask-Login==0.5.
Flask-SQLAlchemy==2.4.4
Flask-WTF==0.14.3
itsdangerous==1.1.0
Jinja2==2.11.2
MarkupSafe @ file:///C:/ci/markupsafe_1594405949945/work
python-dotenv==0.14.0
SQLAlchemy==1.3.18
sqlparse==0.3.1
Werkzeug==1.0.1
WTForms==2.3.3
```

对于某些配置，生产环境下需要使用不同的值。为了让配置更加灵活，把需要在生产环境下使用的配置改为优先从环境变量中读取，如果没有读取到，则使用默认值：

```python
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev')
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(os.path.dirname(app.root_path), os.getenv('DATABASE_FILE', 'data.db'))
```

以第一个配置变量为例， `os.getenv('SECRET_KEY', 'dev')` 表示读取系统环境变量 `SECRET_KEY` 的值，如果没有获取到，则使用 `dev` 。

> 注意 
>
> 像密钥这种敏感信息，保存到环境变量中要比直接写在代码中更加安全。

对于第二个配置变量，仅改动了最后的数据库文件名。在示例程序里，因为部署后将继续使用 SQLite，所以只需要为生产环境设置不同的数据库文件名，否则的话，可以像密钥一样设置优先从环境变量读取整个数据库 URL。

在部署程序时，不会使用 Flask 内置的开发服务器运行程序，因此，对于写到 `.env` 文件的环境变量，需要手动使用 `python-dotenv` 导入。下面在项目根目录创建一个 wsgi.py 脚本，在这个脚本中加载环境变量，并导入程序实例以供部署时使用：

wsgi.py：手动设置环境变量并导入程序实例

```python
import os
from dotenv import load_dotenv


dotenv_path = os.path.join(os.path.dirname(__file__), '.env')
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

from watchlist import app
```

这两个环境变量的具体定义，将在远程服务器环境创建新的 `.env` 文件写入。

最后把改动提交到 Git 仓库，并推送到 GitHub 上的远程仓库：

```powershell
$ git add .
$ git commit -m "Ready to deploy"
$ git push
```

### 使用 PythonAnywhere 部署程序

首先访问注册页面注册一个免费账户。注册时填入的用户名将作为程序域名的子域部分，以及分配给你的 Linux 用户名。比如，如果用户名为 `BL00D`，最终分配的程序域名就是 http://BL00D.pythonanywhere.com/ 。注册完成后会有一个简单的教程，可以跳过，也可以跟着了解一下基本用法。

导航栏包含几个常用的链接，可以打开其他面板：

* Consoles（控制台）：可以打开 Bash、Python Shell、MySQL 等常用的控制台
* Files（文件）：创建、删除、编辑、上传文件，你可以在这里直接修改代码
* Web：管理 Web 程序
* Tasks（任务）：创建计划任务
* Databases（数据库）：设置数据库，免费账户可以使用 MySQL

> 这些链接对应页面的某些功能也可以直接在管理面板主页打开。

**Web 应用创建**

1. 首先，创建一个 Web 程序，可以点击导航栏的 Web 链接，或是主页上的“Open Web tab”按钮打开 Web 面板
2. 点击“Add a new web app”按钮创建 Web 程序，**Your web app's domain name** 提示升级账户后可以自定义域名，直接点击“Next”按钮跳到下一步
3. 跳转到 **Select a Python Web framework** 窗口，这一步选择 Web 框架，为了获得更灵活的控制，选择手动设置（Manual configuration）
4. 然后在 **Select a Python version** 窗口接着选择要使用的 Python 版本（我用的 Python 3.8）
5. 最后点击“Next”按钮即可完成创建 Web 程序流程

接下来需要进行一系列程序初始化操作，最后再回到 Web 面板进行具体的设置。

### 初始化程序运行环境

首先要考虑把代码上传到 PythonAnywhere 的服务器上。上传代码一般有两种方式：

* 从 GitHub 拉取我们的程序
* 在本地将代码存储为压缩文件，然后在 Files 标签页上传压缩包

因为代码已经推送到 GitHub 上，这里将采用第一种方式。首先通过管理面  板主页的“Bash”按钮或是 Consoles 面板下的“Bash”链接创建一个命令行会话，在命令行下输入下面的命令：

```bash
$ git clone https://github.com/HEY-BLOOD/watchlist.git  # 注意替换 Git 仓库地址
$ cd watchlist # 切换进程序仓库
```

这会把程序代码克隆到 PythonAnywhere 为你分配的用户目录中，路径即 `/home/你的 PythonAnywhere 用户名/你的仓库名称` ，比如 `/home/BL00D/watchlist` 。

下面我们在项目根目录创建 `.env` 文件，并写入生产环境下需要设置的两个环境变量。其中，密钥（ SECRET_KEY ）的值是随机字符串，可以使用 `uuid` 模块来生成：

```python
$ python3
>>> import uuid
>>> uuid.uuid4().hex
'812efe2e831f47b5afefd723b2e48465'
```

复制生成的随机字符备用，接着创建 `.env` 文件：

```bash
$ vim .env
```

写入设置密钥和数据库名称的环境变量：

```bash
SECRET_KEY=812efe2e831f47b5afefd723b2e48465
DATABASE_FILE=data-prod.db
```

最后安装依赖并执行初始化操作：

```bash
$ python3 -m venv env # 创建虚拟环境
$ . env/bin/activate # 激活虚拟环境
(env) $ pip install -r requirements.txt # 安装所有依赖
(env) $ flask initdb # 初始化数据库
(env) $ flask admin # 创建管理员账户
```

先不要关闭这个标签页，后面还要在这里执行一些命令。点击右上角的菜单按钮，并在浏览器的新标签页打开 Web 面板。

### 设置并启动程序

代码部分已经设置完毕，接下来进行一些简单设置就可以启动程序了。

**代码**
回到 Web 标签页，先来设置 Code 部分的配置

点击源码（Source code）和工作目录（Working directory）后的路径并填入项目根目录，目录规则为“/home/用户名/项目文件夹名”。

```bash
/home/BL00D/watchlist/
```

点击 WSGI 配置文件（WSGI configuration file）后的链接打开编辑页面，删掉这个文件内的所有内容，填入下面的代码：

```python
import sys

path = '/home/BL00D/watchlist'  # 路径规则为 /home/你的用户名/项目文件夹名
if path not in sys.path:
	sys.path.append(path)
    
from wsgi import app as application
```

完成后点击绿色的 Save 按钮或按下 Ctrl+S 保存修改，点击右上角的菜单按钮返回 Web 面板。

PythonAnywhere 会自动从这个文件里导入名称为 application 的程序实例，所以我们从项目目录的 **wsgi** 模块中导入程序实例 `app` ，并将名称映射为 `application` 。

**虚拟环境**

为了让程序正确运行，我们需要在 Virtualenv 部分填入虚拟环境文件夹的路径

```bash
/home/BL00D/watchlist/env/
```

对应我们的项目就是 `/home/BL00D/watchlist/env/` ，注意替换其中的用户名、项目名称和虚拟环境名称部分。点击 **Virtualenv** 部分的红色字体链接，填入并保存。

**静态文件**

静态文件可以交给 PythonAnywhere 设置的服务器来处理，这样会更高效。要让PythonAnywhere 处理静态文件，只需要在 Static files 部分指定静态文件 URL 和对应的静态文件文件夹目录

URL：`/static/`

Directory：`/home/BL00D/watchlist/watchlist/static/`

注意目录中的用户名和项目文件夹名称。

**启动程序**

一切就绪，点击绿色的重载按钮即可让配置生效，访问程序网址“https://用户名.pythonanywhere.com”（Web 面板顶部的链接），比如https://BL00D.pythonanywhere.com 即可访问程序。

最后还要注意的是，免费账户需要每三个月点击一次黄色的激活按钮（在过期前会收到提醒邮件）

**更新部署后的程序**

当需要更新程序时，流程和部署类似。在本地完成更新，确保程序通过测试后，将代码推送到 GitHub 上的远程仓库。登录到 PythonAnywhere，打开一个命令行会话（Bash），切换到项目目录，使用 git pull 命令从远程仓库拉取更新：

```python
$ cd ~/watchlist
$ git pull
```

