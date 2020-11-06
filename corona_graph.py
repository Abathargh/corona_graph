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
from utils import *
import argparse
import json
import sys


# Argparse descriptions and error messages

description = "Plot generator for COVID-19 data by the Italian Department of Civil Protection; day_0 = 24/02/2020."
reg_help = "Name(s) of one or more region to plot. By default " \
           "data from every region is plotted."
date_help = "Plot graph(s) up to the passed date; date in the y-m-d format."
last_help = "Plot graph(s) using the last n data samples (using data from the [today -n; today] interval) with " \
            "0 <= n <= # days form day_0"
derivative_help = "Plots graph(s) of the rate of change of the growth(s)"
save_help = "Saves the img instead of opening it in a window"
force_help = "Forces a fresh download of the data"


# Static region data

regioni = ["Lombardia", "Lazio", "Campania", "Sicilia", "Veneto",
           "Emilia Romagna", "Abbruzzo", "Basilicata", "P.A. Bolzano",
           "Calabria", "Friuli Venezia Giulia", "Liguria", "Marche", "Molise",
           "Piemonte", "Puglia", "Sardegna", "Toscana", "P.A. Trento", "Umbria",
           "Valle d'Aosta"]


# Argparse settings

parser = argparse.ArgumentParser(description)
parser.add_argument("--regione", "-r", type=str, nargs="+", help=reg_help, default=regioni)
parser.add_argument("--data", "-d", type=str, help=date_help, default=today)
parser.add_argument("--last", "-l", type=int, help=last_help)
parser.add_argument("--derivative", "-c", action="store_true", help=derivative_help)
parser.add_argument("--save", "-s", action="store_true", help=save_help)
parser.add_argument("--force", "-f", action="store_true", help=force_help)


def main():
    args = parser.parse_args()
    if not file_path.exists() or is_cache_old() or args.force:
        update_data()

    with open(file_path, "r") as file:
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
        if args.derivative:
            diff_casi = list_diff(casi_c)
            dx = list_diff(list(range(0, len(casi_c))))
            plt.plot(div_list(diff_casi, dx), label=f"d({regione})/dx")
        else:
            plt.plot(casi_c, label=regione)

    plt.grid(linestyle="-", linewidth=2)
    plt.legend()
    if args.save:
        ri_name = random_img_name()
        plt.savefig(ri_name)
        print(f"Saved @ {ri_name}")
    else:
        plt.show()


if __name__ == "__main__":
    try:
        main()
    except FileNotFoundError as fne:
        print(fne)
        parser.print_help()
    except ValueError as ve:
        print(ve)
        parser.print_help()
