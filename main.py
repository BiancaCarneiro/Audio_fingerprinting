from spectrogram import create_spectrogram, to_wav
from match import do_match
import os

def main():
    tests = [
        "mp3/from-finner.mp3",
        "mp3/Tu y Yo (Feat. Chris Marshall).mp3",
        "mp3/tropicana.mp3",
        "mp3/Sin Miedo (Feat. DJ Luian & Mambo Kingz).mp3",
        "mp3/pelas ruas que andei.mp3"
    ] 
    for test in tests:
        # create_spectrogram(test)
        print("Vou rodar " + test + "\n")
        test = to_wav(test, "aux")
        do_match(test) 
        print("_"*100)
        print("\n")
        os.remove(test)
        

if __name__ == '__main__':  
    main()