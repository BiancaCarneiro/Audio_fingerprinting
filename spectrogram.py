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
    plt.specgram(data_1D, NFFT = 64, Fs = 64, noverlap=32)  
    plt.savefig(name+"_spectrogram.png", format="png")  
    get_peaks(data,name)

def get_peaks(audio, name):
    peaks = np.argmax(audio, axis=1)
    plt.plot(peaks)
    plt.savefig(name+"_peaks.png", format="png")  

if __name__ == '__main__':   
    create_spectrogram("mp3/01_Do_I_Wanna_Know.mp3")    
    create_spectrogram("mp3/dirty-paws.mp3") 
    create_spectrogram("mp3/02_R_U_Mine.mp3")   


