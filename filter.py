from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
from scipy.signal import hann, boxcar, butter, lfilter, freqz
from scipy.fftpack import rfft
import numpy as np
import os


lowcut = 100.0
highcut = 7000.0

root_en = r'D:\audios\en\16000'
root_de = r'D:\audios\de\9ppl\16000'
root_de2 = r'D:\audios\de\16000'
root_ru = r'D:\audios\ru\16000'

root = root_de2

files = []

for file in os.listdir(root):
    if os.path.isfile(os.path.join(root, file)):
        files.append(file)


def butter_bandpass(lowcut, highcut, fs, order=5):
    nyq = 0.5 * fs
    low = lowcut / nyq
    high = highcut / nyq
    b, a = butter(order, [low, high], btype='band')
    return b, a


def butter_bandpass_filter(data, lowcut, highcut, fs, order=5):
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    y = lfilter(b, a, data)
    return y


def draw(audio, xmin=None, xmax=None, ymin=None, ymax=None):
    if xmin is None:
        xmin=0
    if xmax is None:
        xmax=len(audio)
    if ymin is None:
        ymin=min(audio)
    if ymax is None:
        ymax=max(audio)
    for a in audio:
        plt.plot(a[0:len(a)])
    # label the axes
    plt.ylabel("Amplitude")
    plt.xlabel("Time (samples)")
    # set the title
    plt.title("Voice message")
    plt.xlim([xmin, xmax])
    plt.ylim([ymin, ymax])
    # display the plot
    plt.show()



for file in files:
    filepath = os.path.join(root, file)
    # read audio samples
    input_data = read(filepath)
    audio = input_data[1]
    #draw([audio])
    
    order = 6
    fs = float(input_data[0])
    
    
    b, a = butter_bandpass(lowcut, highcut, fs, order=order)
    w, h = freqz(b, a, worN=512)
    
    #plt.plot((fs * 0.5 / np.pi) * w, abs(h), label="order = %d" % order)
    #plt.show()
    
    y = butter_bandpass_filter(audio, lowcut, highcut, fs, order=order)
    
    z = np.array(y, np.int16)
    
    #draw([audio,y], xmin=10000, xmax=10200, ymin=-11000, ymax=11000)
    
    out_file = os.path.join(root, 'filtered', file)
    
    write(out_file, input_data[0], z)
