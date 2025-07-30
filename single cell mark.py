import numpy as np
import matplotlib.pyplot as plt
from PIL import Image
from pathlib import Path


base_path = Path()
image_path = Path()
output_path = Path()

try:
    F = np.load()
    Fneu = np.load()
    iscell = np.load()
    stat = np.load()
    image = Image.open()
    image_array = np.array()
except Exception as e:
    print()
    exit()


target_cell_ids = []


valid_cells = [i for i in target_cell_ids if iscell[i, 0] > 0.5]
print( {[x+1 for x in valid_cells]})



fig = plt.figure(frameon=False)
plt.imshow(image_array, cmap='gray')


for cell_id in valid_cells:
    xpix = stat[cell_id]['xpix']
    ypix = stat[cell_id]['ypix']
    plt.scatter(xpix, ypix, s=1, alpha=0.05, color='red')


plt.axis('off')
plt.gca().set_axis_off()
plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0, wspace=0)
plt.margins(0, 0)


plt.show()


fig.savefig(output_path, bbox_inches='tight', pad_inches=0, dpi=image.info.get('dpi', 300))
plt.close(fig)

print({output_path})