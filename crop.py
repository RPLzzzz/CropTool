# -*- coding: utf-8 -*-
"""
@author: Loïc ARGENTIER
"""

import argparse
import os
import matplotlib.image as mpimg
import numpy as np

class Image:
    """ This class contain all tools to crop images """    
    def __init__(self):
        self.pixel_max=1.0
        self.path_output=args.output
        if args.path==None:
            self.path = os.path.dirname(os.path.realpath(__file__)) #Current folder
        else:
            self.path = args.path
    
    def _imread(self,file):
        img = mpimg.imread(file)
        self.pixel_max=np.max(img)
        return img/self.pixel_max
    
    def _imsave(self,file,img):
        mpimg.imsave(file, img)
    
    def _crop(self, img):
        nb_raw,nb_col,nb_can = np.shape(img)
        col_min=1e9
        col_max=-1
        raw_min=1e9
        raw_max=-1
        for k in range(nb_raw):
            for j in range(nb_col):
                if (img[k,j,0] != 1.0 and j<col_min):
                    col_min=j
                    break
            for j in range(nb_col-1,0,-1):
                if (img[k,j,0] != 1.0 and j>col_max):
                    col_max=j
                    break
        for j in range(nb_col):
            for k in range(nb_raw):
                if (img[k,j,0] != 1.0 and k<raw_min):
                    raw_min=k
                    break
            for k in range(nb_raw-1,0,-1):
                if (img[k,j,0] != 1.0 and k>raw_max):
                    raw_max=k
                    break
        return img[raw_min:raw_max,col_min:col_max,:]

    def _iter(self):
        for file in os.listdir(self.path):
            if file[-3::] != '.py':
                img=self._imread(self.path+"/"+file)
                img=self._crop(img)
                if self.path_output==None:
                    self._imsave(self.path+"/"+file,img)
                else :
                    if os.path.exists(self.path_output):
                        self._imsave(self.path_output+"/"+file,img)
                    else:
                        os.makedirs(self.path_output)
                        self._imsave(self.path_output+"/"+file,img)
                print(file+ ' ... Done')
            
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="Tools to crop plot\'s images produced on Matlab, Python, etc, containing in a folder. The current Folder is taken by default",
        epilog="Pouet")
    parser.add_argument("-p", "--path", help="Path of the input folder containing images to crop")
    parser.add_argument("-o", "--output", help="Path of the output folder will contain images croped")
    args = parser.parse_args()
    
    tool=Image()
    tool._iter()



