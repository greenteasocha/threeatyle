import json
import requests
import time


def save_image(content, folder, letter):
    filename = "../data/images/{}/{}.png".format(folder, letter)
    with open(filename, "wb") as fout:
        fout.write(content)


def download_image(url, timeout=10):
    response = requests.get(url)
    if response.status_code != 200:
        e = Exception("HTTP Status: " + response.status_code)
        raise e

    content_type = response.headers["content-type"]
    if 'image' not in content_type:
        e = Exception("Content-Type: " + content_type)
        raise e

    return response.content


class ImageGetter(object):
    def __init__(self):
        self.face_order = ["U", "R", "F", "D", "L", "B"]

        self.adjacent_faces = {
            "U": ("F", "R"),
            "R": ("D", "B"),
            "F": ("D", "R"),
            "D": ("B", "R"),
            "L": ("D", "F"),
            "B": ("D", "L")
        }

        self.color = {
            "U": "g",
            "R": "y",
            "F": "o",
            "D": "b",
            "L": "w",
            "B": "r"
        }

    def exec(self, target):
        request_url = self.make_url(target)
        print(request_url)
        return request_url

    def make_url(self, sticker):
        # parameterをくつけてリクエストURLを作成
        base_url = "http://cube.crider.co.uk/visualcube.php?"
        params = {
            "fmt": "png",
            "size": "100",
            "r": "y20x-34",
            "cc": "n",
            "bg": "t",
            "fo": "100",
            "co": "5",
        }
        for k, v in params.items():
            base_url = base_url + "&" + k + "=" + v.replace("s", "l")

        # 最後に"fc"部分の取得
        param_fc = "&fc=" + self._make_facecolor(sticker.split())
        base_url += param_fc

        return base_url

    def _make_facecolor(self, target_stickers):
        # visualcubeの"fc"パラメータに相当する文字列の作成
        fc_states = {
            "U": "dtdtdtdtd",
            "R": "dtdtdtdtd",
            "F": "dtdtdtdtd",
            "D": "ststststs",
            "L": "ststststs",
            "B": "ststststs"
        }

        if len(target_stickers) != 3:
            print("invalid target alg '{}': should contain 3 letters".format(target_stickers))
            return

        for sticker in target_stickers:
            if len(sticker) != 3:
                print("invalid sticker '{}': should contain 3 letters".format(sticker))
                return

            target_face, side = sticker[0], sticker[1] + sticker[2]
            isdown = int(self.adjacent_faces[target_face][0] in side)
            isright = int(self.adjacent_faces[target_face][1] in side)

            target_position = 2 * isdown + isright

            # 真ん中をskip
            if target_position >= 2:
                target_position += 1

            # ここで文字列の書き換えを行う
            fc_states[target_face] = fc_states[target_face][:(2 * target_position)] \
            + self.color[target_face] \
            + fc_states[target_face][(2 * target_position + 1):]

        fc_query = ""
        for each_face in self.face_order:
            fc_query += fc_states[each_face]

        return fc_query


def main():
    with open("../data/convert.json", "r", encoding="utf-8") as fc:
        convert = json.load(fc)
    convert_inverse = {v:k for k, v in convert.items()}

    with open("../data/myalgs.json", "r", encoding="utf-8") as fa:
        algs = json.load(fa)

    gn = ImageGetter()

    for k, v in algs.items():
        if len(k) != 2 or not v:
            print("invalid characters: {}".format(k))
            continue

        letter = "{} {} {}".format(
            "UFR",
            convert_inverse[k[0]],
            convert_inverse[k[1]]
        )

        # 元のステッカー
        url = gn.exec(letter)
        save_image(download_image(url), "target", k)

        # セットアップ後
        if v.startswith("["):
            setup = v.split("[")[1].replace("]", "").replace(" ","")
        else:
            setup = ""
        url += "&alg={}".format(setup)
        save_image(download_image(url), "setup", k)
        print(setup, k)


if __name__ == "__main__":
    main()