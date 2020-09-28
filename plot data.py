import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img = mpimg.imread('cage.png')

df = pd.read_csv('logged_data/20200916_location.csv')
print(len(df))

plt.figure(1,figsize=(18,6))
plt.imshow(img)
plt.plot(df['x_pixel'].to_numpy(),df['y_pixel'].to_numpy(),'.')
#plt.xlim(0,71*17)
#plt.ylim(0,-24*17)
plt.savefig('20200916.png')
plt.show()