import inspect
import os
import platform
import re
import sys
import traceback

sys.path.append(os.getcwd())
import config
from pyfa import options

if options.rootsavedata is True:
    config.saveInRoot = True
config.debug = options.debug
config.defPaths(options.savepath)

import eos.db
# Make sure the saveddata db exists
if not os.path.exists(config.savePath):
    os.mkdir(config.savePath)

from effs_stat_export import parseNeededFitDetails

def exportPyfaFits(opts):
    if opts:
        if opts.outputpath:
            basePath = opts.outputpath
        elif opts.savepath:
            basePath = opts.savepath
        else:
            basePath = config.savePath + os.sep
    else:
        basePath = config.savePath + os.sep
    if basePath[len(basePath) - 1] != os.sep:
        basePath = basePath + os.sep
    output = open(basePath + 'shipJSON.js', 'w')
    output.write('let shipJSON = JSON.stringify([')
    #The current storage system isn't going to hold more than 2500 fits as local browser storage is limited
    limit = 2500
    skipTill = 0
    nameReq = ''
    n = 0
    fitList = eos.db.getFitList()
    for fit in fitList:
        if limit == None or n < limit:
            n += 1
            name = fit.ship.name + ': ' + fit.name
            if n >= skipTill and nameReq in name:
                stats = parseNeededFitDetails(fit, 0)
                output.write(stats)
                output.write(',\n')
    output.write(']);\nexport {shipJSON};')
    output.close()
