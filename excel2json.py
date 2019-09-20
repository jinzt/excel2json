#!/usr/bin/python
# -*- coding: utf-8 -*-
# 这段代码主要的功能是把excel表格转换成utf-8格式的json文件
# lastdate:2011-8-15 14:21 version 1.1 

"""
https://github.com/zdhsoft/excel2json
pip install pyinstaller
pyinstaller -F excel2json.py
"""

import os
import sys
import codecs
import json
import xlrd #http://pypi.python.org/pypi/xlrd
from collections import OrderedDict
from enum import Enum
import types

reload(sys)						 # reload 才能调用 setdefaultencoding 方法  
sys.setdefaultencoding('utf-8')	 # 设置 'utf-8'  



def space_str(layer):
	lua_str = ""
	for i in range(0,layer):
		lua_str += '\t'
	return lua_str


def arr_to_lua_str(data, layer=0):
	d_type = type(data)
	if d_type is types.ListType:
		lua_str = "{\n"
		lua_str += space_str(layer+1)
		for i in range(0,len(data)):
			lua_str += ("[" + str(i+1) + "] = ")
			lua_str += dic_to_lua_str(data[i],layer+1)
			if i < len(data)-1:
				lua_str += ','
		lua_str += '\n'
		lua_str += space_str(layer)
		lua_str +=	'}'
		return lua_str	
	else:
		print d_type , 'is error'
		return None

def dic_to_lua_str(data,layer=0):
	d_type = type(data)
	if	d_type is types.StringTypes or d_type is str or d_type is types.UnicodeType:
		return "'" + data + "'"
	elif d_type is types.BooleanType:
		if data:
			return 'true'
		else:
			return 'false'
	elif d_type is types.IntType or d_type is types.LongType or d_type is types.FloatType:
		return str(data)
	elif d_type is types.ListType:
		lua_str = "{\n"
		lua_str += space_str(layer+1)
		for i in range(0,len(data)):
			lua_str += ("[" + str(i+1) + "] = ")
			lua_str += dic_to_lua_str(data[i],layer+1)
			if i < len(data)-1:
				lua_str += ','
		lua_str += '\n'
		lua_str += space_str(layer)
		lua_str +=	'}'
		return lua_str
	elif d_type is types.DictType:
		lua_str = ''
		lua_str += "\n"
		lua_str += space_str(layer)
		lua_str += "{\n"
		data_len = len(data)
		data_count = 0
		for k,v in data.items():
			data_count += 1
			lua_str += space_str(layer+1)
			if type(k) is types.IntType:
				lua_str += '[' + str(k) + ']'
			else:
				lua_str += k 
			lua_str += ' = '
			try:
				lua_str += dic_to_lua_str(v,layer +1)
				if data_count < data_len:
					lua_str += ',\n'

			except Exception, e:
				print 'error in ',k,v
				raise
		lua_str += '\n'
		lua_str += space_str(layer)
		lua_str += '}'
		return lua_str
	else:
		print d_type , 'is error'
		return None



 
# 数据类型枚举
class DataType(Enum):
	NONE	= 0
	INT		= 1
	FLOAT	= 2 
	BOOL	= 3
	STRING	= 4
	OBJECT	= 5
	ANY		= 6

def IsJson(strValue):
	try:
		json.loads(strValue, encoding='utf-8')
	except ValueError:
		return False
	return True

def IsInt(strValue):
	try:
		int(strValue)
	except ValueError:
		return False
	return True

def IsFloat(strValue):
	try:
		float(strValue)
	except ValueError:
		return False
	return True


AcessDataType = {'INT': DataType.INT, 'FLOAT': DataType.FLOAT, 'BOOL': DataType.BOOL, 'STRING': DataType.STRING, 'OBJECT': DataType.OBJECT, 'ANY': DataType.ANY}
	
def FloatToString (aFloat):
	if type(aFloat) != float:
		return u""
	strTemp = str(aFloat)
	strList = strTemp.split(".")
	if len(strList) == 1 :
		return strTemp
	else:
		if strList[1] == "0" :
			return u""+strList[0]
		else:
			return u""+strTemp

def ParseExtType(paramExtType):
	strList = paramExtType.split(":")
	retType = {}
	if len(strList) == 2:
		retType["key"] = strList[0]
		retType["type"] = strList[1]
	else:
		retType["key"] = ""
		retType["type"] = ""
	return retType


#查找第1个非要求的字符串的下标
def findFirstNot(str, begin, substr):
	for i in range(begin, len(str)):
		if substr.find(str[i]) == -1:
			return i
	return -1

