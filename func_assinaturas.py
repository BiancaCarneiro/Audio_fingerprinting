import numpy as np
import scipy

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