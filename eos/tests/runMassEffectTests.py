#===============================================================================
# This file is part of eos.
#
# eos is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# eos is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with eos.  If not, see <http://www.gnu.org/licenses/>.
#===============================================================================

if __name__ == "__main__":
    print "starting"
    import sys
    import os.path

    #Add the good path to sys.path
    path = os.path.dirname(unicode(__file__, sys.getfilesystemencoding()))
    sys.path.append(os.path.realpath(os.path.join(path, "..", "..")))

    from eos.types import Effect
    from eos.gamedata import effectDummy

    print "checking files in effects folder"
    list = os.listdir(os.path.join("../effects"))
    def validate(fileName):
        moduleName, ext = os.path.splitext(fileName)
        return moduleName != "__init__" and ext == ".py"

    list = filter(validate, list)
    size = len(list)
    print "found %d effects, starting checks:" % size
    i = 0
    lastError = -500
    errors = 0
    errorString = ""
    for fileName in list:
        moduleName, ext = os.path.splitext(fileName)
        i += 1
        if i / 50.0 == int(i / 50.0):
            sys.stdout.write(".")
            sys.stdout.flush()

        e = Effect()
        e.name = unicode(moduleName)
        try:
            e.init()

            if e.handler == effectDummy:
                errors += 1
                sys.stdout.write("F")
                errorString += "\n%s: No handler" % moduleName
            if e.type is None:
                errors += 1
                sys.stdout.write("F")
                errorString += "\n%s: No type" % moduleName
        except Exception, exc:
            errors += 1
            sys.stdout.write("E")
            errorString += "\n%s: Exception thrown: %s\n%s\n" % (moduleName, exc.__class__, exc)

    sys.stderr.write(errorString)

    print ""
    print "Done"
    print "%d errors with a total of %d effects (%.2f%%)" % (errors, size, float(errors) / size * 100)
