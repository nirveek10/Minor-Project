import random
from tkinter.constants import END
from PIL import Image

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename

def encode():
    ent_dec_name.delete(0,tk.END)
    ent_keyin.delete(0,tk.END)
    ent_dec_msg.delete(0,tk.END)
    img = ent_img_name.get()
    image = Image.open(img, 'r')

    data = ent_msg.get()
    if (len(data) == 0): 
	    raise ValueError('Data is empty')

    newimg = image.copy()
    key = pattern(newimg, data)

    outname = ent_new_name.get()
    newimg.save(outname, str(outname.split(".")[1].upper()))
    print("The key is: ",key)
    ent_key.insert(tk.END,key)

def pattern(img, data):
    length = img.size[0]
    (x, y) = (0, 0)
    key = random.randint(1, 9)

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

    for  k in range(datalen * key):
        pixlist = [value for value in imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] + 
                                      imgdata.__next__()[:3] ]
        
        if (k % key == 0):
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

def decod():
    ent_img_name.delete(0, tk.END)
    ent_msg.delete(0, tk.END)
    ent_new_name.delete(0, tk.END)
    ent_key.delete(0, tk.END)
    msg=decode()
    ent_dec_msg.insert(tk.END,msg)

def decode():
    img = ent_dec_name.get()
    image = Image.open(img, 'r')
    key = int(ent_keyin.get())

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
        i += 1

window = tk.Tk()
window.title("Image Steganography")
window.rowconfigure(0, minsize=500, weight=1)
window.columnconfigure(1, minsize=500, weight=1)

    
fr_buttons = tk.Frame(window, relief=tk.RAISED, bd=2)
fr_buttons.grid(row=0, column=0, sticky="ns")

btn_open = tk.Button(fr_buttons, text="encode",command=encode)
btn_save = tk.Button(fr_buttons, text="decode",command=decod)

btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_input1 = tk.Frame(window)
frm_input1.grid(row=0, column=1, sticky="nsew" )


frm_input2=tk.Frame(window)
frm_input2.grid(row=0, column=3, sticky="nsew")

lbl_img_name = tk.Label(master=frm_input1, text="Enter image name for encode:")
ent_img_name = tk.Entry(master=frm_input1, width=50)
lbl_img_name.grid(row=0, column=1, sticky="e")
ent_img_name.grid(row=0, column=2)

lbl_msg = tk.Label(master=frm_input1, text="Enter data/message for encode")
ent_msg = tk.Entry(master=frm_input1, width=50)
lbl_msg.grid(row=1, column=1, sticky="e")
ent_msg.grid(row=1, column=2)

lbl_new_name = tk.Label(master=frm_input1, text="Enter new image name:")
ent_new_name = tk.Entry(master=frm_input1, width=50)
lbl_new_name.grid(row=3, column=1, sticky="e")
ent_new_name.grid(row=3, column=2)

lbl_key = tk.Label(master=frm_input1, text="The key is:")
ent_key = tk.Entry(master=frm_input1, width=50)
lbl_key.grid(row=4, column=1, sticky="e")
ent_key.grid(row=4, column=2)

lbl_dec_name = tk.Label(master=frm_input2, text="Enter image name for decode:")
ent_dec_name = tk.Entry(master=frm_input2, width=50)
lbl_dec_name.grid(row=5, column=1, sticky="e")
ent_dec_name.grid(row=5, column=2)

lbl_keyin = tk.Label(master=frm_input2, text="Enter key:")
ent_keyin = tk.Entry(master=frm_input2, width=50)
lbl_keyin.grid(row=6, column=1, sticky="e")
ent_keyin.grid(row=6, column=2)

lbl_dec_msg = tk.Label(master=frm_input2, text="The decoded msg is:")
ent_dec_msg = tk.Entry(master=frm_input2, width=50)
lbl_dec_msg.grid(row=7, column=1, sticky="e")
ent_dec_msg.grid(row=7, column=2)


window.mainloop()