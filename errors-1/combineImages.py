import numpy as np
from PIL import Image
from PIL import _imaging

imgNum = 97 
rows = 5
imgPerRow = 24

for i in range(rows) : 
    start = imgPerRow * i
    end = imgPerRow * (i + 1)
    if end > imgNum : 
        end = imgNum
    print(start, end)
    list_im = map(lambda x: str(x) + '.png', range(start, end))
    imgs    = [ Image.open(i) for i in list_im ]
    # pick the image which is the smallest, and resize the others to match it (can be arbitrary image shape here)
    min_shape = sorted( [(np.sum(i.size), i.size ) for i in imgs])[0][1]
    imgs_comb = np.vstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )

    # save that beautiful picture
    imgs_comb = Image.fromarray( imgs_comb)
    imgs_comb.save( 'row-' + str(i) + '.png' )    

# for a vertical stacking it is simple: use vstack
imgs = [ Image.open(i) for i in map(lambda x: 'row-' + str(x) + '.png', range(rows - 1)) ]
# imgs_comb = np.vstack(imgs)
imgs_comb = np.hstack( (np.asarray( i.resize(min_shape) ) for i in imgs ) )
imgs_comb = Image.fromarray( imgs_comb)
imgs_comb.save( 'Trifecta_vertical.jpg' )
