# pip install matplotlib
# pip install pydub
# sudo apt-get install ffmpeg
# pip install scipy
import os
import librosa
import librosa.display
import IPython.display as ipd
import numpy as np 
import matplotlib.pyplot as plt 
from scipy import signal
from scipy.io import wavfile
from pydub import AudioSegment

FRAME_SIZE = 2048
HOP_SIZE = 512

def to_wav(path):                                                            
    sound = AudioSegment.from_mp3(path)
    name = path.split("/")[-1]
    sound.export("wav/"+name, format="wav")
    return "wav/"+name

def show_spectrogram(path):
    if not path.endswith(".wav"):
        if path.endswith(".mp3"):
            path = to_wav(path)
        else:
            print("ERROR: Nor mp3 or wav")
            return -1
        
    ipd.Audio(path)
    signal, sample_rate = librosa.load(path)
    
    # Calculando a short-time fourier transform
    S_scale = librosa.stft(signal, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)    
    
    # Calculando o spectrogram
    Y_scale = np.abs(S_scale)**2
    Y_scale = librosa.power_to_db(Y_scale)
    plt.figure(figsize=(25, 10))
    librosa.display.specshow(Y_scale, sr=sample_rate, hop_length=HOP_SIZE, x_axis="time", y_axis="log")
    plt.colorbar(format="%+2.f")
    plt.savefig("spectrogram.png", format="png")
show_spectrogram("foo.wav")