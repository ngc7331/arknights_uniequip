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
    'ops': 'ops.json',
    'profs': 'profs.json'
}

def getName(s:str):
    prof_name = {
        'support': '辅助',
        'summoner': '召唤师',

        'warrior': '近卫',
        'instructor': '教官',
        'sword': '剑豪',
        'fearless': '无畏者',

        'sniper': '狙击',
        'longrange': '神射手',
        'aoesniper': '炮手',

        'medic': '医疗',
        'ringhealer': '群愈师',

        'special': '特种',
        'executor': '处决者',
        'merchant': '行商',

        'caster': '术师',
        'chain': '链术师',
        'splashcaster': '扩散术师',

        'pioneer': '先锋',
        'charger': '冲锋手'
    }
    s = s.lower()
    if s not in prof_name.keys():
        return s
    return prof_name[s]


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

    data = {}
    ops = {}
    profs = {}
    for char, (_, equip) in char_equip.items():
        name = character_table[char]['name']
        desc = [mission_list[m]['desc'] for m in equip_dict[equip]['missionList']]
        prof = character_table[char]['profession']
        subprof = character_table[char]['subProfessionId']
        op = re.search(r'通关(.+)[；;]', desc[1]).group(1)

        data[char] = {
            'name': name,
            'desc': desc,
            'op': op,
            'prof': prof,
            'subprof': subprof
        }

        if op not in ops.keys():
            ops[op] = {
                'name': op,
                'show': True
            }

        if prof not in profs.keys():
            profs[prof] = {
                'name': getName(prof),
                'sub': {}
            }
        if subprof not in profs[prof]['sub'].keys():
            profs[prof]['sub'][subprof] = {
                'name': getName(subprof),
                'show': True
            }


    write(OUTPUT_DIR, OUTPUT['data'], data)
    write(OUTPUT_DIR, OUTPUT['ops'], ops)
    write(OUTPUT_DIR, OUTPUT['profs'], profs)
