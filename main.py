from spectrogram import create_spectrogram

def main():
    tests = [
        "mp3/lakehouse.mp3",
        "wav/mountain-sound.wav",
        "mp3/01_Do_I_Wanna_Know.mp3",
        "mp3/02_R_U_Mine.mp3",
        "mp3/from-finner.mp3"
    ] 
    for test in tests:
        create_spectrogram(test) 
if __name__ == '__main__':  
    main()