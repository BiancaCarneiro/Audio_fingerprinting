import acoustid
import chromaprint
import pandas as pd



f1 = chromaprint.decode_fingerprint(acoustid.fingerprint_file("th1.mp3")[1])[0]
f2 = chromaprint.decode_fingerprint(acoustid.fingerprint_file("th2.mp3")[1])[0]
# print(f1, f2)
f1 = chromaprint.hash_fingerprint(f1)
f2 = chromaprint.hash_fingerprint(f2)


# Creates database
data = []
df = pd.DataFrame(data, columns=['Name', 'Fingerprint'])
musica1_nome = "th1.mp3"
musica2_nome = "th2.mp3"
dic1 = {'Name':musica1_nome, 'Fingerprint':f1}
dic2 = {'Name':musica2_nome, 'Fingerprint':f2}
df = df.append(dic1)
df = df.append(dic2)
print(bin(f1), bin(f2))

# Compare the binary strings using Hamming distance.
first_fp_binary = format(f1, 'b')
second_fp_binary = format(f2, 'b')

# This value will be between 0 and 32 and represent the POPCNT.
# A value > 15 indicates the two fingerprints are very different.
print(bin(int(first_fp_binary,2)^int(second_fp_binary,2)))

# Saves database
df.to_csv("output.csv")