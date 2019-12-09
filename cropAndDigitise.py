from ImageManager import ImageManager

fontSizes = ["24", "28", "32", "36", "40", "44", "48", "56", "72"]
fileNumbers = [str(5+3*i) for i in range(52)]

def cropAndDigitiseDataset(charType, font):
    oldPathStump = "res/dataset/"
    newPathStump = "res/dataset (cropped and digitised)/"

    print(charType + "," + font)
    
    for i in range(len(fontSizes)):
        for j in range(len(fileNumbers)):
            
            pathStem = charType + "/" + font + "/" + fontSizes[i] + "/line_" + fileNumbers[j] + ".bmp"
            img = ImageManager.openImage(oldPathStump + pathStem)
            
            ImageManager.toDigital(img)
            pixelArray = list(img.getdata())

            #get rid of black box on left hand side of A and 0 images
            if j == 0:
                blackFound = False
                
                for k in range(img.width):
                    if (0,0,0) in pixelArray[k::img.width]:
                        blackFound = True
                    elif blackFound:
                        img = img.crop((k+1, 0, img.width, img.height))
                        break
                    
            #crop whitespace around image
            img = ImageManager.cropWhiteBorder(img)
            
            ImageManager.saveImage(img, newPathStump + pathStem)                                      
    

if __name__ == "__main__":
    cropAndDigitiseDataset("Letters", "Arial")
    cropAndDigitiseDataset("Letters", "Times New Roman")

    fileNumbers = fileNumbers[:10]
    cropAndDigitiseDataset("Numbers", "Arial")
    cropAndDigitiseDataset("Numbers", "Times New Roman")
    
    
    
