import pandas as pd
from pathlib import *
import os
import time
start = time.perf_counter()

p = Path('./data/hegai')  #***************************************************************
i = 0       #当前excel文件序数
count = 0   #计数器

#统计excel文件总数
for file in os.listdir(p):
    count += 1
print("excel文件总数为：" + str(count))
excel_number = count    #excel文件总数

for x in p.iterdir():
    name = os.path.basename(x).split('.')[0]
    # print(name)
    data_xls = pd.read_excel(Path(x), index_col=None, engine='xlrd')
    csvname = name+'.csv'
    csvpath = Path('./data/hegaiCSV', csvname) #*****************************************
    data_xls.to_csv(csvpath, encoding='utf-8')
    print(name+' '+"已转换完成")
    i += 1
    print('待处理的excel文件数量：'+''+str(excel_number - i) + "/"+str(excel_number))

end = time.perf_counter()
print("final is in ", str(end-start) +" 秒")
