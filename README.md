# 简介
工具是根据 https://github.com/zdhsoft/excel2json 修改而来，非常感谢原作者。


## 工具使用
### excel表格配置
excel表配置主要有tablelist标签页和其它内容标签页构成。

#### tablelist标签页
tablelist标签页是用来导出其它内容标签页的配置，它包括 目标标签页、描述、导出文件名、导出字段、导出类型
![tablelist](/images/1.png)

每个记录代表一个导出操作，比如上图中每个标签页分别有两份导出配置记录，分别对应客户端使用和服务器使用，
他们的区别在于导出文件名和导出字段不一样。

tablelist 一共支持三种导出类型 key:map key:array key:value，这三种类型是我自己总结最常用的三种


#### 内容标签页
内容标签页的第一行是列名，第二行是列的类型，这里一共设计了6中类型，
分别是 INT、FLOAT、BOOL、STRING、OBJECT、ANY。前四种类型都很好理解，
OBJECT是json类型，它必须是一个合法json
ANY是任意类型，它可以是其它5种类型的任意一种，仅适用于key:value类型标签页,ANY类型列中


**key:map** 是字典结构，它有多个列，每个列属性类型一样，第一列作为字典的key并且只能是string类型，
,配置表示例如下
![key:map](/images/2.png)
导出 test_key_map_c.json 如下:
```json
{
	"test001": { "Name":"zhangsan", "Age":18 },
	"test002": { "Name":"lisi", "Age":19 }
}
```

**key:array** 是数组结构，它有多个列，每个列属性类型一样，所有列构成一个字典对象，作为数组的一条记录
,配置表示例如下
![key:array](/images/3.png)
导出 test_key_array_c.json 如下:
```json
[
	{ "ID":100, "Ratio":0.6, "Rward":[2,3,4], "Open":false, "Desc":"23" },
	{ "ID":101, "Ratio":0.7, "Rward":[3,5,7], "Open":true, "Desc":"2.33" },
	{ "ID":102, "Ratio":0.5, "Rward":[10,15,20], "Open":false, "Desc":"金宝箱" }
]
```

**key:value** 是键值对结构，他是一种特殊字典结构，它只有两列，第一列作为key并且只能是string类型，第二列是值，它是任意类型
,配置表示例如下
![key:value](/images/4.png)
导出 test_key_value_c.json 如下:
```json
{
	"KEY_INT":100,
	"KEY_FLOAT":0.23,
	"KEY_BOOL":true,
	"KEY_OBJECT_ARRAY":[10,20],
	"KEY_OBJECT_DICT":{"Ratio":1, "Base":10000},
	"KEY_STRING":"string test",
	"KEY_STRING_INT":"100",
	"KEY_STRING_FLOAT":"0.23",
	"KEY_STRING_BOOL":"true",
	"KEY_STRING_OBJECT_ARRAY":"[10,20]",
	"KEY_STRING_OBJECT_DICT":"\"{\"Ratio\":1, \"Base\":10000}\""
}
```


### 导出json
导出json的工具是使用python开发的，脚本 excel2json.py，可以直接使用脚本导出
``` bash
python excel2json.py config.xlsx
```

更方便的方式是使用打包后的二进制文件 excel2json.exe 进行导出
``` bash
excel2json.exe config.xlsx
```

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
然后双击 convert.bat 即可自动转换，你也可以在批处理里加上 拷贝json到客户端及服务器目录,提交到git、svn等等


## 修改代码
如果需要对源码进行修改，那么需要安装python2.7

python脚本打包为exe借助了pyinstaller，这里使用pip安装pyinstaller，之后进行打包
```
pip install pyinstaller
```
安装好后就可以使用pyinstaller命令进行打包了
```
pyinstaller -F excel2json.py
```
这样会在dist目录生成 excel2json.exe 可执行文件了




