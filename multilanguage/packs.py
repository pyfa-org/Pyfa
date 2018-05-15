import os

packs_list = ["default"]


def get_packs_list():
    global packs_list
    packs_list = ["default"]
    for root, dirs, files in os.walk("language_packs"):
        for file in files:
            if os.path.splitext(file)[1] == '.db':
                packs_list.append(os.path.splitext(file)[0])


get_packs_list()
