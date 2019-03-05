import json
import re
import random

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
            return 1
        else:
            print(alg)
            return 0


def main():
    prog_interchenge = re.compile(r'\[[^\[]*?\]')
    algs = get_algs()

    print("START.")
    while True:
        letter, arg = random.choice(list(algs.items()))
        reverse = (letter[::-1], algs[letter[::-1]])
        if arg == "nan":
            pass
        else:
            end_frag = display_alg(letter, arg, reverse, prog_interchenge)
            if end_frag:
                break

if __name__ == "__main__":
    main()