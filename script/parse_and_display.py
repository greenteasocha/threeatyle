import json
import re
import random
import pandas as pd

def get_algs():
    with open("../data/myalgs.json", "r", encoding="utf-8") as f:
        algs = json.load(f)
    return algs

def extract_interchange(alg, prog):
    try:
        return prog.search(alg).group()
    except:
        return None


def display_alg(letter, alg, rev, prog):
    print(letter.strip())
    while(True):
        user_input: str = input()
        if user_input.lower() == "hint":
            hint = extract_interchange(alg, prog)
            print("Interchange : ", hint)

        elif user_input.lower() == "rev":
            print(" ".join(rev))

        elif user_input.lower() == "end":
            return True
        else:
            print(alg)
            return False

def del_none(algs) -> dict:
    """
    手順票に含まれる手順の存在しないレターペアを削除する
    :param dict: algs ... 手順票("にに:None"などが含まれる)
    :return: dict: algs ... 上記のようなエラーを削除した手順票
    """
    null_letters = []
    for k in algs.keys():
        if algs[k] == None:
            null_letters.append(k)

    for nullkey in null_letters:
        del algs[nullkey]

    return algs

def show_all(algs) -> None:
    algs = del_none(algs)
    n_algs = len(algs.keys())

    letters = list(algs.keys())
    for i in range(n_algs):
        print("{}/{}".format(i, n_algs))

        print("{} : {}".format(letters[i], algs[letters[i]]))
        user_input: str = input() # enterまち

    print("All algs executed!!!! Congratulation!!!!")

    return



def main():
    #df_args = pd.read_json("../data/myalgs.json", orient="values")
    with open("../data/myalgs.json", "r", encoding="utf-8") as falg:
        json_algs = json.load(falg)

    for k in json_algs.values():
        print(k)
    #df_algs = pd.DataFrame.from_dict(json_algs)
    prog_interchenge = re.compile(r'\[[^\[]*?\]')
    algs = get_algs()

    print("START.")
    show_all(algs)
    # while True:
    #     letter, arg = random.choice(list(algs.items()))
    #     reverse = (letter[::-1], algs[letter[::-1]])
    #     if arg == "nan":
    #         pass
    #     else:
    #         end_frag = display_alg(letter, arg, reverse, prog_interchenge)
    #         if end_frag:
    #             break

if __name__ == "__main__":
    main()