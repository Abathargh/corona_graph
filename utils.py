"""
This is free and unencumbered software released into the public domain.

Anyone is free to copy, modify, publish, use, compile, sell, or
distribute this software, either in source code form or as a compiled
binary, for any purpose, commercial or non-commercial, and by any
means.

In jurisdictions that recognize copyright laws, the author or authors
of this software dedicate any and all copyright interest in the
software to the public domain. We make this dedication for the benefit
of the public at large and to the detriment of our heirs and
successors. We intend this dedication to be an overt act of
relinquishment in perpetuity of all present and future rights to this
software under copyright law.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT.
IN NO EVENT SHALL THE AUTHORS BE LIABLE FOR ANY CLAIM, DAMAGES OR
OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE,
ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
OTHER DEALINGS IN THE SOFTWARE.

For more information, please refer to <http://unlicense.org/>
"""

import subprocess
import datetime
import pathlib
import random
import string

data_file = "https://raw.githubusercontent.com/pcm-dpc/COVID-19/master/dati-json/dpc-covid19-ita-regioni.json"
file_name = "dati-regioni.json"
last_name = "last_update"


# Important datatimes and data paths, by default everything is saved in ~/.corona_graph

data_folder = pathlib.Path(pathlib.Path.home(), ".corona_graph")
img_folder = pathlib.Path(pathlib.Path.home(), ".corona_graph", "imgs")
file_path = pathlib.Path(data_folder, file_name)
last_path = pathlib.Path(data_folder, last_name)

day_0 = datetime.date(2020, 2, 24).strftime("%Y-%m-%d")
today = datetime.datetime.now().strftime("%Y-%m-%d")


def is_cache_old() -> bool:
    if not last_path.exists():
        return False
    with open(last_path, "r") as lp:
        last_update = datetime.datetime(*[int(elem) for elem in lp.read().split("-")])
        now = datetime.datetime.now()
        return (now.date() > last_update.date()) or ((now.hour - last_update.hour) > 0)


def save_update() -> None:
    with open(last_path, "w") as lp:
        now = datetime.datetime.now().strftime("%Y-%m-%d-%H")
        lp.write(now)


def update_data() -> None:
    data_folder.mkdir(parents=True, exist_ok=True)
    curl = subprocess.run(["curl", data_file, "-o", file_name], cwd=data_folder)
    if curl.returncode != 0:
        raise ValueError
    save_update()


def get_data(data: str) -> str:
    return data[0:data.index("T")]


def is_data(data: str) -> bool:
    try:
        datetime.datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def random_img_name() -> str:
    img_folder.mkdir(parents=True, exist_ok=True)
    rand = "".join([random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(10)])
    return str(pathlib.Path(img_folder, f"{rand}.png"))


def sub_data(d1: str, d2: str) -> int:
    y1, m1, d1 = [int(e) for e in d1.split("-")]
    y2, m2, d2 = [int(e) for e in d2.split("-")]
    return (datetime.date(y1, m1, d1) - datetime.date(y2, m2, d2)).days


def list_diff(i_list: list) -> list:
    return [i_list[idx+1] - elem for idx, elem in enumerate(i_list[0:-1])]


def div_list(f_list: list, s_list: list) -> list:
    return [f/s if s != 0 else 0 for f, s in zip(f_list, s_list) ]
