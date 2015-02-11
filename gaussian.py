import numpy as np
import matplotlib.pyplot as plt
import sys

def gaussian_2d(x, y, x0, y0, a, b , c, scale):
    return scale*np.exp( -(a*np.power(x-x0,2) + 2.0 * b * (x-x0) * (y-y0) + c * np.power(y-y0,2)) )


imsize=1024;
x0=512;		# uvfill 2 assumes that the pointing is at the centre of the map (centre = imsize/2)
y0=512;

bpa=0.0;
bmaj=5;	# assumed in pixels (FWHM)
bmin=5;
comp1=1;
norm1=0.0;


x=np.linspace(0, imsize-1, imsize);
y=np.linspace(0, imsize-1, imsize);
[X,Y]=np.meshgrid(x,y);


bpa=bpa*(np.pi/180.0);	# convert to radiens



bmaj=bmaj/(2*np.sqrt(2*np.log(2)));
bmin=bmin/(2*np.sqrt(2*np.log(2)));



a=0.5*(((np.cos(bpa)/bmaj)**2)+((np.sin(bpa)/bmin)**2));
b=0.25*np.sin(2.0*bpa)*(-1.0/(bmaj**2)+1.0/(bmin**2));
c=0.5*(((np.sin(bpa)/bmaj)**2)+((np.cos(bpa)/bmin)**2));

g1=gaussian_2d(X, Y, x0, y0, a, b , c, comp1);
normal_factor = np.sum(g1)
g1 = np.multiply(g1, norm1 / normal_factor)


plt.imshow(g1,aspect='auto')
plt.show()
np.savetxt("gaussian_vmap.csv", g1, delimiter=",")