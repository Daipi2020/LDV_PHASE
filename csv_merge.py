import time
import pandas as pd
from pathlib import *
import os
start = time.perf_counter()

i = 0       #当前csv文件序数
count = 0   #计数器
base_path = Path('./data/hegaiCSV') #************************************************
#定义一个空列表，存放从CSV中读取的波形数据
files = []
csv_path = os.listdir(base_path)
#统计csv文件总数
for file in csv_path:
    csv_name = os.path.basename(file).split('.')[0]
    count += 1
    print('文件', str(count), ':', csv_name)
print("csv文件总数为：" + str(count))
csv_number = count    #csv文件总数
#排序
csv_path.sort(key=lambda x: int((x.split('.')[0]).split('_')[-1]))

for x in base_path.iterdir():
    # name = os.path.basename(x).split('.')[0]
    wave = pd.read_csv(x, header=None, skiprows=[0])
    # wave = pd.read_csv(x, usecols=[7], header=None, skiprows=[0])
    #将所有CSV存放为一个列表，便于后面pd.concat()函数进行拼接
    files.append(wave)
    i += 1
    print('remain：' + '' + str(csv_number - i))

#csv文件拼接
result = pd.concat(files)
#准备进行拼接的文件数
print(len(files))
#拼接后的csv长度
print(len(result))
#完成拼接后，存储为一个新的CSV
result.to_csv('./hegai.csv', encoding='utf-8') #************************************
print('csv merge success')

end = time.perf_counter()
print("final is in ", str(end-start) +" 秒")
