import pandas as pd


def prunning(file):
    df = pd.read_csv(file)
    print("Read file: Done")
    reviews = df["Reviews"].tolist()[:10]
    f = open(file)
    for line in f.readlines():
        word = line.replace("\n", "")

        print(word)


prunning("extracted/target.txt")