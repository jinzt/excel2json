# 简介
工具是根据 https://github.com/zdhsoft/excel2json 修改而来，非常感谢原作者。


## 工具
excel表配置主要有tablelist标签页和其它内容标签页构成。

### tablelist标签页
tablelist标签页是用来导出其它内容标签页的配置，它包括 目标标签页、描述、导出文件名、导出字段、导出类型
![tablelist](/images/1.png)

每个记录代表一个导出操作，比如上图中每个标签页分别有两份导出配置记录，分别对应客户端使用和服务器使用，
他们的区别在于导出文件名和导出字段不一样。



type

### 内容标签页


## 打包为exe
代码基于python2.7进行开发，将python脚本编译成exe更方便在windows上传播使用,这里使用pip安装pyinstaller，之后进行打包
```
pip install pyinstaller
```
安装好后就可以使用pyinstaller命令进行打包了
```
pyinstaller -F excel2json.py
```
这样会在dist目录生成 excel2json.exe 可执行文件了,使用命令如下
```
excel2json.exe config.xlsx
```

## 启动批处理
每次输入命令进行转换比较繁琐，这里使用windos批处理来优化，新建一个 convert.bat 文件，内容如下:
```
@echo off

:: delete all *.json
echo del all *.json
del /s *.json

:: covert config
excel2json.exe config.xlsx

pause
```
然后双击 convert.bat 即可自动转换，你也可以在批处理里加上 拷贝json到客户端及服务器目录

