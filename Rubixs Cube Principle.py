from random import randint
import numpy
import sys
from helper import *
import matplotlib.pyplot as plt #plot import
import matplotlib.colors  #color import
import numpy as np  #importing numpy
from PIL import Image #importing PIL to read all kind of images
#from PIL import ImageTk
import glob
import os
from datetime import datetime
string = 's'
num = 0
for test in string:
    if num == 0:
        filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\att_faces\*'
        savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\Rubixs Cube Principle/'
    if num != 0:
            filepath = r'C:\Users\OEM\Desktop\chiru\colorferet\colorferet\dvd2\gray_feret_cd1\test\inp\*'
            savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Rubixs Cube Principle\images\colorfet database\Test_encrypted/'
    #password = hashlib.sha256('2'.encode("UTF-8")).hexdigest()
    # password = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    if len(os.listdir(savepath)) == 0:
        folders = glob.glob(filepath)
        imagenames = []
        for folder in folders:
            iP = 1
            for face_images in glob.glob(folder + '/*.jpg'):  # assuming jpg
                im = Image.open(face_images)
                im = im.convert('RGB')
                pix = im.load()
                pixx = []
                # Obtaining the RGB matrices
                # Obtaining the RGB matrices
                r = []
                g = []
                b = []
                for i in range(im.size[0]):
                    r.append([])
                    g.append([])
                    b.append([])
                    for j in range(im.size[1]):
                        rgbPerPixel = pix[i, j]
                        r[i].append(rgbPerPixel[0])
                        g[i].append(rgbPerPixel[1])
                        b[i].append(rgbPerPixel[2])

                m = im.size[0]
                n = im.size[1]

                # Vectors Kr and Kc
                alpha = 8
                Kr = [randint(0, pow(2, alpha) - 1) for i in range(m)]
                Kc = [randint(0, pow(2, alpha) - 1) for i in range(n)]
                ITER_MAX = 1

                print('Vector Kr : ', Kr)
                print('Vector Kc : ', Kc)

                f = open('keys.txt', 'w+')
                f.write('Vector Kr : \n')
                for a in Kr:
                    f.write(str(a) + '\n')
                f.write('Vector Kc : \n')
                for a in Kc:
                    f.write(str(a) + '\n')
                f.write('ITER_MAX : \n')
                f.write(str(ITER_MAX) + '\n')

                for iterations in range(ITER_MAX):
                    # For each row
                    for i in range(m):
                        rTotalSum = sum(r[i])
                        gTotalSum = sum(g[i])
                        bTotalSum = sum(b[i])
                        rModulus = rTotalSum % 2
                        gModulus = gTotalSum % 2
                        bModulus = bTotalSum % 2
                        if (rModulus == 0):
                            r[i] = numpy.roll(r[i], Kr[i])
                        else:
                            r[i] = numpy.roll(r[i], -Kr[i])
                        if (gModulus == 0):
                            g[i] = numpy.roll(g[i], Kr[i])
                        else:
                            g[i] = numpy.roll(g[i], -Kr[i])
                        if (bModulus == 0):
                            b[i] = numpy.roll(b[i], Kr[i])
                        else:
                            b[i] = numpy.roll(b[i], -Kr[i])
                    # For each column
                    for i in range(n):
                        rTotalSum = 0
                        gTotalSum = 0
                        bTotalSum = 0
                        for j in range(m):
                            rTotalSum += r[j][i]
                            gTotalSum += g[j][i]
                            bTotalSum += b[j][i]
                        rModulus = rTotalSum % 2
                        gModulus = gTotalSum % 2
                        bModulus = bTotalSum % 2
                        if (rModulus == 0):
                            upshift(r, i, Kc[i])
                        else:
                            downshift(r, i, Kc[i])
                        if (gModulus == 0):
                            upshift(g, i, Kc[i])
                        else:
                            downshift(g, i, Kc[i])
                        if (bModulus == 0):
                            upshift(b, i, Kc[i])
                        else:
                            downshift(b, i, Kc[i])
                    # For each row
                    for i in range(m):
                        for j in range(n):
                            if (i % 2 == 1):
                                r[i][j] = r[i][j] ^ Kc[j]
                                g[i][j] = g[i][j] ^ Kc[j]
                                b[i][j] = b[i][j] ^ Kc[j]
                            else:
                                r[i][j] = r[i][j] ^ rotate180(Kc[j])
                                g[i][j] = g[i][j] ^ rotate180(Kc[j])
                                b[i][j] = b[i][j] ^ rotate180(Kc[j])
                    # For each column
                    for j in range(n):
                        for i in range(m):
                            if (j % 2 == 0):
                                r[i][j] = r[i][j] ^ Kr[i]
                                g[i][j] = g[i][j] ^ Kr[i]
                                b[i][j] = b[i][j] ^ Kr[i]
                            else:
                                r[i][j] = r[i][j] ^ rotate180(Kr[i])
                                g[i][j] = g[i][j] ^ rotate180(Kr[i])
                                b[i][j] = b[i][j] ^ rotate180(Kr[i])

                for i in range(m):
                    for j in range(n):
                        pix[i, j] = (r[i][j], g[i][j], b[i][j])

                src_fname, ext = os.path.splitext(face_images)  # split filename and extension
                # construct output filename, basename to remove input directory
                basename = os.path.splitext(os.path.basename(face_images))[0]
                now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                src_fname, ext = os.path.splitext(face_images)  # split filename and extension
                # construct output filename, basename to remove input directory
                folderbasename = os.path.splitext(os.path.basename(folder))[0]
                basename = os.path.splitext(os.path.basename(face_images))[0]
                now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                # byte_array = byte_array
                # filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Train_encrypted/'
                file_path = os.path.join(savepath, folderbasename + "/")
                # file_path = string.join(savepath, "/")
                if iP == 1:
                    os.makedirs(file_path)
                # cv2.imwrite(file_path + basename + '.jpg', byte_array)

                savepathh = file_path
                im.save(savepathh + basename + '.jpg')
                iP = 1 + iP

    num = num + 1


