import random
import numpy
from PIL import Image #importing PIL to read all kind of images
import glob
import os
from datetime import datetime
import cv2
string = 's'
num = 0
for test in string:
    if num == 0:
        filepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\att_faces\*'
        savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\PCA_FaceRecognition - Copy\RSA/'
    if num != 0:
        filepath = r'C:\Users\OEM\Desktop\chiru\colorferet\colorferet\dvd2\gray_feret_cd1\test\inp\*'
        savepath = r'C:\Users\OEM\Desktop\chiru\USBDrive\untitled\Work\Image-Encryption-using-Genetic-algorithm-and-Bit-Slice-and-Rotation-master\GA_Images\Test_encrypted/'
    #password = hashlib.sha256('2'.encode("UTF-8")).hexdigest()
    # password = hashlib.sha256(str(random.getrandbits(256)).encode('utf-8')).hexdigest()
    if len(os.listdir(savepath)) != 100:
        folders = glob.glob(filepath)
        imagenames = []
        for folder in folders:
            ip = 1
            for face_images in glob.glob(folder + '/*.jpg'):  # assuming jpg
                jpgfile = Image.open(face_images).convert('RGB')# jpgfile.show()

                #print(jpgfile.bits, jpgfile.size, jpgfile.format)
                row, col = jpgfile.size
                pixels = jpgfile.load()

                row1 = 1000003
                phi = [0 for x1 in range(row1)]
                occ = [0 for x1 in range(row1)]
                primes = []
                phi[1] = 1
                # phi[2] = 1
                # print (phi)
                for i in range(2, 1000001):
                    # print (i)
                    if (phi[i] == 0):
                        phi[i] = i - 1
                        # print (i)
                        primes.append(i)
                        # j = 2*i
                        for j in range(2 * i, 1000001, i):
                            # print("j ",j)
                            # print(j)
                            if (occ[j] == 0):
                                # print ("inside if2")
                                occ[j] = 1
                                phi[j] = j
                            # print (phi[j])
                            # print ((i-1)//i)
                            phi[j] = (phi[j] * (i - 1)) // i
                    # print(phi[j])
                    # j = j + i
                # print (primes)
                p = primes[random.randrange(1, 167)]
                q = primes[random.randrange(1, 167)]
                print(p, " ", q)
                n = p * q
                mod = n
                phin1 = phi[n]
                phin2 = phi[phin1]
                e = primes[random.randrange(1, 9000)]
                mod1 = phin1


                def power1(x, y, m):
                    ans = 1
                    while (y > 0):
                        if (y % 2 == 1):
                            ans = (ans * x) % m
                        y = y // 2
                        x = (x * x) % m
                    return ans


                d = power1(e, phin2 - 1, mod1)
                enc = [[0 for x in range(row)] for y in range(col)]
                dec = [[0 for x in range(row)] for y in range(col)]
                for i in range(col):
                    for j in range(row):
                        r, g, b = pixels[j, i]
                        r1 = power1(r + 10, e, mod)
                        g1 = power1(g + 10, e, mod)
                        b1 = power1(b + 10, e, mod)
                        enc[i][j] = [r1, g1, b1]
                print(pixels[row - 1, col - 1])
                img = numpy.array(enc, dtype=numpy.uint8)
                img1 = Image.fromarray(img, "RGB")
                # pixels2 = img1.load()

                # pixels2 = img1.load()
                # img1.show()
                imagename = face_images
                src_fname, ext = os.path.splitext(imagename)  # split filename and extension
                # construct output filename, basename to remove input directory
                basename = os.path.splitext(os.path.basename(imagename))[0]
                now = datetime.now().strftime('%Y%m%d-%H%M%S-%f')
                src_fname, ext = os.path.splitext(imagename)  # split filename and extension
                folderbasename = os.path.splitext(os.path.basename(folder))[0]
                basename = os.path.splitext(os.path.basename(imagename))[0]
                file_path = os.path.join(savepath, folderbasename + "/")
                if ip == 1:
                    os.makedirs(file_path)
                savepathh = file_path
                img1 = img1.convert('L')
                img1.save(savepathh + basename + '.jpg')
                #cv2.imwrite(savepathh + basename + '.jpg', img1)
                for i in range(col):
                    for j in range(row):
                        r, g, b = enc[i][j]
                        r1 = power1(r, d, mod) - 10
                        g1 = power1(g, d, mod) - 10
                        b1 = power1(b, d, mod) - 10
                        dec[i][j] = [r1, g1, b1]
                img2 = numpy.array(dec, dtype=numpy.uint8)
                img3 = Image.fromarray(img2, "RGB")
                #img3.show()
                img3.save('out.bmp')
                j = Image.open("out.bmp")
                img = j.save("out.jpeg")

                p = j.load()
                print(p[row - 1, col - 1])
                ip = ip+1

    num = num+1
