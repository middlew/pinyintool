import json
import unicodedata

# 读取汉字拼音数据
with open('py2hz.json', 'r', encoding='utf-8') as f:
    py2hz = json.load(f)

# 查找所有的简体汉字
simplified_chars = set()
for hz_list in py2hz.values():
    for hz in hz_list:
        for char in hz:
            if unicodedata.name(char).startswith('CJK UNIFIED IDEOGRAPH'):
                if unicodedata.name(char).endswith('CJK COMPATIBILITY IDEOGRAPH'):
                    continue
                simplified_char = unicodedata.normalize('NFKC', char)
                simplified_chars.add(simplified_char)

# 生成简体汉字到拼音的映射
simplified_py2hz = {}
for pinyin, hz_list in py2hz.items():
    simplified_hzs = []
    for hz in hz_list:
        # simplified_hz = ''.join([unicodedata.normalize('NFKC', char) if char in simplified_chars else char for char in hz])
        simplified_hz = ''.join(['' if char not in simplified_chars else char for char in hz])
        simplified_hzs.append(simplified_hz)
        # print(simplified_hzs)
    simplified_py2hz[pinyin] = simplified_hzs


# 保存简体汉字拼音数据到文件
with open('simplified_py2hz.json', 'w', encoding='utf-8') as f:
    json.dump(simplified_py2hz, f, ensure_ascii=False, indent=2)

