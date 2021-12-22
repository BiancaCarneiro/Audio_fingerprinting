import librosa 
import numpy as np
from math import pi,sin,cos
import scipy
from matplotlib import pyplot as plt
import librosa.display 
import pandas as pd
from func_assinaturas import fingerprint
from spectrogram import to_wav
import time


def conv2Mono(sample):
    if(len(np.shape(sample))>1):
        channels = np.shape(sample)[0]
        sample = np.array(sample)
        for j in range(channels-1):
            sample[0] += sample[j+1]
        sample[0]/=channels
        sample = sample[0]
    return sample

def cmpFing(f1, f2):
    # print(type(f1))
    f1 = np.reshape(np.array(f1), -1) # Linearizar
    # print(np.shape(f1))
    # f1/=np.sqrt(len(f1))
    # print(type(f2))
    f2 = np.reshape(np.array(f2), -1)
    # print(np.shape(f2))
    # f2/=np.sqrt(len(f2))

    f2 = f2[::-1]

    f1 = np.append(f1, np.zeros(max(len(f1),len(f2))-len(f1))) # Preencher com 0s
    f2 = np.append(f2, np.zeros(max(len(f1),len(f2))-len(f2)))

    f1=f1/np.sqrt(len(f1)) # Normalizar
    f2=f2/np.sqrt(len(f2))

    # return max(np.convolve(f1, f2))

    f1 = scipy.fft.fft(f1) # Transformar para o domínio das frequências
    f2 = scipy.fft.fft(f2)
    
    return max(scipy.fft.ifft(f1[:int(len(f1)/2)] * f2[:int(len(f2)/2)])) # Convolução no dominio do tempo -> multiplicação no dominio da frequência


def do_match(path):
    dt = time.time()
    name = path.split("/")[-1][:-4]
    
    sample, sample_rate = librosa.load(path, sr=None) #Carrega o arquivo
    #print('Duração do som:', int(len(sample)/sample_rate/60),':', int(len(sample)/sample_rate%60))
    # print(len(sample)/sample_rate/60, 0.037*5500/60)
    # sample = conv2Mono(sample[:int(sample_rate*0.037)*5500])

    sample = sample[int(len(sample)/2):int(len(sample)/1.5)] # Obter apenas um trecho da música

    fing = fingerprint([sample],sample_rate,1,len(sample)) # Faz a fingerprint

    df = pd.read_csv("Fingerprint_database.csv")

    maxindex = -1
    maxpeak = 0
    peaklist = []

    for i, f in enumerate(df["Fingerprint"]):
        f = [int(x) for x in f.replace('[', '').replace(']','').split(',')]
        peaklist.append((cmpFing(f, fing), i))

    peaklist.sort(key = (lambda a: a[0]))
    #print(len(peaklist))
    _, x = peaklist[-1]
    nome_musica = df["Name"][x]
    #print([df["Name"][a] for _,a in peaklist])
    nome_musica = nome_musica.split(" ")
    info_df = pd.read_csv("get_info_to_database/get_info_to_database/info.csv")
    salva_nome = ""
    for nome_info in info_df["Nome"]:
        salva_nome = nome_info
        aux_match = nome_info.lower()
        aux_match = aux_match.split(" ")
        count = 0
        i = 0
        while i < len(aux_match) and i < len(nome_musica):
            if aux_match[i] == nome_musica[i]:
                count+=1
            i+=1
        if count >= len(aux_match)/2:
            #print(count)
            break
    #print(salva_nome)
    print(info_df.loc[info_df["Nome"]==salva_nome])
    # print("Escolhido:", df["Name"][maxindex])

    #print("Finalizado em ", int((time.time()-dt)/60), ':', int((time.time()-dt)%60))