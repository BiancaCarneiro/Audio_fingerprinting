import librosa
import os
import numpy as np
import pandas as pd
from func_assinaturas import fingerprint
from spectrogram import to_wav

def create_database():
    data = {
            "Fingerprint": [],
            "Name" : []
        }
    
    mp3s = os.listdir("mp3") # Lista o nome dos arquivos dentro da pasta mp3
    count = 0
    #mp3s = os.listdir("wav")
    for name in mp3s:
        mp3_path = "mp3/" + name
        name_musica = name[:-4]
        mp3_path = to_wav(mp3_path, name_musica)
        sample, sample_rate = librosa.load(mp3_path, sr=None) #Carrega o arquivo
        fing = fingerprint([sample],sample_rate,1,len(sample))
        print(np.shape(fing))
        data["Fingerprint"].append(fing[0].tolist())
        name_musica = name_musica.replace("_", " ")
        name_musica = name_musica.replace("-", " ")
        data["Name"].append(name_musica.lower())
        os.remove(mp3_path)
    df = pd.DataFrame.from_dict(data)
    df.to_csv("Fingerprint_database.csv", index=False)
    
create_database()