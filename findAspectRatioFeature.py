from ImageManager import ImageManager
import os

fontSizes = ["24", "28", "32", "36", "40", "44", "48", "56", "72"]
fileNumbers = [str(5+3*i) for i in range(52)]

def findAspectRatioFeature(charType, font):
    pathStump = "res/dataset (cropped and digitised)/"

    print(charType + "," + font)
    
    for i in range(len(fontSizes)):
        for j in range(len(fileNumbers)):
            
            pathStem = charType + "/" + font + "/" + fontSizes[i] + "/line_" + fileNumbers[j] + ".bmp"
            img = ImageManager.openImage(pathStump + pathStem)

            aspectRatio = img.height/img.width

            items = [pathStem, str(aspectRatio)]
            with open("res/aspectRatios.txt", "a") as f:
                f.write(",".join(items) + "\n")

    

def featureScale():
    total = 0
    high = -9999
    low = 9999
        
    ratios = []
    with open("res/aspectRatios.txt", "r") as f:
        ratios = f.read().split("\n")
    
    n = len(ratios)
    
    for i in range(n):
        ratios[i] = ratios[i].split(",")
        ri = float(ratios[i][1])
        total += ri
        high = max(ri, high)
        low = min(ri, low)

    mean = total/n
    range_ = high - low

    for i in range(n):
        ratios[i][1] = str((float(ratios[i][1]) - mean) / range_ + 0.5)
        ratios[i] = ",".join(ratios[i])

    open("res/aspectRatios.txt", "w").close()
    
    with open("res/aspectRatios.txt", "a") as f:
        f.write("\n".join(ratios))
    
if __name__ == "__main__":
    if os.path.exists("res/aspectRatios.txt"):
        os.remove("res/aspectRatios.txt")
        
    findAspectRatioFeature("Letters", "Arial")
    findAspectRatioFeature("Letters", "Times New Roman")

    fileNumbers = fileNumbers[:10]
    findAspectRatioFeature("Numbers", "Arial")
    findAspectRatioFeature("Numbers", "Times New Roman"

    featureScale()
