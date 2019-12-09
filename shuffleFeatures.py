import os
from random import randint

def fisherYatesShuffle(array):
    for i in range(len(array)-1, 0, -1):
        j = randint(0, i)
        array[i], array[j] = array[j], array[i]

if __name__ == "__main__":
    features = []
    
    with open("res/features.txt", "r") as f:
        features = f.read().split("\n")

    fisherYatesShuffle(features)

    with open("res/shuffledFeatures.txt", "w") as f:
        f.write("\n".join(features))
        

    
