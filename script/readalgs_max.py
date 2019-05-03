import pandas as pd
import json
import re


def main():
    with open("../data/convert.json", "r", encoding="utf-8") as fcv:
        convert = json.load(fcv)

    df = pd.read_csv("../data/MaxFU.csv")
    regex_colname = re.compile(r"[UDLRFB][UDLRFB]")
    base_col_name = df.columns[0]
    df.index = df[base_col_name]

    # drop unused columns
    df.drop((i for i in df.columns if not regex_colname.search(i))
            , axis=1
            , inplace=True)

    # drop unused rows
    df.drop((index for index in df.index if not regex_colname.search(index))
            , axis=0
            , inplace=True)

    # 一度"BU"などの形にする
    df_new = df.rename(columns=lambda s: regex_colname.search(s)
                       , index=lambda s: regex_colname.search(s))

    # さらにひらがなにする
    # FUをUFに直している
    df_kana = df.rename(columns=lambda s: convert[s[::-1]],
                        index=lambda s: convert[s[::-1]],
                        inplace=True)

    numbering_list = "あいうえかきくけさしすせたちつてなにぬねはひふへ"
    algs = {}
    for x in numbering_list:
        for y in numbering_list:
            try:
                # ここものすごくpythonっぽい書き方で怖い x:str, y:str
                # 都合上逆にしています
                algs[x + y] = df.loc[y][x]
            except:
                algs[x + y] = "NaN"

    print(algs["はけ"])
    print(algs["へな"])
    with open("../data/myalgs.json", "w", encoding="utf-8") as fj:
        json.dump(algs, fj, ensure_ascii=False, indent=4)

if __name__ == "__main__":
    main()
