# jdk설치, 직접 다운받아서 해당폴더에 복사해야지 error없이 수행
from tika import parser
import os


# inputPath = "C:\\Users\\디랩 학생\\Desktop\\crawlingTest\\"
# outputPath = "C:\\Users\\디랩 학생\\Desktop\\crawlingTestTxt\\"

inputPath = "C:/Users/디랩 학생/Desktop/crawlingTest/"
outputPath = "C:/Users/디랩 학생/Desktop/crawlingTestTxt/"

fileList = os.listdir(inputPath)
회계몇개 = 0
for file in fileList:
    outputName = file.split(".")[0]
    parsered = parser.from_file(inputPath+file)
    # print(file, ':', parsered['content'].count('회계'))
    fileOut = open(outputPath+outputName+'.txt', 'w', encoding='utf-8')
    print(parsered['content'], file=fileOut)
    fileOut.close()

