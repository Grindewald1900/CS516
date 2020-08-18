import ants
import nibabel as nib
import matplotlib.pyplot as plt
import os

base_path = '/home/yee/Documents/CS516/A2'
path1 = base_path + '/t1.nii';
path2 = base_path + '/tof.nii';
path3 = base_path + '/tof_t1.nii.gz'
style = 'Greens'


def fsl(img_fix, img_move, slice, path):
    """ Registration with FLIRT(part 5)

        Arguments
        ---------
        img_fix: the image to be registered.
        img_move: the image need to register.
        slice: the number of slice to be shown
        path: the absolute path of resources(t1.nii & tof.nii)
    """
    os.chdir(path)
    print("FSL running...")
    # print("Voxel size:")
    # print(img_fix.header.get_zooms())  
    # print(img_move.header.get_zooms())
    img_fix.header.set_zooms((0.6, 0.6, 0.6))
    img_move.header.set_zooms((0.6, 0.6, 0.6)) # Reset the voxel size
    # print("Changed voxel size:")
    # print(img_fix.header.get_zooms())
    # print(img_move.header.get_zooms())

    os.system("flirt -in tof.nii -ref t1.nii -out tof_t1.nii -omat matrix.mat")

    data1 = img_fix.get_fdata()
    data2 = img_move.get_fdata()
    data3 = nib.load(path+'/tof_t1.nii.gz').get_fdata()

    pf = data1[slice, :, :]
    pm = data2[slice, :, :]
    p3 = data3[slice, :, :]

    plt.figure("Slice = " + str(slice))
    plt.subplot(2, 2, 1); plt.imshow(pf); plt.title('t1')
    plt.subplot(2, 2, 2); plt.imshow(pm); plt.title('tof')
    plt.subplot(2, 2, 3); plt.imshow(p3+pf); plt.title('FSL')
    plt.subplots_adjust(wspace=0.5, hspace=0.5)
    plt.show()


if __name__ == '__main__':
    fsl(nib.load(path1), nib.load(path2), 120, base_path)


