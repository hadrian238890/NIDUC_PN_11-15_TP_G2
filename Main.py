import scipy.misc
import numpy
from commpy.channelcoding import turbo


from TransmissionChannel import TransmissionChannel
from Coder import Coder
from Receiver import Receiver
import matplotlib.pyplot as plt
from PIL import Image
import imageio
import random




def open_image(filename):
    image = Image.open(filename)
    image.load()
    image = numpy.array(image)
    return image


def openImageio(filename):
    image = imageio.imread(filename)
    return image


kanal = TransmissionChannel()
koder = Coder()
odbiornik = Receiver()


random.seed(420)
file_name = 'zdjecie.jpg'
myImg = open_image(file_name)

plt.figure('Wroclaw Image')
plt.imshow(myImg)
plt.show()

myImgBSC = kanal.pass_bsc(myImg)
plt.figure('Binary Symmetric Channel')
plt.imshow(myImgBSC)
plt.show()

myImgGilbert = kanal.pass_gilbert(myImg)
plt.figure('Model Gilberta')
plt.imshow(myImgGilbert)
plt.show()

tmr_image = koder.encode_tmr(myImg)
tmr_bsc_image = kanal.pass_bsc(tmr_image)
myImgTMRBSCdec = odbiornik.decode_tmr(tmr_bsc_image, myImg.shape)
plt.figure('BSC po zastosowaniu potrojnej redundancji')
plt.imshow(myImgTMRBSCdec)
plt.show()

"""
myTurbo = turbo.turbo_encode(myImg)
myTurboBSC = kanal.pass_bsc(myImgTMR[0])
myTurboBSCdec = turbo.turbo_decode(myTurboBSC)
plt.figure('Turbo kod')
plt.imshow(myTurboBSCdec)
plt.show()
"""

rs_image = koder.encode_reed_salomon(myImg)
rs_bsc_image = kanal.pass_bsc(rs_image)
rs_image_decoded = odbiornik.decode_reed_salomon(rs_bsc_image, myImg.shape)
plt.figure('BSC po zastosowaniu kodu Reeda Salomona')
plt.imshow(rs_image_decoded)
plt.show()

rs_image = koder.encode_reed_salomon(myImg)
rs_gilbert_image = kanal.pass_gilbert(rs_image)
rs_image_decoded = odbiornik.decode_reed_salomon(rs_gilbert_image, myImg.shape)
plt.figure('Model Gilberta po zastosowaniu kodu Reeda Salomona')
plt.imshow(rs_image_decoded)
plt.show()


tmr_gilbert_image = kanal.pass_gilbert(tmr_image)
myImgTMRGilbertdec = odbiornik.decode_tmr(tmr_gilbert_image, myImg.shape)
plt.figure('Model Gilberta po zastosowaniu potrojnej redundancji')
plt.imshow(myImgTMRGilbertdec)
plt.show()


hamming_img = koder.encode_hamming_code(myImg)
hamming_bsc_image = kanal.pass_bsc(hamming_img)
hamming_img_decoded = odbiornik.decode_hamming_code(hamming_bsc_image, myImg.shape)
plt.figure('Binary Symmetric Channel po zastosowaniu kodu Hamminga')
plt.imshow(hamming_img_decoded)
plt.show()


hamming_gilbert_image= kanal.pass_gilbert(hamming_img)
hamming__gilbert_img_decoded = odbiornik.decode_hamming_code(hamming_gilbert_image, myImg.shape)
plt.figure('Model Gilberta po zastosowaniu kodu Hamminga')
plt.imshow(hamming__gilbert_img_decoded)
plt.show()

hamming_img = koder.encode_hamming_code(myImg)
hamming_img_interleaved = kanal.pass_interleave(hamming_img)
hamming_gilbert_img_interleaved = kanal.pass_gilbert(hamming_img_interleaved)
hamming_gilbert_img_interleavedx2 = kanal.pass_interleave(hamming_gilbert_img_interleaved)
hamming_gilbert_img_interleavedx2_decoded = odbiornik.decode_hamming_code(hamming_gilbert_img_interleavedx2, myImg.shape)
plt.figure('Model Gilberta po zastosowaniu przeplotu i kodu Hamminga')
plt.imshow(hamming_gilbert_img_interleavedx2_decoded)
plt.show()









