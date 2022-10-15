import tkinter as tk
from tkinter import ttk
from tkinter import filedialog as fd
from tkinter import messagebox

import cv2
import numpy
from PIL import Image,ImageTk
from math import log10, sqrt

g_val="53710246"


def get_binary(data):
    # list of binary codes
    # of given data
    newd = []

    for i in data:
        newd.append(format(ord(i), '08b'))
    return newd

def get_key(data):
    ln=len(data)
    new_val=g_val
    for i in range(16):
        i_i=i%ln
        fi=ord(data[i_i])%8
        f_si=ord(data[i_i])%ln
        f_si=ln-f_si
        if(f_si==ln):
            f_si=f_si-1
        si=ord(data[f_si])%8
        if(si<fi):
            temp=si
            si=fi
            fi=temp

        if (si == fi):
            if (si == 0):
                si = 1
            elif (si == 7):
                fi = 6
            else:
                fi = si - 1

        beg=new_val[0:fi]
        mid=new_val[fi+1:si]
        end=new_val[si+1:]
        new_val=beg+new_val[si]+mid+new_val[fi]+end

    return new_val


def getPix(pix, data,key_data):

    bin_data = get_binary(data)
    len_data = len(bin_data)
    img_data = iter(pix)

    print(key_data)
    new_key=get_key(key_data)
    print(new_key)

    for i in range(len_data):

        new_key=new_key[1:]+new_key[:1]

        # Extracting 3 pixels at a time
        arr=[value for value in img_data.__next__()[:3] +
                                img_data.__next__()[:3] +
                                img_data.__next__()[:3]]

        # Pixel value should be made
        # odd for 1 and even for 0
        for j in range(0, 8):
            if (bin_data[i][j] == '0' and arr[ord(new_key[j])-48]% 2 != 0):
                arr[ord(new_key[j])-48] -= 1

            elif (bin_data[i][j] == '1' and arr[ord(new_key[j])-48] % 2 == 0):
                if(arr[ord(new_key[j])-48] != 0):
                    arr[ord(new_key[j])-48] -= 1
                else:
                    arr[ord(new_key[j])-48] += 1

        # Eighth pixel of every set tells
        # whether to stop or to read further.
        # 0 means keep reading; 1 means the
        # message is over.
        if (i == len_data - 1):
            if (arr[-1] % 2 == 0):
                if(arr[-1] != 0):
                    arr[-1] -= 1
                else:
                    arr[-1] += 1

        else:
            if (arr[-1] % 2 != 0):
                arr[-1] -= 1

        arr = tuple(arr)
        yield arr[0:3]
        yield arr[3:6]
        yield arr[6:9]

def encode(image, data,key_data):
    w = image.size[0]
    (x, y) = (0, 0)

    for pixel in getPix(image.getdata(), data,key_data):

        # Putting modified pixels in the new image
        image.putpixel((x, y), pixel)
        if (x == w - 1):
            x = 0
            y += 1
        else:
            x += 1
    return image


def decode(stego_img,key_data):
    data = ''
    imgdata = iter(stego_img.getdata())
    print(key_data)
    new_key = get_key(key_data)
    print(new_key)
    while (True):

        new_key = new_key[1:] + new_key[:1]
        pixels = [value for value in imgdata.__next__()[:3] +
                  imgdata.__next__()[:3] +
                  imgdata.__next__()[:3]]

        # string of binary data
        binstr = ''

        for i in range(0, 8):
            if (pixels[ord(new_key[i]) - 48] % 2 == 0):
                binstr += '0'
            else:
                binstr += '1'

        data += chr(int(binstr, 2))
        if (pixels[-1] % 2 != 0):
            return data



root = tk.Tk()
root.title('Image Steganography')
root.resizable(False, False)
root.geometry('400x450')
frame=tk.Frame(master=root, relief=tk.RAISED)

v=tk.IntVar()
#v.set(1)

