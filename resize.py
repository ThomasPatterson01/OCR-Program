from ImageManager import ImageManager
import os

fontSizes = ["24", "28", "32", "36", "40", "44", "48", "56", "72"]
fileNumbers = [str(5+3*i) for i in range(52)]

def resize(charType, font, width, height):
    oldPathStump = "res/dataset (cropped and digitised)/"
    newPathStump = "res/dataset (resized " + str(width) + "x" + str(height) + ")/"
    
    for i in range(len(fontSizes)):
        for j in range(len(fileNumbers)):
            
            pathStem = charType + "/" + font + "/" + fontSizes[i] + "/line_" + fileNumbers[j] + ".bmp"
            img = ImageManager.openImage(oldPathStump + pathStem)

            img = img.resize((width, height))

            ImageManager.saveImage(img, newPathStump + pathStem)
            print(newPathStump + pathStem)
            

if __name__ == "__main__":
    width = 20
    height = 24
        
    resize("Letters", "Arial", width, height)
    resize("Letters", "Times New Roman", width, height)

    fileNumbers = fileNumbers[:10]
    resize("Numbers", "Arial", width, height)
    resize("Numbers", "Times New Roman", width, height)
