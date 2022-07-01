import argparse
import json
import os
import re
import requests

with open('data/server.json', 'r') as f:
    SERVER_LIST = json.load(f).keys()

parser = argparse.ArgumentParser()
parser.add_argument('-c', '--use-cdn', action='store_true')
parser.add_argument('-s', '--server', choices=SERVER_LIST, default='zh_CN')
args = parser.parse_args()

if args.use_cdn:
    BASE_URL = 'https://fastly.jsdelivr.net/gh/Kengxxiao/ArknightsGameData@master' # JSdelivr
else:
    BASE_URL = 'https://raw.githubusercontent.com/Kengxxiao/ArknightsGameData/master'
SERVER = args.server
UNIEQUIP_TABLE = 'gamedata/excel/uniequip_table.json'
CHARACTER_TABLE = 'gamedata/excel/character_table.json'
with open('data/prof_dict.json', 'r') as f:
    PROF_DICT = json.load(f)
PATTERNS = {
    'zh_CN': {r'通关(.+?)[；;]':''},
    'en_US': {r'clear (.+?) with':''},
    'ko_KR': {r'스토리 (.+?) 스테이지를':''}, # HELP-WANTED
    'ja_JP': {r'メインテーマ(.+?)を':'メインテーマ', r'サイドストーリー(.+?)を':'サイドストーリー'}, # HELP-WANTED
}
OUTPUT_DIR = f'data/{SERVER}'
OUTPUT = {
    'data': 'data.json',
    'ops': 'ops.json',
    'profs': 'profs.json'
}


def write(path:str, file:str, data:dict) -> None:
    if not os.path.exists(path): os.mkdir(path)
    with open(os.path.join(path, file), 'w') as f:
        json.dump(data, f, ensure_ascii=False, indent=4, separators=(',', ': '))


def getJson(url:str) -> dict:
    return json.loads(requests.get(url).content)


def main():
    prof_dict = PROF_DICT[SERVER]
    pattern = PATTERNS[SERVER]

    uniequip_table:dict = getJson(f'{BASE_URL}/{SERVER}/{UNIEQUIP_TABLE}')
    char_equip:dict = uniequip_table['charEquip']
    equip_dict:dict = uniequip_table['equipDict']
    mission_list:dict = uniequip_table['missionList']
    subprof_dict:dict = {key: value['subProfessionName'] for key, value in uniequip_table['subProfDict'].items()}

    character_table = getJson(f'{BASE_URL}/{SERVER}/{CHARACTER_TABLE}')

    data = {}
    ops = {}
    profs = {}
    for char, equips in char_equip.items():
        name = character_table[char]['name']
        prof = character_table[char]['profession']
        subprof = character_table[char]['subProfessionId']

        for (equip, i) in zip(equips, range(len(equips))):
            if equip_dict[equip]['type'] == 'INITIAL':
                continue

            desc = [mission_list[m]['desc'] for m in equip_dict[equip]['missionList']]
            for (pat, pre) in pattern.items():
                try:
                    op = re.search(pat, desc[1], re.I).group(1)
                except AttributeError:
                    continue
                op = pre + op
                break


            data[f'{char}_{i}'] = {
                'name': name,
                'desc': desc,
                'op': op,
                'prof': prof,
                'subprof': subprof,
            }

            if op not in ops.keys():
                ops[op] = {
                    'name': op
                }

        if prof not in profs.keys():
            profs[prof] = {
                'name': prof_dict[prof.lower()],
                'sub': {}
            }
        if subprof not in profs[prof]['sub'].keys():
            profs[prof]['sub'][subprof] = {
                'name': subprof_dict[subprof]
            }

    write(OUTPUT_DIR, OUTPUT['data'], data)
    write(OUTPUT_DIR, OUTPUT['ops'], ops)
    write(OUTPUT_DIR, OUTPUT['profs'], profs)


if __name__ == '__main__':
    # Currently zh_TW doesn't have uniequip system
    if SERVER == 'zh_TW':
        exit()
    main()