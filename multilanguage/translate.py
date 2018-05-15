import sqlite3
from multilanguage import language

if language.current_language != "default":
    conn = sqlite3.connect("language_packs/" + language.current_language + ".db")


def look_up(name_type, origin):
    ans = origin
    if language.current_language != "default":
        c = conn.cursor()
        cursor = c.execute("SELECT `to` FROM " + name_type + " WHERE `from` = \"" + origin + "\"")
        for row in cursor:
            ans = row[0]
    return ans