#解析filter字符串，返回变量数组
def parseFilterKey(filter):
	ret = []
	begin = 0
	while True:
		index = filter.find("$", begin)
		if index >= 0:
			index += 1
			end = findFirstNot(filter, index, "1234567890abcdefghijklmnopqrstuvwxyz_ABC DEFGHIJKLMNOPQRSTUVWXYZ")
			key = filter[index:end]
			ret.append(key)
			begin = end
		else:
			return ret

#读入字段映射表
def readMap(table):
	mapTable = {}
	nrow = table.nrows
	if table.ncols == 0:
		return mapTable

	for r in range(nrow):
		k = table.cell_value(r, 0)
		if table.ncols < 2:
			v = k
		else:
			v = table.cell_value(r, 1)
			if (len(v) == 0):
				v = k
		mapTable[k] = v
	return mapTable

#读取字段列表
def readFieldMap(paramFields):
	mapField = {}
	strList = paramFields.split(",")
	for f in strList:
		strNameList = f.split(":")
		if len(strNameList) > 1:
			mapField[strNameList[0]]=strNameList[1]
		else:
			mapField[f] = f

	return mapField

#			 table2as3config(destTable, destFileName, mapTable, mapParam)

def CellToString(paramCell):
	strCellValue = u""
	if type(paramCell) == unicode:
		strCellValue = paramCell
	elif type(paramCell) == float:
		strCellValue = FloatToString(paramCell)
	else:
		strCellValue = str(paramCell)
	return strCellValue

def IsEmptyLine(paramTable, paramRow, paramFieldCount):
	linecnt = 0
	for i in range(paramFieldCount-1):
		v = paramTable.cell_value(paramRow, i)
		if type(v) == unicode:
			v = v
		elif type(v) == float:
			v = FloatToString(v)
		else:
			v = str(v)
		linecnt += len(v)
		if linecnt > 0:
			return False

	if linecnt == 0:
		return True
	else:
		return False

# 数据解析
def DealData(dataType, data):
	ok = False
	strValue = u""

	if dataType == DataType.INT:
		# 这里读进来的整形 带.0
		if type(data) != float:
			return ok, strValue
		strValue = FloatToString(data)
		if IsInt(strValue) == False:
			return ok, strValue
		strValue = str(strValue)
	elif dataType == DataType.FLOAT:
		if type(data) != float:
			return ok, strValue
		strValue = FloatToString(data)
	elif dataType == DataType.BOOL:
		if data == 0:
			strValue = u"false"
		elif data == 1:
			strValue = u"true"
		else:
			return ok, strValue
	elif dataType == DataType.STRING:
		if type(data) == float:
			data = FloatToString(data)
		if type(data) != unicode:
			return ok, strValue
		strValue = data.replace(u"\\", u"\\\\").replace(u"\"", u"\\\"")
		strValue = strValue.replace(u"\n", u"")
		strValue = "\""+ strValue + u"\""
	elif dataType == DataType.OBJECT:
		obj = data.replace(u"\\", u"")
		if IsJson(obj) == False:
			return ok, strValue
		strValue = obj
	elif dataType == DataType.ANY:
		while 1:
			ok, strValue = DealData(DataType.INT, data)
			if ok == True:
				break
			ok, strValue = DealData(DataType.FLOAT, data)
			if ok == True:
				break
			ok, strValue = DealData(DataType.BOOL, data)
			if ok == True:
				break
			ok, strValue = DealData(DataType.OBJECT, data)
			if ok == True:
				break
			ok, strValue = DealData(DataType.STRING, data)
			if ok == True:
				break

			return ok, strValue
	else:
		return ok, strValue

	return True, strValue

