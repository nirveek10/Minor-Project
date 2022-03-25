import random
from tkinter.constants import END
from PIL import Image

import tkinter as tk
from tkinter.filedialog import askopenfilename, asksaveasfilename
A=0
def genData(data): 
		
		# list of binary codes 
		# of given data 
		newd = [] 
		
		for i in data: 
			newd.append(format(ord(i), '08b')) 
		return newd 
		
# Pixels are modified according to the 
# 8-bit binary data and finally returned 
def modPix(pix, data): 
	
	datalist = genData(data) 
	lendata = len(datalist) 
	imdata = iter(pix) 

	for i in range(lendata): 
		
		# Extracting 3 pixels at a time 
		pix = [value for value in imdata.__next__()[:3] +
								imdata.__next__()[:3] +
								imdata.__next__()[:3]] 
									
		# Pixel value should be made 
		# odd for 1 and even for 0 
		for j in range(0, 8): 
			if (datalist[i][j]=='0') and (pix[j]% 2 != 0): 
				
				if (pix[j]% 2 != 0): 
					pix[j] -= 1
					
			elif (datalist[i][j] == '1') and (pix[j] % 2 == 0): 
				pix[j] -= 1
				
		# Eigh^th pixel of every set tells 
		# whether to stop ot read further. 
		# 0 means keep reading; 1 means the 
		# message is over. 
		if (i == lendata - 1): 
			if (pix[-1] % 2 == 0): 
				pix[-1] -= 1
		else: 
			if (pix[-1] % 2 != 0): 
				pix[-1] -= 1

		pix = tuple(pix) 
		yield pix[0:3] 
		yield pix[3:6] 
		yield pix[6:9] 

def encode_enc(newimg, data): 
	w = newimg.size[0] 
	(x, y) = (0, 0) 
	
	for pixel in modPix(newimg.getdata(), data): 
		
		# Putting modified pixels in the new image 
		newimg.putpixel((x, y), pixel) 
		if (x == w - 1): 
			x = 0
			y += 1
		else: 
			x += 1
			
# Encode data into image 
def encode(): 
	img = ent_img_name.get()
	image = Image.open(img, 'r') 
	
	data = ent_msg.get()


	if (len(data) == 0): 
		raise ValueError('Data is empty') 
		
	newimg = image.copy() 
	encode_enc(newimg, data) 
	
	new_img_name = ent_new_name.get()
	newimg.save(new_img_name) 

# Decode the data in the image 
def decod(): 
    C= decode()
    ent_dec_msg.insert(tk.END,C)
    
def decode(): 
	img = ent_dec_name.get()
	image = Image.open(img, 'r') 
	
	data = '' 
	imgdata = iter(image.getdata()) 
	A=0
	while (True): 
		pixels = [value for value in imgdata.__next__()[:3] +
								imgdata.__next__()[:3] +
								imgdata.__next__()[:3]] 
		# string of binary data 
		binstr = '' 
		
		for i in pixels[:8]: 
			if (i % 2 == 0): 
				binstr += '0'
			else: 
				binstr += '1'
				
		data += chr(int(binstr, 2))
		if (pixels[-1] % 2 != 0): 
			return data 
            #ent_dec_msg.insert(tk.END,data) 	
     
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

lbl_dec_name = tk.Label(master=frm_input2, text="Enter image name for decode:")
ent_dec_name = tk.Entry(master=frm_input2, width=50)
lbl_dec_name.grid(row=5, column=1, sticky="e")
ent_dec_name.grid(row=5, column=2)

lbl_dec_msg = tk.Label(master=frm_input2, text="The decoded msg is:")
ent_dec_msg = tk.Entry(master=frm_input2, width=50)
lbl_dec_msg.grid(row=6, column=1, sticky="e")
ent_dec_msg.grid(row=6, column=2)


window.mainloop()