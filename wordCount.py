import sys
import os
import re
from operator import itemgetter

def main(inputFileName, outputFileName):

    table = dict()
    notWords = re.compile('\W+')
    words = re.compile('\w+')
    
    with open(inputFileName) as inputFile:
        fileStr = inputFile.read()
        fileStrWords = re.sub(notWords, ' ', fileStr).lower()
        matchList = re.findall(words, fileStrWords)
        for word in matchList:
            if word not in table:
                table[word] = 1
            else:
                table[word] += 1

    with open(outputFileName, 'w') as outputFile:
        sortedTable = sorted(table.items(), key=itemgetter(1), reverse=True)
        for item in sortedTable:
            outputFile.write(item[0] + ' ' + str(item[1]) + '\n')

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
