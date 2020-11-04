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

import matplotlib.pyplot as plt
import subprocess
import datetime
import argparse
import pathlib
import random
import string
import json
import sys


repo_name = "COVID-19"
description = "Plot generator for COVID-19 data by the Italian Department of Civil Protection; day_0 = 24/02/2020."
reg_help = "Name(s) of one or more region to plot. By default " \
           "data from every region is plotted."
date_help = "Plot graph(s) up to the passed date; date in the y-m-d format."
last_help = "Plot graph(s) using the last n data samples (using data from the [today -n; today] interval) with " \
            "0 <= n <= # days form day_0"
save_help = "Saves the img instead of plotting it"

gen_err = "You have one of the following problems:\n\t-The passed file does not exist\n\t-You don't have git " \
          "installed on this machine"

git_err = "Couldn't download the repository with the data from Protezione Civile! You need to install git and to " \
            "have an internet connection"

regioni = ["Lombardia", "Lazio", "Campania", "Sicilia", "Veneto",
           "Emilia Romagna", "Abbruzzo", "Basilicata", "P.A. Bolzano",
           "Calabria", "Friuli Venezia Giulia", "Liguria", "Marche", "Molise",
           "Piemonte", "Puglia", "Sardegna", "Toscana", "P.A. Trento", "Umbria",
           "Valle d'Aosta"]


def clone_repo():
    clone = subprocess.run(["git", "clone", "https://github.com/pcm-dpc/COVID-19"])
    if clone.returncode != 0:
        print(git_err)
        sys.exit(clone.returncode)


def pull_repo():
    pull = subprocess.run(["git", "pull"], cwd="COVID-19")
    if pull.returncode != 0:
        print(git_err)
        sys.exit(pull.returncode)


def get_data(data):
    return data[0:data.index("T")]


def is_data(data):
    try:
        datetime.datetime.strptime(data, "%Y-%m-%d")
    except ValueError:
        return False
    return True


def random_img_name():
    return "".join([random.choice(string.ascii_lowercase + string.digits + string.ascii_uppercase) for _ in range(10)])


def sub_data(d1, d2):
    y1, m1, d1 = [int(e) for e in d1.split("-")]
    y2, m2, d2 = [int(e) for e in d2.split("-")]
    return (datetime.date(y1, m1, d1) - datetime.date(y2, m2, d2)).days


def_file = pathlib.Path("COVID-19", "dati-json", "dpc-covid19-ita-regioni.json")
day_0 = datetime.date(2020, 2, 24).strftime("%Y-%m-%d")
today = datetime.datetime.now().strftime("%Y-%m-%d")

parser = argparse.ArgumentParser(description)
parser.add_argument("--regione", "-r", type=str, nargs="+", help=reg_help, default=regioni)
parser.add_argument("--data", "-d", type=str, help=date_help, default=today)
parser.add_argument("--last", "-l", type=int, help=last_help)
parser.add_argument("--save", "-s", action="store_true", help=save_help)
args = parser.parse_args()

try:
    if not pathlib.Path(repo_name).exists():
        clone_repo()
    pull_repo()

    with open(def_file, "r") as file:
        dati = json.loads(file.read())

    if not is_data(args.data) or sub_data(args.data, day_0) < 0 or sub_data(today, args.data) < 0:
        print("Invalid date format: must be in the following form yyy-mm-dd with date > 2020-02-24 and <= today's")
        sys.exit(1)

    max_last = sub_data(today, day_0)
    if not args.last:
        args.last = max_last

    if args.last < 0 or args.last > max_last:
        print(f"Invalid last n-samples, n must be s.t. 0 <= n <= #days from day_0 (currently {max_last})")
        sys.exit(1)

    if not set(args.regione).issubset(set(regioni)):
        print(f"Invalid region, the following are valid names\n {str(regioni)[1:-1]}")
        sys.exit(1)

    for regione in args.regione:
        casi_c = [d["totale_casi"] for d in dati
                  if d["denominazione_regione"] == regione
                  and get_data(d["data"]) < args.data][max_last-args.last:]
        plt.plot(casi_c, label=regione)

except NotADirectoryError as err:
    parser.print_help()
    print("Can't find the COVID-19 directory")
except FileNotFoundError:
    parser.print_help()
    print(gen_err)
except ValueError as ve:
    parser.print_help()
    print(gen_err)
    print("You have a typo in your date")
else:
    plt.grid(linestyle='-', linewidth=2)
    plt.legend()
    if args.save:
        plt.savefig(f"./imgs/{random_img_name()}.png")
    else:
        plt.show()
