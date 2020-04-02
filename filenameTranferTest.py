import os

files = os.listdir("C:\\Users\\디랩 학생\\Desktop\\crawlingTest\\")

종목코드별다운로드파일이름 = {'000480': '7227717', '015760': '7227643', '317530': '7226027', '002840': '7225706', '216050': '7225659'}

print(files)

for filename in files:
    new_filename = filename.replace("AA", "BB")
    os.rename(filename, new_filename)




