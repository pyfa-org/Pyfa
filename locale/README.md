# Pyfa Internationalization(i18n) and Localization(l10n)

Below is a summary of [GNU gettext](https://www.gnu.org/software/gettext/) manual, adapted for Pyfa i18n workflow. 

[Poedit](https://poedit.net/) offers a nice GUI for same GNU gettext translation workflow.

## i18n with command line

Windows users can get these tools via Git for windows, Msys2 or Cygwin; or just use WSL / WSL2.
For Linux and macOS users these tools might be available out-of-box.

### To generate new template for translation:

```console
$ find */ *.py -name "*.py" | xgettext -o locale/lang.pot -d lang -k_t -f -
```

explanation:

* `find */ *.py -name "*.py"`: collect all `.py` file path in root folder and all sub-folder, write it to stdout
* `xgettext`: a utility looking for keyword and put string literals in a specific format for human translation
    * `-o locale/lang.pot`: let `xgettext` write to `locale/lang.pot`
    * `-d lang`: default language domain is `lang`
    * `-k_t`: besides default keyword (including `_`, see `info xgettext` for detail), also look for `_t`
    * `-f -`: let `xgettext` to read from stdin, which is connected to `find` stdout

this `locale/lang.pot` is called PO template, which is throwed away once actual `ll_CC/LC_MESSAGES/lang.po` is ready for use.

### To initialize PO file for new language

```console
$ msginit -i locale/lang.pot -l ll_CC -o locale/ll_CC/LC_MESSAGES/lang.po
```

explanation:

* `-i locale/lang.pot`: input file location
* `-l ll_CC`: target locale. `ll` should be a language code, and `CC` should be a country code
* `-o locale/ll_CC/LC_MESSAGES/lang.po`: output file
    * `ll_CC`: same as above
    * `LC_MESSAGES`: GNU gettext conventional path to search for localized messages
    * `lang.po`: language domain and file format

this `locale/ll_CC/LC_MESSAGES/lang.po` should be checked into VCS, later it will be converted into mechine readable format (MO).

### To update PO file for existing translation

```console
$ msgmerge locale/ll_CC/LC_MESSAGES/lang.po locale/lang.pot
```

### To do actual translation

just edit the `lang.po` file :)

### To generate machine readable MO file

For a single locale:

```console
$ msgfmt locale/ll_CC/LC_MESSAGES/lang.po -o locale/ll_CC/LC_MESSAGES/lang.mo
```

For all available locale:
```bash
for f in locale/*/; do 
    msgfmt $f/LC_MESSAGES/lang.po -o $f/LC_MESSAGES/lang.mo
done
```

## i18n with Poedit

### To update PO file for existing translation

1. open a existing `locale/ll_CC/LC_MESSAGES/lang.po`
2. *Catalog* -> *Update form POT file*
3. select pre-prepared `lang.pot` file

### To translate and generate MO file

edit the translation and hit Save :)