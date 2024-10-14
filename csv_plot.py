import pandas as pd
from matplotlib import pyplot as plt
from matplotlib import colors
from matplotlib.pylab import mpl
import numpy as np
from scipy.integrate import simps
from matplotlib.pyplot import plot, savefig
import os
# print('当前路径：',os.getcwd())
base_path = os.getcwd()
# figsave_path = os.path.join(base_path, 'data')
figsave_path = base_path
print(figsave_path)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 这两行需要手动设置
#############################################################################
# path_key0 = ''
# path_key1 = '2'
#上面的path_key0和path_key1 是自己定义的两个关键字，用来指定 相关地址。这种表示方法在后期可能采用别的方法来优化，或者通过遍历来处理。

#从CSV中读取时间列
# x_time = pd.read_csv('PSD光楔.csv', usecols=[1], header=None)
#从CSV中读取电压值列#************************************************
wave = pd.read_csv('./phi20220327.csv', usecols=[3], dtype={"1": float})
#转换为数值，便于后续数据处理，比如FFT
# x_time =x_time.values
wave = wave.values
#取有效数据
# x_time = x_time[1:]
wave = wave[1:]
# print('拼接后的时间列： ', x_time)
print('拼接后的电压值列： ', wave)

# print('拼接后电压值列的数组类型： ', type(wave))
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
framerate = 1000000 #采样率
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
# NFFT = 16384
overlapSize = 1.0/2 * framesize #重叠部分采样点数overlapSize约为每帧点数的1/3~1/2
overlapSize = int(round(overlapSize))#取整

# plt.specgram(wave1, NFFT=2000, Fs=20000, noverlap=500, scale=None, mode=None)

plt.specgram(wave1, NFFT=NFFT, Fs=framerate, window=np.hanning(M=framesize), cmap=None,
                                     noverlap=overlapSize, mode='default', scale_by_freq=True, sides='default', scale='dB', xextent=None)

#网格线设置
plt.grid()
# plt.grid(b="True",axis="y")
# plt.grid(b="True",axis="x")
# #设置语谱图颜色样式
# colors.Normalize(vmin=None, vmax=None, clip=False)
# #设置坐标轴范围 https://blog.csdn.net/mighty13/article/details/113812357

#设置坐标轴名称
plt.xlabel("frame_number")
plt.ylabel("Frequency / Hz")
####################################################################################
#************由于数据的频谱中出现的混叠，这里对纵轴进行了缩放和裁剪。  混叠的原因还未找到
# ymax = framerate//2
# plt.ylim(0, ymax//2)
# plt.yticks(np.linspace(0, ymax//2, 11), np.linspace(0, ymax, 11), fontsize=8)

# title1 = path_key1 + '-时频图'
title1 = '-时频图'
plt.title(title1, fontsize=18)#************************************************
save_name1 = figsave_path + '/' + title1 + '.png'
plt.savefig(save_name1)

plt.figure(2)
# #绘制时域图
plt.plot(wave1)
# plt.xlim(3e5, 4e5)
# plt.ylim(-3, 3)
plt.xlabel("sample_number")
plt.ylabel("Amplitude / V")
# title2 = path_key1 + '-时域图'
title2 = '-时域图'
plt.title(title2, fontsize=18)#************************************************
# plt.plot(wave1[:2000000])
save_name2 = figsave_path + '/' + title2 + '.png'
plt.savefig(save_name2)

plt.grid()
#显示图像
plt.show()