def table2array(table, filename, suffix, filter, mapTable, desc):
	nrows = table.nrows
	ncols = table.ncols
	hasMap = (len(mapTable) > 0)

	# 头部加上"[\n"
	json_str = u"[\n"
	rs = 0
	for r in range(2, nrows):
		if IsEmptyLine(table, r, ncols):  #跳过空行
			continue
		strTmp = u"\t{ "
		i = 0
		
		# 过滤不需要的行
		if len(filter) > 0:
			dic = {}
			for c in range(ncols):
				key = table.cell_value(0,c)
				value = table.cell_value(r,c)
				dic[key] = value
			if (eval(filter,{},dic)) == False:
				continue

		for c in range(ncols):
			# 根据列名校验是否是要导出的列
			title = table.cell_value(0,c)
			title = title.replace(u"\n", u"").replace(u"\"", u"")
			if hasMap:
				if not title in mapTable:
					continue
				else:
					title = mapTable[title]

			# 校验列的数据类型
			colType = table.cell_value(1,c)
			if not colType in AcessDataType:
				print (u"data type error on make ", filename, "row:", r, "col:", c, "title:", title)
				sys.exit(1)
			dataType = AcessDataType[colType]

			# 取数据
			data = table.cell_value(r,c)

			# 数据校验转换
			ok, strValue = DealData(dataType, data)
			if ok == False:
				print (u"data format error on make ", filename, "row:", r, "col:", c, "title:", title)
				sys.exit(1)
			
			if i > 0:
				strTmp += u", " + u"\""	 + title + u"\":"+ strValue
			else:
				strTmp += u"" + u"\""  + title + u"\":"+ strValue
	  
			i += 1	
		
		# 当前行结束
		strTmp += u" }"
		if rs > 0:	#不是第1行
			strTmp = ",\n" + strTmp
		rs += 1
		json_str += strTmp

	# 尾部加上"\n]"
	json_str += u"\n]"
	json_str += u"\n"

	# 打开输出文件
	dir = os.path.dirname(filename)
	if dir and not os.path.exists(dir):
		os.makedirs(dir)	
	f = codecs.open(filename,"w","utf-8")
	if suffix == ".json":
		f.write(json.dumps(json.loads(json_str,	 object_pairs_hook=OrderedDict),ensure_ascii=False,indent=4))
	elif suffix == ".lua":
		if len(desc) > 0:
			f.write("--[[\n")
			f.write(str(desc))
			f.write("\n]]--\n")
		f.write("return " + arr_to_lua_str(json.loads(json_str)))
	f.close()
	print "Create ",filename," OK"
	return

def table2map(table, filename, suffix, filter, mapTable, desc):
	nrows = table.nrows
	ncols = table.ncols
	hasMap = (len(mapTable) > 0)
	json_str = u"{\n"
	keyIndex = 0
	rs = 0
	for r in range(2, nrows):
		if IsEmptyLine(table, r, ncols):  #跳过空行
			continue
		i = 0

		keyValue = table.cell_value(r,keyIndex)
		if type(keyValue) == unicode:
			keyValue = keyValue
		elif type(keyValue) == float:
			keyValue = FloatToString(keyValue)
		else:
			keyValue = str(keyValue)

		strTmp = u"\t\""+keyValue + "\": { "

		# 过滤不需要的行
		if len(filter) > 0:
			dic = {}
			for c in range(ncols):
				key = table.cell_value(0,c)
				value = table.cell_value(r,c)
				dic[key] = value
			if (eval(filter,{},dic)) == False:
				continue

		for c in range(ncols):
			# 根据列名校验是否是要导出的列
			title = table.cell_value(0,c)
			title = title.replace(u"\n", u"").replace(u"\"", u"")
			if hasMap:
				if not title in mapTable:
					continue
				else:
					title = mapTable[title]

			# 校验列的数据类型
			colType = table.cell_value(1,c)
			if not colType in AcessDataType:
				print (u"data type error on make ", filename, "row:", r, "col:", c, "title:", title)
				sys.exit(1)
			dataType = AcessDataType[colType]

			# 取数据
			data = table.cell_value(r,c)

			# 数据校验转换
			ok, strValue = DealData(dataType, data)
			if ok == False:
				print (u"data format error on make ", filename, "row:", r, "col:", c, "title:", title)
				sys.exit(1)

			if i > 0:
				delm = u", "
			else:
				delm = u""

			strTmp += delm + u"\""	+ title + u"\":"+ strValue
			i += 1
		
		strTmp += u" }"
		if rs > 0:	#不是第1行
			strTmp = u",\n" + strTmp
	 
		rs += 1	   
		json_str += strTmp

	json_str += u"\n}"
	json_str += u"\n"  
	# 打开输出文件
	dir = os.path.dirname(filename)
	if dir and not os.path.exists(dir):
		os.makedirs(dir)	
	f = codecs.open(filename,"w","utf-8")
	if suffix == ".json":
		f.write(json.dumps(json.loads(json_str,	 object_pairs_hook=OrderedDict),ensure_ascii=False,indent=4))
	elif suffix == ".lua":
		if len(desc) > 0:
			f.write("--[[\n")
			f.write(str(desc))
			f.write("\n]]--\n")
		f.write("return " + dic_to_lua_str(json.loads(json_str)))
	f.close()
	print "Create ",filename," OK"
	return


