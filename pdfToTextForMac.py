# jdk설치, 직접 다운받아서 해당폴더에 복사해야지 error없이 수행
from tika import parser
import os

inputPath = "/Users/jhyoun/Desktop/downTest1/"
outputPath = "/Users/jhyoun/Desktop/toTxt/"

fileList = os.listdir(inputPath)

for file in fileList:
    outputName = file.split(".")[0]
    parsered = parser.from_file(inputPath+file)
    fileOut = open(outputPath+outputName+'.txt', 'w', encoding="utf-8")
    print(parsered['content'], file=fileOut)
    fileOut.close()
