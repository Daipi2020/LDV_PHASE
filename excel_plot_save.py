from matplotlib import pyplot as plt
from pathlib import *
import pandas as pd
import numpy as np
import time
import os

current_path = os.getcwd()
print('当前路径：', os.getcwd())
start = time.perf_counter()
################################################################################################################
##########################                                                      ################################
##########################                excel文件 转换为 csv文件                 ################################
##########################                                                      ################################
################################################################################################################
path_key0 = '15'
path_key1 = 'Y'
#上面的path_key0和path_key1 是自己定义的两个关键字，用来指定 相关地址。这种表示方法在后期可能采用别的方法来优化，或者通过遍历来处理。
excelpath = current_path + '/' + path_key0 + '/' + path_key1    #待转换的excel 文件地址
# print('excelpath:', str(excelpath))
csvpath = excelpath + '-CSV'    #转换出的csv文件的存储地址
# print('csvpath:', str(csvpath))

p = Path(excelpath)
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
    name = name + '.csv'
    target_path = Path(csvpath, name)
    data_xls.to_csv(target_path, encoding='utf-8')
    print(name+' '+"已转换完成")
    i += 1
    print('待处理的excel文件数量：'+''+str(excel_number - i) + "/"+str(excel_number))
print('excel文件已全部转换为csv文件')
################################################################################################################
##########################                                                      ################################
##########################                      csv文件合并                       ################################
##########################                                                      ################################
################################################################################################################
i = 0       #当前csv文件序数
count = 0   #计数器
base_path = Path(csvpath)
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
#新CSV的存储地址
new_csv = path_key0 + path_key1 + '.csv'
result.to_csv(new_csv, encoding='utf-8')
print('csv合并已完成')
################################################################################################################
##########################                                                      ################################
##########################                根据csv文件中的列或行的数据来画图         ################################
##########################                                                      ################################
################################################################################################################
figsave_path = './'+path_key0
# figsave_path = os.path.join(base_path, str(1)) #图片存储地址
print('图片存储地址:'+ figsave_path)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 这两行需要手动设置

#从CSV中读取时间列
# x_time = pd.read_csv('PSD光楔.csv', usecols=[1], header=None)
#从CSV中读取指定的数据列  usecols 参数
wave = pd.read_csv(new_csv, usecols=[8], header=None, dtype={"1": float})
# wave = pd.read_csv(new_csv, usecols=[8], dtype={"Voltage_0 3": float}, low_memory=False)
#转换为数值，便于后续数据处理，比如FFT
# x_time =x_time.values
wave = wave.values
#取有效数据
# x_time = x_time[1:]
wave = wave[1:]
# print('拼接后的时间列： ', x_time)
# print('拼接后的电压值列： ', wave)

#使用reshape()函数将N维数组转换为一维数组,https://blog.csdn.net/baidu_41805096/article/details/108680836
# 这里是从n*1变成了1*n

# x_time1 = x_time.reshape(-1)
wave1 = wave.reshape(-1)
# print('将时间列转换为1维数组，即： ', x_time1)
# print('将电压值列转换为1维数组，即： ', wave1)
# print(type(wave1))
print('采样点数：' + str(len(wave1)))

plt.figure(1)
#绘制时频图
framerate = 10000 #采样率
framelength = 0.05 #帧长50ms
framesize = framelength * framerate #每帧点数 N = t*fs,通常情况下值为256或512,要与NFFT相等\
                                    #而NFFT最好取2的整数次方,即framesize最好取的整数次方

#找到与当前framesize最接近的2的正整数次方
nfftdict = {}
lists = [32,64,128,256,512,1024]
for i in lists:
    nfftdict[i] = abs(framesize - i)
sortlist = sorted(nfftdict.items(), key=lambda x: x[1])#按与当前framesize差值升序排列
framesize = int(sortlist[0][0])#取最接近当前framesize的那个2的正整数次方值为新的framesize

NFFT = framesize #NFFT必须与时域的点数framsize相等，即不补零的FFT
overlapSize = 1.0/2 * framesize #重叠部分采样点数overlapSize约为每帧点数的1/3~1/2
overlapSize = int(round(overlapSize))#取整

# plt.specgram(wave1, NFFT=2000, Fs=20000, noverlap=500, scale=None, mode=None)

plt.specgram(wave1, NFFT=NFFT, Fs=framerate, window=np.hanning(M=framesize), cmap=None,
                                     noverlap=overlapSize, mode='default', scale_by_freq=True, sides='default', scale='dB', xextent=None)

fig_title = path_key1

#设置坐标轴名称
plt.xlabel("frame_number")
plt.ylabel("Frequency / Hz")
####################################################################################
#************由于数据的频谱中出现的混叠，这里对纵轴进行了缩放和裁剪。  混叠的原因还未找到
ymax = framerate//2
plt.ylim(0, ymax//2)
plt.yticks(np.linspace(0, ymax//2, 11), np.linspace(0, ymax, 11), fontsize=8)


# plt.xlim(0, 90)
title1 = fig_title + '-时频图'
plt.title(title1, fontsize=18)
save_name1 = figsave_path + '/' + title1 + '.png'
#网格线设置
plt.grid(linestyle=":", color='black')        #****************************

#保存图片
plt.savefig(save_name1)

plt.figure(2)
# #绘制时域图
plt.plot(wave1)
# plt.xlim(3e5, 4e5)
# plt.ylim(-0.05, 0.1)
plt.xlabel("sample_number")
plt.ylabel("Amplitude / V")
title2 = fig_title + '-时域图'
plt.title(title2, fontsize=18)#************************************************
# plt.plot(wave1[:2000000])
save_name2 = figsave_path + '/' + title2 + '.png'
plt.grid(linestyle=":",  color='black')      #****************************
#保存图片
plt.savefig(save_name2)
#显示图像
plt.show()
################################################################################################################
##########################                                                      ################################
##########################                      END                             ################################
##########################                                                      ################################
################################################################################################################
end = time.perf_counter()
print("final is in ", str(end-start) +" 秒")