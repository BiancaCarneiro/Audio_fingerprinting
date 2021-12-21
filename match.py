import librosa 
import numpy as np
from math import pi,sin,cos
import scipy
from matplotlib import pyplot as plt
import librosa.display 
import pandas as pd
import os
from spectrogram import to_wav

def treat(timeframe_bands)->np.ndarray:
    bands = len(timeframe_bands[0]) -1#24
    ch_fprint = np.empty([len(timeframe_bands),bands],dtype=int)
    bands_frame_anterior = np.zeros(bands)
    aux = np.empty(bands)
    for j,frame in enumerate(timeframe_bands):
        
        for i in range(len(frame)-1):
            aux[i] = frame[i] - frame[i+1]
            
            if(aux[i]>bands_frame_anterior[i]):
                ch_fprint[j][i] = 1
            else: 
                ch_fprint[j][i] = -1
            bands_frame_anterior[i] = aux[i]
     
    return ch_fprint[1:]

def average(array_freq):
    soma = 0.
    aux = np.empty([len(array_freq),])
    for j,ary in enumerate(array_freq):
        for i in ary:
            soma += abs(i)**2 #Energia em nessa frequencia
        aux[j] = soma

    return aux

def fingerprint(samples, sampling_rate,  channels=2, max_length=0)->np.ndarray:
    
    samples_per_window = int(sampling_rate*0.037) # Quantas samples por window 
    num_timeframes = int(max_length/samples_per_window) # Descobre quantos frames 
    num_bands = 25 # 25 bandas, segundo o artigo
    
    fngrprnt = np.empty([channels,num_timeframes-1,num_bands-1],dtype=int) #Declarando o fingerprint
    for k,ch in enumerate(samples):
        
        add_zero = num_timeframes - (max_length % num_timeframes) #Calculando quantos zeros serão 
                                                                  # necessários para um split exato

        ch = np.append(ch,np.zeros(add_zero)) #Adicionando os zeros necessários
        
        windows = np.split(ch,num_timeframes) #Dividindo a track em frames
    
        fft_windows = np.empty(np.shape(windows), dtype=complex) #Criando array que receberá as transformadas
        
        for i,window in enumerate(windows):
            fft_windows[i] = scipy.fft.fft(window) #Montando os frames transformados
           

        len_frame = int(len(ch)/num_timeframes)
        add_bands_zero = num_bands - (len_frame % num_bands)#Calculando quantos zeros serão 
                                                            # necessários para um split exato
        timeframe_bands = np.empty([num_timeframes,num_bands]) #Criando array que receberá as transformadas
        for j,fft_window in enumerate(fft_windows):
            aux = np.split(np.append(fft_window,np.zeros(add_bands_zero,dtype=complex)),num_bands) # Adicionando os zeros 
                                                                                     #necessários e splitando
            timeframe_bands[j] = average(aux) #Tirando a média de cada banda de energia e montando o array 
        
        ch_fngrprnt = treat(timeframe_bands) # Gerando o fingerprint em si a partir das bandas

        fngrprnt[k] = ch_fngrprnt #Montando o fingerprint do canal k 
    
    return fngrprnt      

def conv2Mono(sample):
    if(len(np.shape(sample))>1):
        channels = np.shape(sample)[0]
        sample = np.array(sample)
        for j in range(channels-1):
            sample[0] += sample[j+1]
        sample[0]/=channels
        sample = sample[0]
    return sample

sample, sample_rate = librosa.load("wav/01_Do_I_Wanna_Know.wav", sr=None) #Carrega o arquivo
# print(len(sample)/sample_rate/60, 0.037*5500/60)
# sample = conv2Mono(sample[:int(sample_rate*0.037)*5500])
fing = fingerprint([sample],sample_rate,1,len(sample)) # Faz a fingerprint

def cmpFing(f1, f2):
    # print(type(f1))
    f1 = np.reshape(np.array(f1), -1) # Linearizar
    # print(np.shape(f1))
    # f1/=np.sqrt(len(f1))
    # print(type(f2))
    f2 = np.reshape(np.array(f2), -1)
    # print(np.shape(f2))
    # f2/=np.sqrt(len(f2))

    f1 = np.append(f1, np.zeros(max(len(f1),len(f2))-len(f1))) # Preencher com 0s
    f2 = np.append(f2, np.zeros(max(len(f1),len(f2))-len(f2)))

    f1=f1/np.sqrt(len(f1)) # Normalizar
    f2=f2/np.sqrt(len(f2))

    # return max(np.convolve(f1, f2))

    f1 = scipy.fft.fft(f1) # Transformar para o domínio das frequências
    f2 = scipy.fft.fft(f2)
    
    return max(scipy.fft.ifft(f1[:int(len(f1)/2)] * f2[:int(len(f2)/2)])) # Convolução no dominio do tempo -> multiplicação no dominio da frequência

df = pd.read_csv("Fingerprint_database.csv")

maxindex = -1
maxpeak = 0
peaklist = []

for i, f in enumerate(df["Fingerprint"]):
    f = [int(x) for x in f.replace('[', '').replace(']','').split(',')]
    peaklist.append((cmpFing(f, fing), i))

peaklist.sort(key = (lambda a: a[0]))
print(len(peaklist))
_, x = peaklist[-1]
nome_musica = df["Name"][x]
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
        print(count)
        break
print(salva_nome)
print(info_df.loc[info_df["Nome"]==salva_nome])
# print("Escolhido:", df["Name"][maxindex])