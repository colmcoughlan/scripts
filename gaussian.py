# Copyright (c) 2014, Colm Coughlan
# All rights reserved.
# 
# Redistribution and use in source and binary forms, with or without modification, are permitted provided that the following
# conditions are met:
# 
# 1. Redistributions of source code must retain the above copyright notice, this list of conditions and the following disclaimer.
# 
# 2. Redistributions in binary form must reproduce the above copyright notice, this list of conditions and the following
# disclaimer in the documentation and/or other materials provided with the distribution.
# 
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, 
# BUT NOT LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT 
# SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING
# NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

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