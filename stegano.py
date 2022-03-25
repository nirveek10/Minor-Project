import random
from PIL import Image

def encode():
    img = input("Enter image name:")
    image = Image.open(img, 'r')

    data = input("Enter data: ")
    if (len(data) == 0): 
	    raise ValueError('Data is empty')

    newimg = image.copy()
    key = pattern(newimg, data)

    outname = input("Enter the name for output: ")
    newimg.save(outname, str(outname.split(".")[1].upper()))
    return key

def pattern(img, data):
    length = img.size[0]
    (x, y) = (0, 0)
    key = random.randint(1, 4)

    for pixel in modPix(img.getdata(), data, key):
        img.putpixel((x, y), pixel)

        if (x == length - 1):
            x = 0
            y += 1
        else:
            x += 1
    
    return key

def modPix(pix, data, key):
    datalist = genData(data)
    datalen = len(datalist)
    imgdata = iter(pix)
    i = 0

    while i < datalen:
        pixlist = [value for value in imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] ]
        
        if (i % key == 0):
            for j in range(0, 8):
                if (datalist[i][j] == '0' and pixlist[j] % 2 != 0):
                    pixlist[j] -= 1
                
                elif (datalist[i][j] != '0' and pixlist[j] % 2 == 0):
                    if (pixlist[j] == 0):
                        pixlist[j] += 1
                    else:
                        pixlist[j] -= 1
            
        if (i == datalen - 1):
            if (pixlist[-1] % 2 == 0):
                if (pixlist[-1] == 0):
                    pixlist[-1] += 1
                else:
                    pixlist[-1] -= 1
        else:
            if(pixlist[-1] % 2 != 0):
                pixlist[-1] -= 1        
        i += 1

        pixlist = tuple(pixlist)
        yield pixlist[0:3]
        yield pixlist[3:6]
        yield pixlist[6:9]

def genData(data):
    newdata = []

    for i in data:
        newdata.append(format(ord(i), '08b'))
    
    return newdata

def decode():
    img = input("Enter image name: ")
    image = Image.open(img, 'r')
    key = int(input("Enter key: "))

    data = ''
    imgdata = iter(image.getdata())
    i = 0

    while(True):
        pixlist = [value for value in imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] ]
        binstr = ''
        
        if (i % key == 0):
            for j in pixlist[:8]:
                if (j % 2 == 0):
                    binstr += '0'
                else:
                    binstr += '1'            
            data += chr(int(binstr, 2))
        
        if (pixlist[-1] % 2 != 0):
            return data



command = int(input("1. Encode   2. Decode\n"))

if (command == 1):
    print("The key is: ", encode())
elif (command == 2):
    print("Decoded data: ", decode())
else:
    raise Exception("Enter correct input")
