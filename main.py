from spectrogram import create_spectrogram
from match import do_match

def main():
    tests = [
        "wav/lakehouse.wav",
        "wav/mountain-sound.wav",
        "wav/01_Do_I_Wanna_Know.wav",
        "wav/02_R_U_Mine.wav",
        "wav/from-finner.wav",
        "mp3/Tu y Yo (Feat. Chris Marshall).mp3",
        "mp3/tropicana.mp3",
        "mp3/Sin Miedo (Feat. DJ Luian & Mambo Kingz).mp3",
        "mp3/pelas ruas que andei.mp3"
    ] 
    for test in tests:
        print("Vou rodar " + test + "\n")
        do_match(test) 
        print("_"*100)
        print("\n")
        

if __name__ == '__main__':  
    main()