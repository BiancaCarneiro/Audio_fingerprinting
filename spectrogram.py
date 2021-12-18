# pip install matplotlib
# pip install pydub
# sudo apt-get install ffmpeg
# pip install scipy
import numpy as np      
import matplotlib.pyplot as plt 
import scipy.io.wavfile 
from pydub import AudioSegment    
from scipy import signal
from scipy.signal import find_peaks

def to_wav(path, name):                                                            
    sound = AudioSegment.from_mp3(path)
    sound.export("wav/"+name+".wav", format="wav")
    return "wav/"+name+".wav"

def create_spectrogram(path):
    name = path.split("/")[-1][:-4]
    
    if not path.endswith(".wav"):
        if path.endswith(".mp3"):
            path = to_wav(path, name)
        else:
            print("ERROR: Nor mp3 or wav")
            return -1
    
    rate, data = scipy.io.wavfile.read(path)        
    data_1D = data.flatten()
    fig_spec = plt.figure()
    plt.specgram(data_1D, NFFT = 64, Fs = 64, noverlap=32)  
    fig_spec.savefig("spectrograms/" + name + "_spectrogram.png", format="png")  
    get_peaks(data,name) 
    
def get_peaks(audio, name):
    peaks = np.argmax(audio, axis=1)
    fig_peak = plt.figure()
    plt.plot(peaks)
    fig_peak.savefig("peaks/" + name + "_peaks.png", format="png")