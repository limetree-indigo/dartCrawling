import csv

filePath = "C:/Users/디랩 학생/Desktop/csvTest/"

f = open(filePath+'data2.csv', 'r', encoding='utf-8')
rdr = csv.reader(f)

for line in rdr:
    print(line)
f.close()