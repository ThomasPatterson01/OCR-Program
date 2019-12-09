from PIL import Image

class ImageManager():

    def openImage(filePath):
        img = Image.open(filePath)
        if img.mode != 'RGB':
            img = img.convert('RGB')
        return img

    def saveImage(image, filePath, fileType = None):
        image.save(filePath, fileType)

    def cropWhiteBorder(image):
        pixelArray = list(image.getdata())           
        x = 0
        y = 0
        w = image.width-1
        h = image.height-1

        
        for k in range(image.width):
            if (0,0,0) in pixelArray[k::image.width]:
                x = k - 1
                break
        for k in range(image.width-1, 0, -1):
            if (0,0,0) in pixelArray[k::image.width]:
                w = k + 2
                break
        for k in range(image.height):
            if (0,0,0) in pixelArray[image.width * k:image.width * (k+1)]:
                y = k - 1
                break
        for k in range(image.height-1, 0, -1):
            if (0,0,0) in pixelArray[image.width * (k-1):image.width * k]:
                h = k + 1
                break

        
        image = image.crop((x, y, w, h))
        return image

    def getDigitalPixels(image):
        pixelArray = list(image.getdata())
        
        digitalPixels = []
        for pixel in pixelArray:
            if pixel == (0,0,0):
                digitalPixels.append("1")
            else:
                digitalPixels.append("0")

        return digitalPixels

    def toDigital(image):
        px = image.load()
        for i in range(image.width):
            total = 0
            for j in range(image.height):
                col = px[(i, j)]
                total += col[0] + col[1] + col[2]
            total /= image.height
            threshold = total * 0.73
            for j in range(image.height):
                col = px[(i, j)]
                if col[0] + col[1] + col[2] < threshold:
                   px[(i,j)] = (0, 0, 0)
                else:
                    px[(i,j)] = (255, 255, 255)
