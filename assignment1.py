import nibabel as nib
import os
import matplotlib.pyplot as plt
import pylab
import threading
import time
import random
import cv2
from PIL import Image
import numpy as np
from pynput import keyboard,mouse
from matplotlib.widgets import Button
from pynput.mouse import Controller, Listener

path = 'D:\Desktop\CS516\Assignment1\images'
docs = ('\\t1.nii','\\t2.nii','\\tof.nii','\swi.nii','\\bold.nii')
style = "PuRd_r"
slice_id = 60
view = "axial"
color = ('Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat')
size = (0,0,0)
event_count = 0

def viewer(brain,slice,view):
    """ Function to show the slice from 3d image (part 1)"""
    # For test use
    # time.sleep(0.5)
    fig = plt.figure("Assignment1")
    plt.title("Slice = "+ str(slice)+"\nView = "+ view)
    if "axial" == view:
        plt.imshow(brain[:,slice,:],cmap=style)
    elif "sagittal" == view:
        plt.imshow(brain[slice,:,:],cmap=style)
    elif "coronal" == view:
        plt.imshow(brain[:,:,slice],cmap=style)
    # Interactive mode
    plt.ion()
    plt.pause(0.1)
    plt.show()

def viewer2(brain,slice,view):
    """ Function to show the simple 2d FFT (part 2a)"""
    fig = plt.figure("Assignment1")
    plt.subplot(1,2,1)
    plt.imshow(brain[:,slice,:])
    plt.title("Slice = "+ str(slice)+"\nView = "+ view)
    plt.subplot(1,2,2)
    plt.imshow(my_fft(brain[:,slice,:]))
    plt.title("requence domain of raw")
    # Interactive mode
    plt.ion()
    plt.pause(0.1)
    plt.show()

def viewer3(brain,slice,view):
    """ Function to show the gaussian filter (part 2b)"""
    raw = brain[:,slice,:]
    filter(my_fft(raw),raw)

def viewer4(brain,slice,view):
    """ Function to show all plots (part 2c)"""
    fig = plt.figure("Assignment1")
    base = brain[:,slice,:]
    base_fft = my_fft(base)
    plt.subplot(2,2,1)
    plt.imshow(base)
    plt.title("raw image")
    plt.subplot(2,2,2)
    plt.imshow(base_fft)
    plt.title("2d fft")
    plt.subplot(2,2,3)
    # edge = cv2.Canny(img,100,200)
    img = filter2(base)
    plt.imshow(img)
    plt.title("edge detection")
    plt.subplot(2,2,4)
    plt.imshow(filter3(base_fft,base))
    plt.title("smooth")
    plt.subplots_adjust(wspace=0.5,hspace=0.5)
     # Interactive mode
    plt.ion()
    plt.pause(0.1)
    plt.show()

def viewer5(brain,slice,view):
    """ Function to show all views (part 1a bonus)"""
    fig = plt.figure("Assignment1")
    plt.title("Slice = "+ str(slice)+"\nView = "+ view)
    plt.subplot(2,2,1)
    plt.imshow(brain[:,slice,:],cmap=style)
    plt.title("axial view")
    plt.subplot(2,2,2)
    plt.imshow(brain[slice,:,:],cmap=style)
    plt.title("sagittal view")
    plt.subplot(2,2,3)
    plt.imshow(brain[:,:,slice],cmap=style)
    plt.title("coronal view")
    plt.subplots_adjust(wspace=0.2,hspace=0.2)
    # Interactive mode
    plt.ion()
    plt.pause(0.1)
    plt.show()

def my_fft(img):
    """ Function to figure out 2d fft"""
    fft = np.fft.fft2(img)
    center = np.fft.fftshift(fft)
    return np.log(1+np.abs(center))

