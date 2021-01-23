#!/usr/bin/env python3
#coding: UTF-8

# === 簡単な言語認識を行います ===

# 言語認識機能に使うdict 型
target_dict = {
    'エアコン': ['エアコン'],
    '照明': ['照明','明かり', 'あかり', '電気', 'ライト']
    }
verb_dict = {
    'つける': ['つける', '点ける', 'つけて', '点けて', 'オン', 'on', 'ON'],
    'けす': ['けす', '消す', 'けして', '消して', 'オフ', 'off', 'OFF']
    }


def checkup_msg(msg):
    # 戻り値を先に定義
    tg = None
    vb = None

    # 対象物部分の検索
    for key_t, values_t in target_dict.items():
        found_list = [val for val in values_t if msg.startswith(val)]       
        if len(found_list) >0:
            tg = key_t                  # return value1

            # 動詞部分の検索
            rest_of_msg = msg[len(found_list[0]):]
            for key_v, values_v in verb_dict.items():
                found_list = [val for val in values_v if rest_of_msg.find(val) >= 0]
                if len(found_list) >0:
                    vb = key_v            # return value2
                    break
            break
    return [tg, vb]

# checkup_msg('エアコン点けて')     # こんな感じで使用
# > 'エアコン', 'つける'
