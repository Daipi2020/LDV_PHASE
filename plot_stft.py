import pandas as pd
from scipy import signal
from matplotlib import pyplot as plt
import numpy as np
import os

base_path = os.getcwd()
# figsave_path = os.path.join(base_path, 'DATA') # stft图片存储地址
figsave_path = base_path
print('stft图片存储地址:', figsave_path)
plt.rcParams['font.sans-serif'] = ['SimHei']  # 显示中文标签
plt.rcParams['axes.unicode_minus'] = False   # 这两行需要手动设置

#csv文件读取
# name_csvfile = '合盖'
dir_csvfile = './hegai.csv'
name_csvfile = dir_csvfile.split('.csv')[0]  #以 .csv 来分割dir_csvfile,并返回列表，取其第1个元素。此行的作用是 除去后缀 .csv
name_csvfile = name_csvfile.split('/')[-1]   #以 / 来分割字符串，并返回列表，取其倒数第1个元素。此行的作用是 除去多余的地址字符串，只保留csv文件名
col_name = 'w'     # 当前所读取的列 的名字
name_csvfile = name_csvfile + ' ' + col_name
print('name_csvfile: ', name_csvfile)

wave = pd.read_csv(dir_csvfile, usecols=[3], skiprows=[0],  header=None)
wave = wave.values
wave = wave[1:]
print('拼接后的电压值列： ', wave)
wave1 = wave.reshape(-1)
print('采样点数：' + str(len(wave1)))

#数据段 截取
# wave1=wave1[:5700000]
#画 时频图
plt.figure(1)
Fsamplerate = 10000
nfft = 4096
hop = nfft/2
######################## 方法（1）用plt.specgram()画 时频图
# plt.specgram(wave1, NFFT=nfft, Fs=Fsamplerate, cmap='bwr',
#                                      noverlap=hop, mode='default', scale_by_freq=True, sides='default', scale='dB', xextent=None)

######################## 方法（2）用signal.stft()和plt.pcolormesh()画 时频图
f, t, Zxx = signal.stft(wave1, Fsamplerate, nperseg=nfft, noverlap=hop, nfft=nfft,window='hann',
                        return_onesided=True, padded=True, detrend=False) # nperseg代表窗函数长度，
plt.pcolormesh(t,f,np.abs(Zxx))

plt.xlabel("Time / s")
plt.ylabel("Frequency / Hz")
title1 = name_csvfile + '-时频图'
plt.title(title1, fontsize=18)
plt.ylim(0, 200)
save_name1 =title1 + '.png'
plt.savefig(save_name1)

#画 时域图
plt.figure(2)
plt.plot(wave1)
plt.xlabel("sample_number")
plt.ylabel("Amplitude / V")
title2 = name_csvfile + '-时域图'
plt.title(title2, fontsize=18)
save_name2 =title2 + '.png'
plt.savefig(save_name2)

plt.show()