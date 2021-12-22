import numpy as np
import scipy

def fingerprint(samples, sampling_rate, max_length=0)->np.ndarray:
    
    samples_per_window = int(sampling_rate*0.037) # Quantas samples por window 
    num_timeframes = int(max_length/samples_per_window) # Descobre quantos frames 
    num_bands = 25 # 25 bandas, segundo o artigo
        
    add_zero = num_timeframes - (max_length % num_timeframes) #Calculando quantos zeros serão 
                                                                # necessários para um split exato

    samples = np.append(samples,np.zeros(add_zero)) #Adicionando os zeros necessários
    
    windows = np.split(samples,num_timeframes) #Dividindo a track em frames

    fft_windows = np.empty(np.shape(windows), dtype=complex) #Criando array que receberá as transformadas
    
    for i,window in enumerate(windows):
        fft_windows[i] = scipy.fft.fft(window) #Montando os frames transformados
        

    len_frame = int(len(samples)/num_timeframes)
    add_bands_zero = num_bands - (len_frame % num_bands)#Calculando quantos zeros serão 
                                                        # necessários para um split exato
    timeframe_bands = np.empty([num_timeframes,num_bands]) #Criando array que receberá as transformadas
    for j,fft_window in enumerate(fft_windows):
        aux = np.split(np.append(fft_window,np.zeros(add_bands_zero,dtype=complex)),num_bands) # Adicionando os zeros 
                                                                                    #necessários e splitando
        timeframe_bands[j] = average(aux) #Tirando a média de cada banda de energia e montando o array 
    
    fngrprnt = treat(timeframe_bands) # Gerando o fingerprint em si a partir das bandas
    
    return fngrprnt 

def treat(timeframe_bands)->np.ndarray:
    bands = len(timeframe_bands[0]) -1#24
    time_frames = len(timeframe_bands)
    ch_fprint = np.empty([time_frames,bands],dtype=int)
    bands_frame_anterior = np.zeros(bands)
    
    for j,frame in enumerate(timeframe_bands[:time_frames-1]):
        
        for i in range(len(frame)-1):
            aux = frame[i] - frame[i+1]
            band_frame_futuro = timeframe_bands[j+1][i] - timeframe_bands[j+1][i+1]
            if(aux>bands_frame_anterior[i] and aux>band_frame_futuro): 
                ch_fprint[j][i] = 1
            else: 
                ch_fprint[j][i] = -1
            bands_frame_anterior[i] = aux
    
    return ch_fprint[1:]

def average(array_freq):
    soma = 0.
    aux = np.empty([len(array_freq),])
    for j,ary in enumerate(array_freq):
        for i in ary:
            soma += abs(i)**2 #Energia em nessa frequencia
        aux[j] = soma

    return aux