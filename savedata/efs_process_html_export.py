from efs_export_base_fits import *

def efsFitsFromHTMLExport(opts):
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
    try:
        with open('pyfaFits.html'):
            fileLocation = 'pyfaFits.html'
    except:
        try:
            d = config.savePath + os.sep + 'pyfaFits.html'
            print(d)
            with open(d):
                fileLocation = d
        except:
            fileLocation = None;
    limit = 10000
    n = 0
    skipTill = 0
    nameReq = ''
    minimalExport = True
    if fileLocation != None:
        with open(fileLocation) as f:
            for fullLine in f:
                if limit == None or n < limit:
                    if n <= 1 and '<!DOCTYPE html>' in fullLine:
                        minimalExport = False
                    n += 1
                    fullIndex = fullLine.find('data-dna="')
                    minimalIndex = fullLine.find('/dna/')
                    if fullIndex >= 0:
                        startInd = fullLine.find('data-dna="') + 10
                    elif minimalIndex >= 0 and minimalExport:
                        startInd = fullLine.find('/dna/') + 5
                    else:
                        startInd = -1
                    print(startInd)
                    if startInd >= 0:
                        line = fullLine[startInd:len(fullLine)]
                        endInd = line.find('::')
                        dna = line[0:endInd]
                        name = line[line.find('>') + 1:line.find('<')]
                        if n >= skipTill and nameReq in name:
                            print('name: ' + name + ' DNA: ' + dna + fullLine)
                            stats = setFitFromString(dna, name, 0)
                            output.write(stats)
                            output.write(',\n')
    output.write(']);\nexport {shipJSON};')
    output.close()
