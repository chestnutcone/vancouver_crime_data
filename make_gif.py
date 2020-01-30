# -*- coding: utf-8 -*-
"""
Created on Wed Jan 29 00:38:10 2020

@author: Oliver
"""

import glob
from PIL import Image
import os

# filepaths
fp_in = r"C:\Users\Oliver\Desktop\Python Projects\vancouver_crime_data\crime_points\scatter_all"
fp_out = r"C:\Users\Oliver\Desktop\Python Projects\vancouver_crime_data\crime_points\scatter_crime_gif.gif"


files = sorted(os.listdir(fp_in), key=lambda x: int(x.split(".")[0]))
img, *imgs = [Image.open(os.path.join(fp_in,f)) for f in files]
img.save(fp=fp_out, format='GIF', append_images=imgs, save_all=True,
         duration=200, loop=0)