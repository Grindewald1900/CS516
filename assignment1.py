import nibabel as nib
import os
import matplotlib.pyplot as plt
import pylab
import threading
import time
import random
from pynput import keyboard,mouse
from matplotlib.widgets import Button
from pynput.mouse import Controller, Listener



path = 'D:\Desktop\CS516\Assignment1\images'
docs = ('\\t1.nii','\\t2.nii','\\tof.nii','\swi.nii','\\bold.nii')
style = "Greens"
slice_id = 60
view = "axial"
color = ('Accent', 'Accent_r', 'Blues', 'Blues_r', 'BrBG', 'BrBG_r', 'BuGn', 'BuGn_r', 'BuPu', 'BuPu_r', 'CMRmap', 'CMRmap_r', 'Dark2', 'Dark2_r', 'GnBu', 'GnBu_r', 'Greens', 'Greens_r', 'Greys', 'Greys_r', 'OrRd', 'OrRd_r', 'Oranges', 'Oranges_r', 'PRGn', 'PRGn_r', 'Paired', 'Paired_r', 'Pastel1', 'Pastel1_r', 'Pastel2', 'Pastel2_r', 'PiYG', 'PiYG_r', 'PuBu', 'PuBuGn', 'PuBuGn_r', 'PuBu_r', 'PuOr', 'PuOr_r', 'PuRd', 'PuRd_r', 'Purples', 'Purples_r', 'RdBu', 'RdBu_r', 'RdGy', 'RdGy_r', 'RdPu', 'RdPu_r', 'RdYlBu', 'RdYlBu_r', 'RdYlGn', 'RdYlGn_r', 'Reds', 'Reds_r', 'Set1', 'Set1_r', 'Set2', 'Set2_r', 'Set3', 'Set3_r', 'Spectral', 'Spectral_r', 'Wistia', 'Wistia_r', 'YlGn', 'YlGnBu', 'YlGnBu_r', 'YlGn_r', 'YlOrBr', 'YlOrBr_r', 'YlOrRd', 'YlOrRd_r', 'afmhot', 'afmhot_r', 'autumn', 'autumn_r', 'binary', 'binary_r', 'bone', 'bone_r', 'brg', 'brg_r', 'bwr', 'bwr_r', 'cividis', 'cividis_r', 'cool', 'cool_r', 'coolwarm', 'coolwarm_r', 'copper', 'copper_r', 'cubehelix', 'flag', 'flag_r', 'gist_earth', 'gist_earth_r', 'gist_gray', 'gist_gray_r', 'gist_heat')
size = (0,0,0)
event_count = 0

def viewer(brain,slice,view):
    """ Function to show the slice from 3d image"""
    # For test use
    # time.sleep(0.5)
    fig = plt.figure("Assignment1")
    plt.title("Slice = "+ str(slice)+"\nView = "+ view)
    if "axial" == view:
        plt.imshow(brain[:,:,slice],cmap=style)
    elif "sagittal" == view:
        plt.imshow(brain[slice,:,:],cmap=style)
    elif "coronal" == view:
        plt.imshow(brain[:,slice,:],cmap=style)
    # Interactive mode
    plt.ion()
    plt.pause(0.1)
    plt.show()

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
    viewer(brain,slice_id,view)
    # print("Thread id==>%s, Thread num==> %d\n"%(threading.current_thread().name,threading.activeCount()))

def button_change_color():
    btnaxe = plt.axes([0.8,0.05,0.1,0.1])
    btn = Button(btnaxe,'change')
    btn.on_clicked(change_color)

def change_color():
    global view
    i = random.randint(0,99)
    style = color[i]
    viewer(brain,slice_id,view)


def listener():
    with Listener(on_scroll = on_scroll) as listener:
        listener.join()
    # with Listener(on_release=on_release) as listener:
    #     listener.join()
mouse = Controller
data = nib.load(path+docs[0])
brain = data.get_fdata()
size = brain.shape
listener()
# mouse.scroll(0,1)

# For test use
# for i in range(50):
#     viewer2(brain,slice_id+i,1)
#     print(slice_id+i)





