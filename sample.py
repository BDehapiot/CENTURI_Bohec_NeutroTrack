#%% Imports

import numpy as np
from skimage import io 
from pathlib import Path

#%% Parameters

patch_number = 100 # number of random cropped images 
patch_size = 128 # size of random cropped images 
seed = 1 # seed for random indexes

#%% Open raw data

data = []
for path in Path('data', 'raw').iterdir():   
    raw = io.imread(path)   
    data.append((raw, raw.shape, path))

#%% Generate random patches

# Fix random outputs
np.random.seed(seed)

# Generate random indexes (M = movie, T = time)
randM = np.random.randint(0, len(data), size=patch_number)
randT = np.zeros_like(randM)
randY = np.zeros_like(randM)
randX = np.zeros_like(randM)

for i in range(randM.shape[0]):
    
    randT[i] = np.random.randint(0, data[randM[i]][0].shape[0])   
    
    if data[randM[i]][0].shape[1] > patch_size:        
        randY[i] = np.random.randint(0, data[randM[i]][0].shape[1]-patch_size)        
    else:
        randY[i] = 0
        
    if data[randM[i]][0].shape[2] > patch_size:
        randX[i] = np.random.randint(0, data[randM[i]][0].shape[2]-patch_size)    
    else:
        randX[i] = 0
  
# Extract & save patches
for m, t, y, x in zip(randM, randT, randY, randX):
    patch = data[m][0][t,y:y+patch_size,x:x+patch_size]
    path = Path('data', 'train', 
        f'{data[m][2].stem}_patch({m:03}-{t:04}-{y:04}-{x:04}).tif'
        )  
    io.imsave(path, patch, check_contrast=False)
