import time
import pandas as pd
from pathlib import *
import os
start = time.perf_counter()

i = 0       #当前csv文件序数
count = 0   #计数器
excelfile = Path('./岩芯振动测量数据/泥晶灰岩')
#定义一个空列表，存放从excel中读取的波形数据
files = []

#统计excel文件总数
for file in os.listdir(excelfile):
    count += 1
print("excel文件总数为：" + str(count))
excel_number = count    #excel文件总数

for x in excelfile.iterdir():
    # name = os.path.basename(x).split('.')[0]
    wave = pd.read_excel(x, header=None, skiprows=[0])
    #将所有CSV存放为一个列表，便于后面pd.concat()函数进行拼接
    files.append(wave)
    i += 1
    print('remain：' + '' + str(excel_number - i))

#excel文件拼接
result = pd.concat(files)
#准备进行拼接的文件数
print(len(files))
#拼接后的csv长度
print(len(result))
#完成拼接后，存储为一个新的CSV
result.to_excel('泥晶灰岩.excel', encoding='utf-8')
# print('ok')

end = time.perf_counter()
print("final is in ", str(end-start) +" 秒")
