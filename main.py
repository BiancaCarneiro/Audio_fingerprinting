from spectrogram import create_spectrogram

def main():
    tests = [
        "wav/lakehouse.wav",
        "wav/mountain-sound.wav",
        "wav/01_Do_I_Wanna_Know.wav",
        "wav/02_R_U_Mine.wav",
        "wav/from-finner.wav"
    ] 
    for test in tests:
        create_spectrogram(test) 

if __name__ == '__main__':  
    main()