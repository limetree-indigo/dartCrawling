import os

downloadFolder = "C:/Users/디랩 학생/Desktop/crawlingNameTransferTest/"
files = os.listdir(downloadFolder)

print(files)

changeNameSet = {'0987': 'abc', '123': 'def', '345': 'z231'}

for file in files:
    filename = file.split('.')[0]
    newFile = file.replace(filename, changeNameSet[filename])
    os.rename(downloadFolder+file, downloadFolder+newFile)

# 코드별다운로드파일명 = {'7227717': '000480', '7227643': '015760', '7226027': '317530', '7225706': '002840', '7225659': '216050'}

# new_dict={}
# for k, v in 코드별다운로드파일명.items():
#     new_dict[v] = k

# print(files)
#
# for file in files:
#     filename = file.split('.')[0]
#     new_filename = file.replace(filename, 코드별다운로드파일명[filename])
#     print(new_filename)
#     os.rename(downloadFolder+file, downloadFolder+new_filename)




