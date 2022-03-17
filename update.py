import json
import os
import re
import requests

CONST = {
#    'BASE_URL': 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master',
    'BASE_URL': 'https://fastly.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master', # JSdelivr
    'SERVER': 'zh_CN',
#    'SERVER': 'zh_TW',
#    'SERVER': 'en_US',
#    'SERVER': 'ja_JP',
#    'SERVER': 'ko_KR',
    'UNIEQUIP_TABLE': 'gamedata/excel/uniequip_table.json',
    'CHARACTER_TABLE': 'gamedata/excel/character_table.json'
}

OUTPUT_DIR = 'data'
OUTPUT = {
    'data': 'data.json',
    'ops': 'ops.json'
}

def write(path:str, file:str, data:dict):
    if not os.path.exists(path): os.mkdir(path)
    with open(os.path.join(path, file), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))


if __name__ == '__main__':
    uniequip_table = json.loads(requests.get('{BASE_URL}/{SERVER}/{UNIEQUIP_TABLE}'.format(**CONST)).content)
    char_equip = uniequip_table['charEquip']
    equip_dict = uniequip_table['equipDict']
    mission_list = uniequip_table['missionList']

    character_table = json.loads(requests.get('{BASE_URL}/{SERVER}/{CHARACTER_TABLE}'.format(**CONST)).content)

    for char, dic in character_table.items():
        character_table[char] = dic['name']

    data = {}
    ops = {}
    for char, (_, equip) in char_equip.items():
        name = character_table[char]
        desc = [mission_list[m]['desc'] for m in equip_dict[equip]['missionList']]
        op = re.search(r'通关(.+)[；;]', desc[1]).group(1)

        data[char] = {
            'name': name,
            'desc': desc,
            'op': op
        }
        if op not in ops.keys():
            ops[op] = {
                'name': op,
                'char': []
            }
        ops[op]['char'].append(char)

    write(OUTPUT_DIR, OUTPUT['data'], data)
    write(OUTPUT_DIR, OUTPUT['ops'], ops)
