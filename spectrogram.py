# pip install matplotlib
# pip install pydub
# sudo apt-get install ffmpeg
# pip install scipy
import numpy as np      
import matplotlib.pyplot as plt 
import librosa
import librosa.display
from matplotlib import cm
from pydub import AudioSegment    

FRAME_SIZE = 2048
HOP_SIZE = 512

def to_wav(path, name):                           
    if not path.endswith(".wav"):
        if path.endswith(".mp3"):                                 
            sound = AudioSegment.from_mp3(path)
            sound.export("wav/"+name+".wav", format="wav")
        else:
            raise ValueError ("Nor mp3 or wav")
    return "wav/"+name+".wav"

def create_spectrogram(path):
    name = path.split("/")[-1][:-4]
    print("Estou rodando " + name)
        
    data, rate = librosa.load(path) 
    
    data_1D = librosa.stft(data, n_fft=FRAME_SIZE, hop_length=HOP_SIZE)    
    Y_scale = np.abs(data_1D)**2
    Y_scale = librosa.power_to_db(Y_scale,ref=np.max)
    fig_spec = plt.figure()
    librosa.display.specshow(Y_scale,sr=rate, hop_length=HOP_SIZE, x_axis="time", y_axis="log",cmap=cm.jet)
    plt.title("Spectrogram of " + name)
    plt.colorbar(format='%+02.0f dB')
    plt.tight_layout()
    fig_spec.savefig("spectrograms/" + name + "_spectrogram.png", format="png") 
    

    