from ImageManager import ImageManager
import os

fontSizes = ["24", "28", "32", "36", "40", "44", "48", "56", "72"]
fileNumbers = [str(5+3*i) for i in range(52)]

def extractFeatures(charType, font):
    pathStump = "res/dataset (resized 20x24)/"

    print(charType + "," + font)
    
    ratios = {}
    with open("res/aspectRatios.txt", "r") as f:
        data = f.read().split("\n")

        for d in data:
            d = d.split(",")
            ratios[d[0]] = d[1]
    
    for i in range(len(fontSizes)):
        for j in range(len(fileNumbers)):
            
            pathStem = charType + "/" + font + "/" + fontSizes[i] + "/line_" + fileNumbers[j] + ".bmp"
            img = ImageManager.openImage(pathStump + pathStem)

            features = []
            if charType == "Letters":
                features = [str(j)]
            else:
                features = [str(52+j)]
                
            features += ImageManager.getDigitalPixels(img)
            features += [ratios[pathStem]]
            

            with open("res/features.txt", "a") as f:
                f.write(",".join(features) + "\n")
            

if __name__ == "__main__":

    if os.path.exists("res/features.txt"):
        os.remove("res/features.txt")
        
    extractFeatures("Letters", "Arial")
    extractFeatures("Letters", "Times New Roman")

    fileNumbers = fileNumbers[:10]
    extractFeatures("Numbers", "Arial")
    extractFeatures("Numbers", "Times New Roman")