def table2keyvalue(table, filename, suffix, filter, mapTable, desc):
	nrows = table.nrows
	ncols = table.ncols
	hasMap = (len(mapTable) > 0)
	json_str = u"{\n"
	keyIndex = 0

	rs = 0
	for r in range(2, nrows):
		if IsEmptyLine(table, r, ncols):  #跳过空行
			continue
		i = 0

		# 过滤不需要的行
		if len(filter) > 0:
			dic = {}
			for c in range(ncols):
				key = table.cell_value(0,c)
				value = table.cell_value(r,c)
				dic[key] = value
			if (eval(filter,{},dic)) == False:
				continue

		keyValue = table.cell_value(r,keyIndex)
		if type(keyValue) == unicode:
			keyValue = keyValue
		elif type(keyValue) == float:
			keyValue = FloatToString(keyValue)
		else:
			keyValue = str(keyValue)

		strTmp = u"\t\""+keyValue + "\":"

		for c in range(ncols):
			# 根据列名校验是否是要导出的列
			title = table.cell_value(0,c)
			title = title.replace(u"\n", u"").replace(u"\"", u"")
			if hasMap:
				if not title in mapTable:
					continue
				else:
					title = mapTable[title]

			# 校验列的数据类型
			colType = table.cell_value(1,c)
			if not colType in AcessDataType:
				print (u"data type error on make ", filename, "row:", r, "col:", c, "title:", title)
				sys.exit(1)
			dataType = AcessDataType[colType]

			# 取数据
			data = table.cell_value(r,c)

			# 数据校验转换
			ok, strValue = DealData(dataType, data)
			if ok == False:
				print (u"data format error on make ", filename, "row:", r, "col:", c, "title:", title)
				sys.exit(1)

			if i == 1:
				strTmp += u""+ strValue	

			i += 1
			if i >= 2:
				break
		
		# strTmp += u" }"
		if rs > 0:	#不是第1行
			strTmp = u",\n" + strTmp
		rs += 1
		json_str += strTmp

	json_str += u"\n}"
	json_str += u"\n"
	# 打开输出文件
	dir = os.path.dirname(filename)
	if dir and not os.path.exists(dir):
		os.makedirs(dir)	
	f = codecs.open(filename,"w","utf-8")
	if suffix == ".json":
		f.write(json.dumps(json.loads(json_str,	 object_pairs_hook=OrderedDict),ensure_ascii=False,indent=4))
	elif suffix == ".lua":
		if len(desc) > 0:
			f.write("--[[\n")
			f.write(str(desc))
			f.write("\n]]--\n")
		f.write("return " + dic_to_lua_str(json.loads(json_str)))
	f.close()
	print "Create ",filename," OK"
	return

	

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print 'Usage: %s <excel_file>' % sys.argv[0]
		sys.exit(1)

	print "handle file: %s" % sys.argv[1]

	excelFileName = sys.argv[1]

	# excelFileName = "config.xlsx"

	# 打开excel表
	data = xlrd.open_workbook(excelFileName)

	# 读取 tablelist 导出配置页
	table = data.sheet_by_name(u"tablelist")

	for r in range(table.nrows-1):
		# 读目的table名(filename)
		destTableName = table.cell_value(r+1,0)

		# 读输出文件名(outfilename)
		destFileName = table.cell_value(r+1,2)
		s = "undefined"

		# 读导出的列(fields)
		strUseFields = u""
		if (table.ncols >= 4):
			strUseFields = table.cell_value(r+1,3)
		mapTable = readFieldMap(strUseFields)

		# 读出行筛选条件
		strFilter = table.cell_value(r+1,4)

		# 读导出类型(type)
		strExtType = u""
		if(table.ncols >= 6):
			strExtType = table.cell_value(r+1, 5)
		retType = ParseExtType(strExtType)
		print strExtType, retType, retType["key"], retType["type"]

		# 读出描述
		strDesc = table.cell_value(r+1,6)

		print "\nCreate " + destTableName + " ==> " + destFileName + " Starting..."

		# 读取目的table数据
		destTable = data.sheet_by_name(destTableName)
	  
		# 取目标文件后缀名
		suffix = destFileName[destFileName.rfind("."):].lower()

		#if suffix == ".json" or suffix == ".lua":
		if suffix == ".json" or suffix == ".lua":
			if retType["type"] == "array":
				table2array(destTable, destFileName, suffix, strFilter, mapTable, strDesc)
			elif retType["type"] == "map":
				table2map(destTable, destFileName, suffix, strFilter, mapTable, strDesc)
			elif retType["type"] == "value":
				table2keyvalue(destTable, destFileName, suffix, strFilter, mapTable, strDesc)
			else:
				print u"type only support key:array,key:map,key:value format " + destFileName
				sys.exit(1)
		else:
			print u"当前类型是:", suffix
			print u"only support (json, lua), conf format " + destFileName
			sys.exit(1)

	print "-------- All OK --------"
