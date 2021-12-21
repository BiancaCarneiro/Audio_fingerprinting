from spectrogram import create_spectrogram
from match import do_match

def main():
    tests = [
        "Arctic Monkeys - Do I Wanna Know_  (Live).mp3",
        "Arctic Monkeys - Do I Wanna Know_ Acoustic LIVE _ Radio X (128 kbps).mp3",
        "Do I Wanna Know - Arctic Monkeys (Acoustic Cover) (128 kbps).mp3",
        "Do I Wanna Know_ - Arctic Monkeys Cover (featuring Sterling R Jackson).mp3"
        #"wav/from-finner.wav"
        # "mp3/Tu y Yo (Feat. Chris Marshall).mp3",
        # "mp3/tropicana.mp3",
        # "mp3/Sin Miedo (Feat. DJ Luian & Mambo Kingz).mp3",
        # "mp3/pelas ruas que andei.mp3"
    ] 
    for test in tests:
        # create_spectrogram(test)
        print("Vou rodar " + test + "\n")
        do_match(test) 
        print("_"*100)
        print("\n")
        

if __name__ == '__main__':  
    main()