def filter(rotim,raw):
    """gaussian filter"""
    sz_x = rotim.shape[0]
    sz_y = rotim.shape[1]
    [X, Y] = np.mgrid[0:sz_x, 0:sz_y]
    xpr = X - int(sz_x) // 2
    ypr = Y - int(sz_y) // 2
    count=1
    for sigma in range(1,25,5):
        gaussfilt = np.exp(-((xpr**2+ypr**2)/(2*sigma**2)))/(2*np.pi*sigma**2)
        fft_img = np.fft.fft2(raw)
        fft_shift = np.fft.fftshift(fft_img)
        # fft_g = np.fft.fft2(gaussfilt)
        # fft_shift_g = np.fft.fftshift(fft_g)
        fft_multiple = fft_shift*gaussfilt
        ifft_shift = np.fft.ifftshift(fft_multiple)
        ifft = np.fft.ifft2(ifft_shift)

        log_ifft = np.log(1+np.abs(ifft))
        plt.subplot(1,5,count)
        plt.imshow(gaussfilt)
        plt.title('sigma='+str(sigma))
        plt.ion()
        plt.pause(0.01)
        plt.show()
        count =count + 1

def filter2(image):
    """ edge detection: prewitt operator (3*3 domain) """
    img = Image.fromarray(image).convert("L")
    img_array = np.array(img)
    x,y = img_array.shape
    print(x)
    print(y)
    img_result = np.zeros((x-1,y-1))
    for i in range(1, x-1):
        for j in range(1, y-1):
            Dx = img_array[i + 1][j - 1] + 2 * img_array[i + 1][j] + img_array[i + 1][j + 1] - img_array[i - 1][j - 1] - 2 * img_array[i - 1][j] - img_array[i - 1][j + 1]
            Dy = img_array[i - 1][j + 1] + 2 * img_array[i][j + 1] + img_array[i + 1][j + 1] - img_array[i - 1][j - 1] - 2 * img_array[i][j - 1] - img_array[i + 1][j - 1]
            img_result[i][j] = (Dx * Dx + Dy * Dy) ** 0.5
    return img_result

def filter3(rotim,raw):
    """smooth with gaussian filter"""
    sz_x = rotim.shape[0]
    sz_y = rotim.shape[1]
    [X, Y] = np.mgrid[0:sz_x, 0:sz_y]
    xpr = X - int(sz_x) // 2
    ypr = Y - int(sz_y) // 2
    sigma = 25
    gaussfilt = np.exp(-((xpr**2+ypr**2)/(2*sigma**2)))/(2*np.pi*sigma**2)
    fft = np.fft.fft2(raw)
    fft_shift = np.fft.fftshift(fft)
    ishift = np.fft.ifftshift(fft_shift*gaussfilt)
    ifft = np.fft.ifft2(ishift)
    return np.log(1+np.abs(ifft))

def on_release(key):
    """ Function to listen on mouse scroll"""
    global slice_id, brain
    if key == keyboard.Key.up:
        print("up")
        slice_id = slice_id+1
        viewer(brain,slice_id,"axial")
    if key == keyboard.Key.down:
        print("down")
        slice_id = slice_id+1
        viewer(brain,slice_id,"axial")

def on_scroll(x,y,dx,dy):
    """ Function to listen on mouse scroll"""
    global size, view, brain, slice_id
    slice_id = slice_id + dy
    if slice_id > size[2]-1:
        slice_id = 0
    if slice_id < 0:
        slice_id = size[2]-1
    #change the function here for different part of assignment
    viewer4(brain,slice_id,view)
    # print("Thread id==>%s, Thread num==> %d\n"%(threading.current_thread().name,threading.activeCount()))

# def button_change_color():
#     btnaxe = plt.axes([0.8,0.05,0.1,0.1])
#     btn = Button(btnaxe,'change')
#     btn.on_clicked(change_color)
#
# def change_color():
#     global view
#     i = random.randint(0,99)
#     style = color[i]
#     viewer(brain,slice_id,view)


def listener():
    with Listener(on_scroll = on_scroll) as listener:
        listener.join()
    # with Listener(on_release=on_release) as listener:
    #     listener.join()

if __name__ == '__main__':
    mouse = Controller
    data = nib.load(path+docs[4])
    brain = data.get_fdata()
    size = brain.shape
    # viewer2(brain,slice_id,view)
    listener()


# For test use
# for i in range(50):
#     viewer2(brain,slice_id+i,1)
#     print(slice_id+i)
