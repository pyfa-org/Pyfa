from optparse import AmbiguousOptionError, BadOptionError, OptionParser

class PassThroughOptionParser(OptionParser):

    def _process_args(self, largs, rargs, values):
        while rargs:
            try:
                OptionParser._process_args(self, largs, rargs, values)
            except (BadOptionError, AmbiguousOptionError) as e:
                pyfalog.error("Bad startup option passed.")
                largs.append(e.opt_str)

usage = "usage: %prog [options]"
parser = PassThroughOptionParser(usage=usage)
parser.add_option(
    "-f", "--exportfits", action="store_true", dest="exportfits", \
    help="Export this copy of pyfa's local fits to a shipJSON file that Eve Fleet Simulator can import from", \
    default=False)
parser.add_option(
    "-b", "--exportbaseships", action="store_true", dest="exportbaseships", \
    help="Export ship stats to a shipBaseJSON file used by Eve Fleet Simulator", \
    default=False)
parser.add_option(
    "-c", "--convertfitsfromhtml", action="store_true", dest="convertfitsfromhtml", \
    help="Convert an exported pyfaFits.html file to a shipJSON file that Eve Fleet Simulator can import from\n"
    + "    Note this process loses data like fleet boosters as the DNA format exported by to html contains limited data", \
    default=False)
parser.add_option("-s", "--savepath", action="store", dest="savepath", help="Set the folder for savedata", default=None)
parser.add_option(
    "-o", "--outputpath", action="store", dest="outputpath",
    help="Output directory, defaults to the savepath", default=None)


(options, args) = parser.parse_args()

if options.exportfits:
    from effs_export_pyfa_fits import exportPyfaFits
    exportPyfaFits(options)

if options.exportbaseships:
    from effs_export_base_fits import exportBaseShips
    exportBaseShips(options)

if options.convertfitsfromhtml:
    from effs_process_html_export import effsFitsFromHTMLExport
    effsFitsFromHTMLExport(options)

#stuff bellow this point is purely scrap diagnostic stuff and should not be public (as it's scrawl)
def printGroupData():
    from eos.db import gamedata_session
    from eos.gamedata import Group, Category
    filterVal = Group.categoryID == 6
    data = gamedata_session.query(Group).options().list(filter(filterVal).all())
    for group in data:
        print(group.groupName + '  groupID: ' + str(group.groupID))
    return ''