def save_img(pil_im):
    filetypes = [
        ('image(png)', '*.png')
    ]
    filename = fd.asksaveasfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes
    )
    if(filename.endswith(".png")):
        pil_im.save(filename)
    else:
        pil_im.save(filename+".png")
    #cv2.imwrite(filename, oc_im)

def convert(img_path,msg_bx,key,frame_2):
    cov_img = Image.open(img_path)
    val=(cov_img.size[0]*cov_img.size[1]*3)//9
    val=val-5
    print(len(msg_bx.get("1.0",tk.END)))
    if(len(msg_bx.get("1.0",tk.END))>val):
        if(frame_2.winfo_exists()):
            frame_2.destroy()
        messagebox.showerror("Error","Message Length is more than the image can hide")
        return

    if (len(key.get())==0):
        if (frame_2.winfo_exists()):
            frame_2.destroy()
        messagebox.showerror("Error","Enter Key")
        return

    stego_img=encode(cov_img,msg_bx.get("1.0",tk.END),key.get())
    oc_img = numpy.array(stego_img)
    oc_im = cv2.cvtColor(oc_img, cv2.COLOR_RGB2BGR)
    #cv2.imshow("Stego_img",oc_im)
    #stego_img.show(title="Stego_Img")
    tk_img = stego_img.resize((150, 100))
    tk_img=ImageTk.PhotoImage(tk_img)

    frame_3 = tk.Frame(master=frame_2, relief=tk.RAISED)
    label1 = tk.Label(master=frame_3,image=tk_img)
    label1.image = tk_img
    save_btn = tk.Button(master=frame_3, text="Save", width=15,height=2,command=lambda: save_img(stego_img))
    frame_3.grid(row=3, column=0,padx=5,pady=5,columnspan=2)
    label1.grid(row=0, column=0,padx=5,pady=5)
    save_btn.grid(row=0,column=1,padx=5,pady=5)


def get_msg(stego_img,frame_2,key_box):

    if (len(key_box.get())==0):
        if (frame_2.winfo_exists()):
            frame_2.destroy()
        messagebox.showerror("Error","Enter Key")
        return

    msg=decode(stego_img,key_box.get())
    frame_3 = tk.Frame(master=frame_2, relief=tk.RAISED)
    #label1 = tk.Label(master=frame_3,text=msg,wraplength=300,justify=tk.LEFT,font=8)
    cnvs=tk.Canvas(master=frame_3,width=350,height=200)
    cnvs.pack(side=tk.LEFT,padx=5,pady=5)
    v = tk.Scrollbar(frame_3, orient='vertical',command=cnvs.yview)
    v.pack(side=tk.RIGHT, fill='y')
    cnvs.configure(yscrollcommand=v.set)
    cnvs.bind('<Configure>',lambda e:cnvs.configure(scrollregion=cnvs.bbox("all")))
    cnvs.create_text(10,10,text=msg,fill="black",width=300,justify=tk.LEFT)
    frame_3.grid(row=3,column=0,columnspan=2,padx=5,pady=5)
    #label1.grid(row=0,column=0,padx=5,pady=5)


def create_widget(frame_2,img_path):
    msg_box = tk.Text(master=frame_2,width=22,height=8)
    msg_box.insert("1.0", "Enter your message here")
    lb_bx=tk.Label(master=frame_2,text="Key :")
    key_bx = tk.Entry(master=frame_2,width=15)
    btn_box=tk.Button(master=frame_2,text="Stego",width=15,height=2,command=lambda: convert(img_path,msg_box,key_bx,frame_2) )

    return msg_box,lb_bx,key_bx,btn_box

