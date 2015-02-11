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

def gaussian_2d(x, y, x0, y0, a, b , c, scale):
    return scale*np.exp( -(a*np.power(x-x0,2) + 2.0 * b * (x-x0) * (y-y0) + c * np.power(y-y0,2)) )

imsize=2048;

x0=1024;
y0=1024;

x1=1078
y1=1078

x2=1118
y2=1118

bpa0=0.0;
bmaj0=3;	# assumed in pixels
bmin0=3;
comp0=1;

bpa1=0.0;
bmaj1=15;	# assumed in pixels
bmin1=15;
comp1=0.2;

bpa2=0.0;
bmaj2=30;	# assumed in pixels
bmin2=30;
comp2=0.1;


x=np.linspace(0, imsize-1, imsize);
y=np.linspace(0, imsize-1, imsize);
[X,Y]=np.meshgrid(x,y);


bpa0=bpa0*(np.pi/180.0);	# convert to radiens
bpa1=bpa1*(np.pi/180.0);	# convert to radiens
bpa2=bpa2*(np.pi/180.0);	# convert to radiens



bmaj0=bmaj0/(2*np.sqrt(2*np.log(2)));
bmin0=bmin0/(2*np.sqrt(2*np.log(2)));
bmaj1=bmaj1/(2*np.sqrt(2*np.log(2)));
bmin1=bmin1/(2*np.sqrt(2*np.log(2)));
bmaj2=bmaj2/(2*np.sqrt(2*np.log(2)));
bmin2=bmin2/(2*np.sqrt(2*np.log(2)));



a0=0.5*(((np.cos(bpa0)/bmaj0)**2)+((np.sin(bpa0)/bmin0)**2));
b0=0.25*np.sin(2.0*bpa0)*(-1.0/(bmaj0**2)+1.0/(bmin0**2));
c0=0.5*(((np.sin(bpa0)/bmaj0)**2)+((np.cos(bpa0)/bmin0)**2));

a1=0.5*(((np.cos(bpa1)/bmaj1)**2)+((np.sin(bpa1)/bmin1)**2));
b1=0.25*np.sin(2.0*bpa1)*(-1.0/(bmaj1**2)+1.0/(bmin1**2));
c1=0.5*(((np.sin(bpa1)/bmaj1)**2)+((np.cos(bpa1)/bmin1)**2));

a2=0.5*(((np.cos(bpa2)/bmaj2)**2)+((np.sin(bpa2)/bmin2)**2));
b2=0.25*np.sin(2.0*bpa2)*(-1.0/(bmaj2**2)+1.0/(bmin2**2));
c2=0.5*(((np.sin(bpa2)/bmaj2)**2)+((np.cos(bpa2)/bmin2)**2));

g0=gaussian_2d(X, Y, x0, y0, a0, b0 , c0, comp0);
normal_factor = np.sum(g0)
g0 = np.multiply(g0, comp0 / normal_factor)

g1=gaussian_2d(X, Y, x1, y1, a1, b1 , c1, comp1);
normal_factor = np.sum(g1)
g1 = np.multiply(g1, comp1 / normal_factor)

g2=gaussian_2d(X, Y, x2, y2, a2, b2 , c2, comp2);
normal_factor = np.sum(g2)
g2 = np.multiply(g2, comp2 / normal_factor)

g=g0+g1+g2;

plt.imshow(g,aspect='auto')
plt.show()
np.savetxt("triple_gaussian_imap.csv", g, delimiter=",")