from __future__ import division, print_function, unicode_literals

import sys
import random
import argparse
import logging
from tkinter import *
from tkinter import filedialog
from datetime import datetime


from tkinter import messagebox
import os
import PIL
from PIL import Image
import math
from Crypto.Cipher import AES
import hashlib
import binascii
import numpy as np
import glob

global password
global file_path_e



def encrypt(imagename, password, savepath):
    plaintext = list()
    plaintextstr = ""

    im = Image.open(imagename)
    pix = im.load()

    width = im.size[0]
    height = im.size[1]

    # break up the image into a list, each with pixel values and then append to a string
    for y in range(0, height):
        for x in range(0, width):
            print(pix[x, y])
            plaintext.append(pix[x, y])
    print(width)
    print(height)

    # add 100 to each tuple value to make sure each are 3 digits long.
    for i in range(0, len(plaintext)):
        for j in range(0, 0):
            aa = int(plaintext[i][j]) + 100
            plaintextstr = plaintextstr + str(aa)

    # length save for encrypted image reconstruction
    relength = len(plaintext)

    # append dimensions of image for reconstruction after decryption
    plaintextstr += "h" + str(height) + "h" + "w" + str(width) + "w"

    # make sure that plantextstr length is a multiple of 16 for AES.  if not, append "n".
    while (len(plaintextstr) % 16 != 0):
        plaintextstr = plaintextstr + "n"

    # encrypt plaintext
    obj = AES.new(password, AES.MODE_CBC, 'This is an IV456')
    ciphertext = obj.encrypt(plaintextstr)

    # write ciphertext to file for analysis
    #cipher_name = imagename + ".crypt"
    #g = open(cipher_name, 'w')
    #g.write(ciphertext)
    construct_enc_image(ciphertext, relength, width, height, savepath, imagename)
    print("Visual Encryption done.......")
    level_one_encrypt("visual_encrypt.jpeg", savepath)
    print("2-Share Encryption done.......")

def load_image(name):
    return Image.open(name)
def construct_enc_image(ciphertext, relength, width, height, savepath, imagename):
    asciicipher = binascii.hexlify(ciphertext)

    def replace_all(text, dic):
        text = text.hex()
        for i, j in dic.items():
            text = text.replace(i, j)
        return text

    # use replace function to replace ascii cipher characters with numbers
    reps = {'a': '1', 'b': '2', 'c': '3', 'd': '4', 'e': '5', 'f': '6', 'g': '7', 'h': '8', 'i': '9', 'j': '10',
            'k': '11', 'l': '12', 'm': '13', 'n': '14', 'o': '15', 'p': '16', 'q': '17', 'r': '18', 's': '19',
            't': '20', 'u': '21', 'v': '22', 'w': '23', 'x': '24', 'y': '25', 'z': '26'}
    asciiciphertxt = replace_all(asciicipher, reps)

    # construct encrypted image
    step = 3
    encimageone = [asciiciphertxt[i:i + step] for i in range(0, len(asciiciphertxt), step)]
    # if the last pixel RGB value is less than 3-digits, add a digit a 1
    if int(encimageone[len(encimageone) - 1]) < 100:
        encimageone[len(encimageone) - 1] += "1"
        # check to see if we can divide the string into partitions of 3 digits.  if not, fill in with some garbage RGB values
    if len(encimageone) % 3 != 0:
        while (len(encimageone) % 3 != 0):
            encimageone.append("101")



    encim = Image.new("L", (int(width), int(height)))
    #encim.putdata(encimageone)
    src_fname, ext = os.path.splitext(imagename)  # split filename and extension
    # construct output filename, basename to remove input directory
    basename = os.path.splitext(os.path.basename(imagename))[0]
    encim.save(savepath + basename + '.jpg')

def level_one_encrypt(Imagename, savepath):
    message_image = load_image(Imagename)
    size = message_image.size
    width, height = size

    secret_image = generate_secret(size)
    secret_image.save("secret.jpeg")

    prepared_image = prepare_message_image(message_image, size)
    ciphered_image = generate_ciphered_image(secret_image, prepared_image)
    ciphered_image = ciphered_image.convert('RGB')
    now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    src_fname, ext = os.path.splitext(Imagename)  # split filename and extension
    # construct output filename, basename to remove input directory
    basename = os.path.splitext(os.path.basename(Imagename))[0]
    #im.save('/home/socialab/Desktop/untitled/Work/Images/Train_encrypted/' + now + '.jpg')
    ciphered_image.save(savepath + basename + '.jpg')
def generate_secret(size, secret_image=None):
    width, height = size
    new_secret_image = Image.new(mode="L", size=(width, height))

    for x in range(0,  width):
        for y in range(0, height):
            color1 = np.random.randint(255)

            new_secret_image.putpixel((x, y), (color1))


    return new_secret_image
def prepare_message_image(image, size):
    if size != image.size:
        image = image.resize(size, Image.ANTIALIAS)
    return image
def generate_ciphered_image(secret_image, prepared_image):
    width, height = prepared_image.size
    ciphered_image = Image.new(mode="L", size=(width, height))
    for x in range(0, width):
        for y in range(0, height):
            sec = secret_image.getpixel((x, y))
            msssg = prepared_image.getpixel((int(x / 2), int(y / 2)))
            color1 = (msssg + sec) % 256

            ciphered_image.putpixel((x, y), (color1))


    return ciphered_image


string = 's'
num = 0
for test in string:
    if num == 0:
        filepath = r'D:\New folder\PCA_FaceRecognition\att_faces\*'
        savepath = r'D:\New folder\PCA_FaceRecognition\BIT SLICE 1/'
    if num != 0:
        filepath = r'C:\Users\OEM\Desktop\chiru\colorferet\colorferet\dvd2\gray_feret_cd1\test\inp\*'
        savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Test_encrypted/'
    password = hashlib.sha256('2'.encode("UTF-8")).hexdigest()
    # password = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    if len(os.listdir(savepath)) != 100:
        folders = glob.glob(filepath)
        imagenames = []
        for folder in folders:
            i = 1
            for imagename in glob.glob(folder + '/*.jpg'):  # assuming jpg
                # print("Encrypting image...")
                #byte_array = Algorithm(imagename)
                src_fname, ext = os.path.splitext(imagename)  # split filename and extension
                # construct output filename, basename to remove input directory
                folderbasename = os.path.splitext(os.path.basename(folder))[0]
                basename = os.path.splitext(os.path.basename(imagename))[0]
                now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                #byte_array = byte_array
                # filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Train_encrypted/'
                file_path = os.path.join(savepath, folderbasename + "/")
                # file_path = string.join(savepath, "/")
                if i == 1:
                    os.makedirs(file_path)
                #cv2.imwrite(file_path + basename + '.jpg', byte_array)
                filename = imagename
                password = password[0:32]
                print(len(password))
                savepathh = file_path
                encrypt(filename, password,savepathh)
                i = 1+i
