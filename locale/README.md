On my Windows wsl2 (more generic explaination is needed):

`find ./gui -iname "*.py" | xargs pygettext3 -d lang -o locale/lang.pot`

This will generate the pot that should be carried over to the various language directories and renamed .po

`msgfmt -o lang.mo lang`

Run in each language directory, will compile the .po files to .mo files

## Issues
`zh_CH` doesn't seem to work. AddCatalog is not functioning. See https://discuss.wxpython.org/t/localization-not-working-with-zh-ch-addcatalog-returns-false/34628
