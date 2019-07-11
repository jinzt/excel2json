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

tablelist 一共支持三种导出类型 key:array key:map key:value，这三种类型是我自己总结最常用的三种


#### 内容标签页
内容标签页的第一行是列名，第二行是列的类型，这里一共设计了6中类型，
分别是 INT、FLOAT、BOOL、STRING、OBJECT、ANY。前四种类型都很好理解，
OBJECT是json类型，它必须是一个合法json
ANY是任意类型，它可以是其它5种类型的任意一种，仅适用于key:value类型标签页,ANY类型列中


**key:array** 是数组结构，它有多个列，每个列属性类型一样，所有列构成一个字典对象，作为数组的一条记录
,配置表示例如下
![key:array](/images/2.png)

导出 test_key_array_s.json 如下:
```json
[
	{ "ID":100, "Ratio":0.6, "Reward":[2,3,4], "TaxRatio":{"Ratio":1, "Base":10000} },
	{ "ID":101, "Ratio":0.7, "Reward":[3,5,7], "TaxRatio":{"Ratio":1, "Base":10000} },
	{ "ID":102, "Ratio":0.5, "Reward":[10,15,20], "TaxRatio":{"Ratio":1, "Base":1000} }
]
```

**key:map** 是字典结构，它有多个列，每个列属性类型一样，第一列作为字典的key并且只能是string类型
,配置表示例如下
![key:map](/images/3.png)

导出 test_key_map_s.json 如下:
```json
{
	"test001": { "Key":"test001", "Name":"zhangsan", "Age":18 },
	"test002": { "Key":"test002", "Name":"lisi", "Age":19 }
}
```

**key:value** 是键值对结构，他是一种特殊字典结构，它只有两列，第一列作为key并且只能是string类型，第二列是值，它是任意类型
,配置表示例如下
![key:value](/images/4.png)

导出 test_key_value_s.json 如下:
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

每次输入命令进行转换比较繁琐，这里使用windows批处理来优化，新建一个 convert.bat 文件，内容如下:
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


### json加载示范
这里使用golang来进行举例 load_json.go

```golang
package main

import (
	"encoding/json"
	"fmt"
	"io/ioutil"
	"log"
)

type KeyMapItem struct {
	ID   string `json:"ID"`
	Name string `json:"Name"`
	Age  uint32 `json:"Age"`
}

func loadKeyMapJson() {
	fileName := "test_key_map_s.json"
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Printf("ReadFile %s open failed err:%+v", fileName, err)
		return
	}
	var mapResult map[string]KeyMapItem
	err = json.Unmarshal(data, &mapResult)
	if err != nil {
		log.Printf("ReadFile %s Unmarshal failed err:%+v", fileName, err)
		return
	}
	fmt.Printf("loadKeyMapJson :%+v", mapResult)
}

type probability struct {
	Ratio uint32 `json:"Ratio"`
	Base  uint32 `json:"Base"`
}

type KeyArrayItem struct {
	ID       uint32      `json:"ID"`
	Ratio    float32     `json:"Ratio"`
	Reward   []uint32    `json:"Reward"`
	TaxRatio probability `json:"TaxRatio"`
}

func loadKeyArrayJson() {
	fileName := "test_key_array_s.json"
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Printf("ReadFile %s open failed err:%+v", fileName, err)
		return
	}
	var arrayResult []KeyArrayItem
	err = json.Unmarshal(data, &arrayResult)
	if err != nil {
		log.Printf("ReadFile %s Unmarshal failed err:%+v", fileName, err)
		return
	}
	fmt.Printf("loadKeyArrayJson :%+v", arrayResult)
}

type KeyValueItem struct {
	KEY_INT          uint32      `json:"KEY_INT"`
	KEY_FLOAT        float32     `json:"KEY_FLOAT"`
	KEY_BOOL         bool        `json:"KEY_BOOL"`
	KEY_OBJECT_ARRAY []uint32    `json:"KEY_OBJECT_ARRAY"`
	KEY_OBJECT_DICT  probability `json:"KEY_OBJECT_DICT"`

	KEY_STRING              string `json:"KEY_STRING"`
	KEY_STRING_INT          string `json:"KEY_STRING_INT"`
	KEY_STRING_FLOAT        string `json:"KEY_STRING_FLOAT"`
	KEY_STRING_BOOL         string `json:"KEY_STRING_BOOL"`
	KEY_STRING_OBJECT_ARRAY string `json:"KEY_STRING_OBJECT_ARRAY"`
	KEY_STRING_OBJECT_DICT  string `json:"KEY_STRING_OBJECT_DICT"`
}

func loadKeyValueJson() {
	fileName := "test_key_value_s.json"
	data, err := ioutil.ReadFile(fileName)
	if err != nil {
		log.Printf("ReadFile %s open failed err:%+v", fileName, err)
		return
	}
	var valueResult KeyValueItem
	err = json.Unmarshal(data, &valueResult)
	if err != nil {
		log.Printf("ReadFile %s Unmarshal failed err:%+v", fileName, err)
		return
	}
	fmt.Printf("loadKeyValueJson :%+v", valueResult)
}

func main() {
	loadKeyMapJson()
	loadKeyArrayJson()
	loadKeyValueJson()
}
```

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


## star
欢迎star，个人博客 [https://jinzt.github.io](https://jinzt.github.io)
