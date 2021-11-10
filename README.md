# LFT
这是一个用于老师评价以及查询的网站，可在该网站上查询南开大学计算机学院的老师，进行评价和信息浏览。

开发者：
[double静](https://github.com/king-wk) 🎄 [中药](https://github.com/Pixie-King) 🍟 [樱疼](https://github.com/JARVISHHH) ✈ [小居](https://github.com/tolstoy-yun)


## Getting start
进入项目所在目录下。

首先，我们安装所有的依赖包。
```
pip install -r requirements.txt
```

以下命令进行了环境的设置以及应用的运行。

在 Bash 下：
```
$ export FLASK_APP=flaskr
$ export FLASK_ENV=development
$ flask run
```

在 CMD 下：
```
> set FLASK_APP=flaskr
> set FLASK_ENV=development
> flask run
```

在 Powershell 下：
```
> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
> flask run
```

运行正确时应该有如下输出：
```
* Serving Flask app "flaskr"
* Environment: development
* Debug mode: on
* Running on http://127.0.0.1:5000/ (Press CTRL+C to quit)
* Restarting with stat
* Debugger is active!
* Debugger PIN: 855-212-761
```

在浏览器中打开`http://127.0.0.1:5000/index`，进入寻师问道网站主页。



## Initialize and check database

完成上面的步骤之后，可以在终端中输入以下命令。该命令会初始化整个数据库（数据库中的数据会变成我们设定好的一些数据，主要是为了方便之后的单元测试）。

(在运行下面初始化数据库的命令之前，仍然需要先运行下面这两句配置环境)
```
> $env:FLASK_APP = "flaskr"
> $env:FLASK_ENV = "development"
```

```
flask init-db
```
如果初始化成功，会显示`Initialized the database.`。

完成后，能够看到新建了一个`instance`文件夹（因为我之前运行过了，现在已经有这个文件夹了。可以把这整个文件夹都删掉再试试效果），文件夹下有一个`.sqlite`文件，该文件就是我们的数据库文件。

使用目录下的`SQLiteSpy.exe`软件打开这个文件，可以查看我们的数据库。



## Unit Test

每次运行单元测试之前，需要先初始化数据库，即运行`flask init-db`，之后再进行单元测试。

运行下面的命令行就可以进行单元测试，并输出覆盖率。

```
pytest --cov
```

