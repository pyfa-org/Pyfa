# pyfa

[![Join the chat at https://gitter.im/pyfa-org/Pyfa](https://badges.gitter.im/pyfa-org/Pyfa.svg)](https://gitter.im/pyfa-org/Pyfa?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge)

![pyfa](https://cloud.githubusercontent.com/assets/3904767/10271512/af385ef2-6ade-11e5-8f67-52b8b1e4c797.PNG)

## What is it?

pyfa, short for **py**thon **f**itting **a**ssistant, allows you to create, experiment with, and save ship fittings without being in game. Open source and written in Python, it is available on any platform where Python 2.x and wxWidgets are available, including Windows, Mac OS X, and Linux.

## Latest Version and Changelogs
The latest version along with release notes can always be found on the projects [Releases](https://github.com/DarkFenX/Pyfa/releases) page. pyfa will notify you if you are running an outdated version.

## Installing
Windows and OS X users are supplied self-contained builds of pyfa that can be run without additional software. An `.exe` installer is also available for the Windows builds. There is no self-contained package for Linux users, which are expected to run pyfa through their distributions Python interpreter. However, there are a number of third-party packages available that handle the dependencies and updates for pyfa (for example, [pyfa for Arch Linux](https://aur.archlinux.org/packages/pyfa/)). Please check your distributions repositories.

### Dependencies
If you wish to help with development or simply need to run pyfa through a Python interpreter, the following software is required:

* Python 2.7
* `wxPython` 2.8/3.0
* `sqlalchemy` >= 0.6
* `dateutil`
* `matplotlib` (for some Linux distributions, you may need to install separate wxPython bindings, such as `python-matplotlib-wx`)
* `requests`

### Linux Distro-specific Packages
The following is a list of pyfa packages available for certain distros. Please note that these packages are maintained by third-parties and are not evaluated by the pyfa developers.

* Debian/Ubuntu/derivitives: https://github.com/AdamMajer/Pyfa/releases
* Arch: https://aur.archlinux.org/packages/pyfa/
* openSUSE: https://build.opensuse.org/package/show/home:rmk2/pyfa
* FreeBSD: http://www.freshports.org/games/pyfa/ (see #484 for instructions)

## Bug Reporting
The preferred method of reporting bugs is through the projects GitHub Issues interface. Alternatively, posting a report in the pyfa thread on the official EVE Online forums is acceptable. Guidelines for bug reporting can be found on [this wiki page](https://github.com/DarkFenX/Pyfa/wiki/Bug-Reporting). 

## License
pyfa is licensed under the GNU GPL v3.0, see LICENSE

## Resources
* Development repository: [http://github.com/DarkFenX/Pyfa](http://github.com/DarkFenX/Pyfa)
* XMPP conference: [pyfa@conference.jabber.org](pyfa@conference.jabber.org)
* [EVE forum thread](http://forums.eveonline.com/default.aspx?g=posts&t=247609)
* [EVE University guide using pyfa](http://wiki.eveuniversity.org/Guide_to_using_PYFA)
* [EVE Online website](http://www.eveonline.com/)

## Contacts:
* Sable Blitzmann
    * GitHub: @blitzmann
    * [TweetFleet Slack](https://www.fuzzwork.co.uk/tweetfleet-slack-invites/): @blitzmann
    * [Gitter chat](https://gitter.im/pyfa-org/Pyfa): @ blitzmann
    * Email: sable.blitzmann@gmail.com

## CCP Copyright Notice
EVE Online, the EVE logo, EVE and all associated logos and designs are the intellectual property of CCP hf. All artwork, screenshots, characters, vehicles, storylines, world facts or other recognizable features of the intellectual property relating to these trademarks are likewise the intellectual property of CCP hf. EVE Online and the EVE logo are the registered trademarks of CCP hf. All rights are reserved worldwide. All other trademarks are the property of their respective owners. CCP hf. has granted permission to Osmium to use EVE Online and all associated logos and designs for promotional and information purposes on its website but does not endorse, and is not in any way affiliated with, Osmium. CCP is in no way responsible for the content on or functioning of this website, nor can it be liable for any damage arising from the use of this website.
