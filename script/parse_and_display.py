import json
import re
import random
import math

def get_algs():
    with open("../data/myalgs.json", "r", encoding="utf-8") as f:
        algs = json.load(f)
    return algs

def extract_interchange(alg, prog):
    try:
        return prog.search(alg).group()
    except:
        return None

class SelectModule():
    """
    一定の特徴wを持つ手順だけを含む手順表を作成します。
    ex: F面を含むもの 側面だけで構成されているもの セットアップが3定常の者 インターチェンジに[S, R2]を含むもの
    """
    def __init__(self, args: dict):
        self.origin = get_algs()

    def is_include(self, target: list):
        """
        指定した特徴を1つでも含むもの
        ex: L面を含む(もう一つは何でもよい) U面とD面の手順
        :param target:
        :return:
        """
        valid_keys = []
        for letter in list(self.origin.keys()):
            if self._contain_targets(letter, target):
                valid_keys.append(letter)



    def _contain_targets(self, letter: str, target: tuple(list[str])):
        """
        :param letter: "いさ"などの2文字レターペア
        :param target: 入っていて欲しいグループ
        ex: [["あ", "い", "う" ,"え], ["か", "き", "く", "け"]]
        :return: bool
        """
        if len(letter) != 2:
            assert
        first, second = letter[0], letter[1]
        if len(target) > 2:
            assert
        for t in target:
            if first not in t and second not in t:
                return False

        return True






class ThreeStyle():
    def __init__(self, algs):
        self.algs = self.del_null(algs)
        self.letters = list(self.algs.keys())
        self.show_all()

    def del_null(self, algs: dict) -> dict:
        # "ぬぬ"のような無効なレターペアの削除
        null_letters = []
        for k in list(algs.keys()):
            if isinstance(algs[k], float):
                null_letters.append(k)

        for nk in null_letters:
            del algs[nk]

        return algs

    def show_each(self, idx: int, n_algs: int):
        """
        一手順に当たるモジュール
        :param idx:
        :param n_algs:
        :return:
        """
        print("{}/{}".format(idx + 1, n_algs))
        letter = self.letters[idx]
        print("{} : {}".format(letter, self.algs[letter]))


    def show_all(self):
        n_algs = len(self.letters)
        idx = 0
        while(idx < n_algs - 1):
            self.show_each(idx, n_algs)
            idx += 1
            user_input = input()
            if input == "b":
                idx -= 1

def main():
    prog_interchenge = re.compile(r'\[[^\[]*?\]')
    algs = get_algs()

    print("START.")
    tsapplication = ThreeStyle(algs)


if __name__ == "__main__":
    main()