def select_file(frame_2):

    if (frame_2.winfo_exists()):
        frame_2.grid_remove()
        frame_2.destroy()

    filetypes = (
        ('image(jpg)', '*.jpg'),
        ('image(png)', '*.png')
    )

    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)

    frame_2 = tk.Frame(master=frame, relief=tk.RAISED)
    frame_2.grid(row=1,column=0,padx=5,pady=5,columnspan=2)
    msg_box,lb_box,key_box,btn_box= create_widget(frame_2,filename)

    if (filename.endswith(".jpg")):
        print(filename)
        msg_box.grid(row=0,column=0,rowspan=3,padx=5,pady=5)
        lb_box.grid(row=0,column=1)
        key_box.grid(row=1,column=1,padx=5,pady=5)
        btn_box.grid(row=2,column=1,padx=5,pady=5)
    else:
        print("BAD")

        if (msg_box.winfo_exists()):
            msg_box.destroy()

        if (lb_box.winfo_exists()):
            lb_box.destroy()

        if (key_box.winfo_exists()):
            key_box.destroy()

        if(btn_box.winfo_exists()):
            btn_box.destroy()
        frame_2.grid_forget()


def select_retrive_file(frame_2):
    filetypes = [
        ('image(png)', '*.png')
    ]
    filename = fd.askopenfilename(
        title='Open a file',
        initialdir='/',
        filetypes=filetypes)
    if (frame_2.winfo_exists()):
        frame_2.destroy()
    frame_2 = tk.Frame(master=frame, relief=tk.RAISED)
    frame_2.grid(row=1,column=0,padx=5,pady=5,columnspan=2)
    stego_img = Image.open(filename)
    tk_img = stego_img.resize((150, 100))
    tk_img = ImageTk.PhotoImage(tk_img)

    label1 = tk.Label(master=frame_2, image=tk_img)
    label1.image = tk_img
    lb_bx = tk.Label(master=frame_2, text="Key :")
    key_box = tk.Entry(master=frame_2,width=15)
    extract_btn = tk.Button(master=frame_2, text="Extract",width=15,
                            height=2, command=lambda: get_msg(stego_img,frame_2,key_box))
    label1.grid(row=0, column=0,rowspan=3,padx=5,pady=5)
    lb_bx.grid(row=0, column=1)
    key_box.grid(row=1,column=1,padx=5,pady=5)
    extract_btn.grid(row=2, column=1,padx=5,pady=5)



def create_stego():
    frame_2 = tk.Frame(master=frame, relief=tk.RAISED)
    open_button = ttk.Button(
        frame,
        width=15,
        text='Open a File',
        command=lambda : select_file(frame_2)
    )

    open_button.grid(row=0,column=1,padx=5,pady=5)


def retrive_stego():
    frame_2=tk.Frame(master=frame, relief=tk.RAISED)
    open_button = ttk.Button(
        frame,
        width=15,
        text='Open a File',
        command=lambda: select_retrive_file(frame_2)
    )

    open_button.grid(row=0, column=1,padx=5,pady=5)

def show_frame():
    x=v.get()
    print(x)
    global frame
    if(x==1):
        if (frame.winfo_exists()):
            frame.destroy()
        frame= tk.Frame(master=root, relief=tk.RAISED)
        label = tk.Label(master=frame, text="Select Image",width=15)
        label.grid(row=0,column=0,padx=5, pady=5)
        frame.grid(row=1,column=0,padx=5,pady=5,columnspan=2)
        create_stego()
    else:
        if (frame.winfo_exists()):
            frame.destroy()
        frame = tk.Frame(master=root, relief=tk.RAISED)
        label = tk.Label(master=frame, text="Select Image",width=15)
        label.grid(row=0,column=0,padx=5, pady=5)
        frame.grid(row=1,column=0,padx=5,pady=5,columnspan=2)
        retrive_stego()


if __name__ == '__main__':

    rd1=tk.Radiobutton(root,
                   text="Hide Message",
                   padx=20,
                    width=15,
                    height=2,
                   value=1,
                   variable=v,
                       command=show_frame)

    rd2=tk.Radiobutton(root,
                   text="Retrieve Message",
                   padx=20,
                    width=15,
                    height=2,
                   value=2,
                   variable=v,
                       command=show_frame)

    rd1.grid(row=0,column=0,padx=5,pady=5)
    rd2.grid(row=0,column=1,padx=5,pady=5)
    #rd1.bind('<Button-1>',show_frame)
    #rd2.bind('<Button-1>', show_frame)

    root.mainloop()