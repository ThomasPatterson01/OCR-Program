import numpy as np
from PIL import Image

import tkinter
from tkinter import filedialog
from tkinter import messagebox

from ImageManager import ImageManager
from trainNetwork import loadXandYMatrices, sigmoid

def testDataset():
    X, Y = loadXandYMatrices(0, 1116)
    
    theta1 = np.matrix(np.loadtxt("weights/3-2000-theta1.txt"))
    theta2 = np.matrix(np.loadtxt("weights/3-2000-theta2.txt"))

    h1 = sigmoid(X * theta1.getT())
    a = np.ones((1116, 1))
    h1 = np.concatenate((a, h1), axis=1)
    h2 = sigmoid(h1 * theta2.getT())
    
    predictions = np.argmax(h2, axis = 1)

    correct = 0
    for i in range(len(Y)):
        if int(Y.item(i)) == int(predictions.item(i)):
            correct += 1
        print("Actual: " + str(Y[i]) + "   Predicted: " + str(predictions[i]))

    print(correct/len(Y))

def lineSegmentation(filepath):
    img = ImageManager.openImage(filepath)
    blackFound = False

    ImageManager.toDigital(img)

    px = img.load()

    lines = []
    prevHeight = 0
    
    for i in range(img.height):
        containsBlack = False
        for j in range(img.width):
            if px[(j,i)] == (0,0,0):
                containsBlack = True
                break
        if containsBlack:
            blackFound = True
        elif blackFound:
            if i < img.height - 3:
                i += 2
            lines.append(img.crop((0, prevHeight+1, img.width, i)))
            prevHeight = i        
            for j in range(img.width):
                px[(j, i)] = (0,255,0)
                blackFound = False

    if blackFound and prevHeight < img.height-1:
        lines.append(img.crop((0, prevHeight+1, img.width, img.height)))

    return lines

def wordSegmentation(img):
    blackFound = False


    img = ImageManager.cropWhiteBorder(img)
    
    px = img.load()

    words = []
    prevWidth = 0
    for i in range(img.width):
        containsBlack = False
        for j in range(1, img.height):
            if px[(i,j)] == (0,0,0):
                containsBlack = True
                break
        if containsBlack:
            blackFound = True
        elif blackFound:
            k = i
            while k < img.width-1:
                containsBlack = False
                for j in range(1, img.height):
                    if px[(k,j)] == (0,0,0):
                        containsBlack = True
                        break
                if containsBlack:
                    if (k-i) > 0.2*img.height:
                        if i < img.width - 3:
                            i += 2
                        words.append(img.crop((prevWidth+1, 0, i, img.height)))
                        prevWidth = i
                        for j in range(img.height):
                            px[(i, j)] = (0,255,0)
                    break
                k += 1
            blackFound = False
            
    if prevWidth < img.width - 1:
        words.append(img.crop((prevWidth+1, 0, img.width, img.height)))

    return words

def charSegmentation(img, num1, num2):
    blackFound = False
    
    #img = ImageManager.cropWhiteBorder(img)
    #ImageManager.saveImage(img, "temp/cropped.jpg")

    px = img.load()

    chars = []
    prevWidth = 0
    
    for i in range(img.width):
        containsBlack = False
        for j in range(2, img.height):
            if px[(i,j)] == (0,0,0):
                containsBlack = True
                break
        if containsBlack:
            blackFound = True
        elif blackFound:
            containsBlack = False
            for j in range(2, img.height):
                if i+1 == img.width:
                    break
                if px[(i+1,j)] == (0,0,0):
                    containsBlack = True
                    break
            if not containsBlack:
                chars.append(img.crop((prevWidth+1, 0, i, img.height)))
                prevWidth = i
                for j in range(2, img.height):
                    px[(i, j)] = (0,255,0)
                    blackFound = False

    if blackFound and prevWidth < img.width:
        chars.append(img.crop((prevWidth+1, 0, img.width, img.height)))
    #ImageManager.saveImage(img, "temp/charSegmented-" + str(num1) + "-" + str(num2) + ".jpg")

    return chars

def predict(img, num):
    results = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
    results += results.lower() + "0123456789"
    
    img = ImageManager.cropWhiteBorder(img)

    aspectRatio = np.matrix(img.height/img.width)
    
    img = img.resize((20, 24))
    
    pixels = ImageManager.getDigitalPixels(img)
    X = np.matrix(pixels).astype(np.float)
    one = np.matrix("1")
    X = np.concatenate((one, X, aspectRatio), axis=1)

    theta1 = np.matrix(np.loadtxt("weights/3-2000-theta1.txt"))
    theta2 = np.matrix(np.loadtxt("weights/3-2000-theta2.txt"))

    h1 = sigmoid(X * theta1.getT())
    
    h1 = np.concatenate((one, h1), axis=1)
    h2 = sigmoid(h1 * theta2.getT())
    predictions = np.argmax(h2, axis = 1)
    
    return results[predictions.item(0,0)]

translatedText = None
window = None

def main():
    global translatedText
    global window

    #creates window in centre of screen
    window = tkinter.Tk()
    window.title("Optical Character Recognition")
    #window.configure(background="white")
    
    screenH = window.winfo_screenheight()
    screenW = window.winfo_screenwidth()
    
    #window.geometry("990x700+{0}+{1}".format(int(screenW/2-495),int(screenH/2-350)))
    window.resizable(width=False, height=False)

    title = tkinter.Label(window, text="Optical Character Recognition", font=("Arial", 25))
    title.grid(row=0, columnspan = 2)

    uploadImageBTN = tkinter.Button(window, text="Upload Image", font=("Arial", 10), command=uploadImage)
    uploadImageBTN.grid(row=1, pady = 20, padx = 40, sticky="w")

    translatedText = tkinter.Label(window, text="Deciphered text will show here ", font=("Arial", 10))
    translatedText.grid(row=1, column=1)

    window.mainloop()

def uploadImage():
    
    filepath = filedialog.askopenfilename(title="Select Image", filetypes=[("JPEG files", "*.jpg")])

    if filepath == "":
            messagebox.showinfo("Error", "No image selected")
            return
        
    translatedText['text'] = "Processing..."
    window.update()

    
    lines = lineSegmentation(filepath)

    #for i in range(len(lines)):
    text = ""
    num = 0
    for i in range(len(lines)):
        words = wordSegmentation(lines[i])
        for j in range(len(words)):
            chars = charSegmentation(words[j], i, j)
            for k in range(len(chars)):
                num += 1
                #chars[k] = chars[k].resize((chars[k].width*2, chars[k].height*2))
                #ImageManager.saveImage(chars[k], "temp/char.jpg")
                text += predict(chars[k], num)
                translatedText['text'] = text + "..."
                window.update()
            text += " "
        text += "\n"
    
            
    
    #result = predict(filepath)
    #print(result)
    translatedText['text'] = text
    

if __name__ == "__main__":
    main()
    #testDataset()
