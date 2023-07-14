import json
import unicodedata

# 读取汉字拼音数据
with open('py2hz.json', 'r', encoding='utf-8') as f:
    py2hz = json.load(f)

# 读取3500常用汉字
with open('3500常用汉字.txt', 'r', encoding='utf-8') as fc:
    simplified_chars = fc.read()

# 生成简体汉字到拼音的映射
simplified_py2hz = {}
for pinyin, hz_list in py2hz.items():
    list1 = set(simplified_chars) & set(hz_list)
    simplified_hzs = [char for char in list1]
    simplified_py2hz[pinyin] = simplified_hzs

# 保存简体汉字拼音数据到文件
with open('simplified_py2hz.json', 'w', encoding='utf-8') as f:
    json.dump(simplified_py2hz, f, ensure_ascii=False, indent=2)

