# Pyfa Internationalization (i18n) and Localization (l10n)

pyfa provides community-driven translations for a variety of languages. It is important to keep in mind that pyfa translations are not the same as the translations that come from EVE data. These translations are dumped directly from the game, and the pyfa team has no control over them. This includes, but is not limited to:

* Market browser
* Ship browser
* Item names, description, traits, attributes

If there is a translation issue in EVE data, you must submit a ticket to CCP instead.

## Getting Involved 

Translations are done mainly through [Crowdin](https://crowdin.com/project/pyfa). This platform allows translations to be done by anyone without any real need to understand the project's internals. Simply sign up, join the project as a Translator, and start translating!

As a general rule of thumb, we consider translations community-driven. The pyfa team isn't going to

 1) Maintain individual language packs as a part of general development work, or
 2) Delay a release if translations aren't available

This is because the pyfa team is only versed in a few languages, at best, and we do not wish to hold up development in the case of not having translations available.

### Proofreader

By default, signing up on Crowdin allows you to *suggest* translations. These will still produce a PR on GitHub and can still be included in the project. But, if you wish to adopt a language as a proofreader - someone with the ability to "approve" translations to ensure that they are correct and work well in pyfa - then please get in touch with us and we can set your account on Crowdin as a proofreader.

## `gettext`

The following is more for developers or those that wish to understand better the translation system pyfa uses. If you're looking to simply help us translate, please read the Getting Involved section above.

### How it works

A quick introduction to GNU `gettext` translations! There is no programming knowledge required to help with most of the translations. Each langauge that we support has a `LC_MESSAGES/lang.po` file, and in this file there are multiple groups of `msgid` and `msgstr`. `msgid` is usually the English version that is displayed in pyfa, whereas `msgstr` would be the translated version.

```
msgid "Click to toggle between effective HP and raw HP"
msgstr "点击切换有效HP和原始HP"
```

90% of translations are as simple as that. The other 10% may require you to take a quick dip into the code to tweak the formatting of the string, assign context prefixs (for translations that may translate differently for the same work due to context), or to even add the annotation to the string that will expose it to the translation engine. If you're not comfortable with that, you can always request it!

### POEdit

[Poedit](https://poedit.net/) offers a nice GUI for updating translations.  

#### To update PO file for existing translation

1. open a existing `locale/ll_CC/LC_MESSAGES/lang.po`
2. *Catalog* -> *Update from POT file*
3. select pre-prepared `lang.pot` file

#### To translate and generate MO file

edit the translation and hit Save :)

## FAQ

Q: I'm running Linux and getting "Cannot set locale to language "English (U.S.)" when trying to run pyfa.<br />
A: pyfa will automatically try to use the en_US local as the default unless otgherwise set. This error can happen when your Linux distribution does not have the en_US locale enabled. The fix for thiss may be distro-speecific, but the process for Debian-based distros is as follows:

    1. Edit the file `/etc/locale.gen`, find the line `# en_US.UTF-8 UTF-8`, remove `#` part
    2. Run `locale-gen` to generate new locale files

Please note that you may have to perform this operation after updating your distro, as the locales may revert. See https://github.com/pyfa-org/Pyfa/issues/2314 for more info

Q: The English text isn't in the `.pot`/`.po` file for me to translate<br />
A: This is probably one of two things:

1. Missing annotations in the source code. All text that needs to be translated needs to be wrapped with `_t()` to make it locale-aware
2. Out of date `.po` file. As pyfa development continues, the `.po` file may fall behind. See next question.
   

Q: How do I update the `.po` file for my language?<br />
A: See `Commands` section below for a number of useful commands

Q: I run pyfa in Linux but the translations don't work<br />
A: If you're running from source / your own method, this is because the `.mo` files aren't checked into the repo and thus aren't available by default. Running `python3 scripts\compile_lang.py` should compile all language files. If you're running from a package from a third-party repository, YMMV - please contact the maintainer of that package.

## Commands

Below is a summary of [GNU gettext](https://www.gnu.org/software/gettext/) manual, adapted for Pyfa i18n workflow. 

Windows users can get these tools via Git for windows, Msys2 or Cygwin; or just use WSL / WSL2. For Linux and macOS users these tools might be available out-of-box.

### To generate new template for translation:

```console
$ find * -name "*.py" | xgettext --from-code=UTF-8 -o locale/lang.pot -d lang -k_t -k_t:1,2,3t -k_t:1,2c,2t -f - -s
```

explanation:

* `find * -name "*.py"`: collect all `.py` file path in current folder and all sub-folders, write it to stdout
    * except those starts with `.`.  E.g.  `.env`, `.idea`, `.venv`.
    * can also append `-not -path 'path/to/venv/*` to exclude `path/to/venv` recursively.
    
* `xgettext` ([doc](https://www.gnu.org/software/gettext/manual/gettext.html#Template)): a utility looking for keyword and put string literals in a specific format for human translation
    * `--from-code=UTF-8`: designates encoding of files 
    * `-o locale/lang.pot`: let `xgettext` write to `locale/lang.pot`
    * `-d lang`: default language domain is `lang`
    * `-k_t`: besides default keyword (including `_`, see `info xgettext` for detail), also look for `_t`,
        where the string literal (`msgid`) will be the first argument of this function call
    * `-k_t:1,2,3t`: look for `_t`, first arg is `msgid`, second arg is `msgid_plural`, 3 args in total
    * `-k_t:1,2c,2t`: look for `_t`, first arg is `msgid`, second arg is `msgctxt`, 2 args in total
    * `-f -`: let `xgettext` to read filenames from stdin, which is connected to `find` stdout
    * `-s`: sort output according to `msgid`

this `locale/lang.pot` is called PO template, which is the source file for Crowdin translation.

### To initialize PO file for new language

```console
$ msginit -i locale/lang.pot -l ll_CC -o locale/ll_CC/LC_MESSAGES/lang.po -s
```

explanation:

* `-i locale/lang.pot`: input file location
* `-l ll_CC`: target locale. `ll` should be a language code, and `CC` should be a country code
* `-o locale/ll_CC/LC_MESSAGES/lang.po`: output file
    * `ll_CC`: same as above
    * `LC_MESSAGES`: GNU gettext conventional path to search for localized messages
    * `lang.po`: language domain and file format

this `locale/ll_CC/LC_MESSAGES/lang.po` should be checked into VCS, later it will be converted into mechine readable format (`.mo`).

### To update PO file for existing translation

```console
$ msgmerge -s locale/ll_CC/LC_MESSAGES/lang.po locale/lang.pot
```

### To do actual translation

just edit the `lang.po` file, either manually or via GUI applications like POEdit

### To generate machine readable MO file

For a single locale:

```console
$ msgfmt locale/ll_CC/LC_MESSAGES/lang.po -o locale/ll_CC/LC_MESSAGES/lang.mo
```

For all available locales:
```bash
for f in locale/*/; do 
    msgfmt $f/LC_MESSAGES/lang.po -o $f/LC_MESSAGES/lang.mo
done
```
Since compiling `.po` files is useful to everyone, we also have a script in the repo that can do it without the need for the normal `gettext` tools:
`python3 scripts/compile_lang.py`

### To merge 2 or more PO file

```console
$ msgcat -s path/to/old.po [path/to/another.po] -o path/to/new.po
```

Note that `msgcat` cannot perform a 3-way merge, it will simply stack translations with same `msgid` on top of each other.
If you use `msgcat` to merge multiple PO file, please check and fix the output before commit to Git. 

