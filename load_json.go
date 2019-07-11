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
