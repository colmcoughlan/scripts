from astropy.io import fits
from astropy.modeling import models, fitting
import numpy as np
from matplotlib import pyplot as plt
from matplotlib.patches import Ellipse

#############	Edit here	#######################

hdulist = fits.open('eclipse.fits')
clip_level=70000
sigmax_guess = 5
sigmay_guess = 5


##############	End of user input	################


#	Operations on data (flip and clip etc.)

scidata = hdulist[0].data
scidata = np.flipud(scidata)
scidata = np.clip(scidata,0,clip_level)
scidata = np.multiply(np.add(scidata,-clip_level),-1)





# plotting

dimx,dimy = scidata.shape
print "Image dimensions = "+str(scidata.shape)
ax = plt.gca()
fig = plt.gcf()
global xlim
global ylim
global have_patch
global ell
xlim = [0, np.max(dimy)]
ylim = [0, np.max(dimx)]
have_patch = False
fit_p = fitting.LevMarLSQFitter()


def ondraw(event):
	global xlim
	global ylim
	xlim = np.rint(ax.get_xlim())
	ylim = np.rint(ax.get_ylim())	# get x and y coords of zoom window as nearest integers

def onclick(event):
	global have_patch
	global ell
	if event.button == 3:
		if event.xdata != None and event.ydata != None:
#			print "xlim = "+str(xlim)
#			print "ylim = "+str(ylim)
			ylen = np.abs(xlim[0]-xlim[1])	# N.B. x and y swapping
			xlen = np.abs(ylim[0]-ylim[1])
			y = np.linspace(0,xlen-1,xlen)
			x = np.linspace(0,ylen-1,ylen)
			X,Y = np.meshgrid(x,y)

			ystart = np.min(xlim)
			xstart = np.min(ylim)
#			xval = int(event.xdata + 0.5) - np.min(xlim)
#			yval = int(event.ydata + 0.5) - np.min(ylim)
#			print "Shapes: X = "+str(X.shape)+", Y = "+str(Y.shape)+", data = "+str(scidata[xstart:xstart+xlen,ystart:ystart+ylen].shape)
			xval,yval = np.unravel_index(scidata[xstart:xstart+xlen,ystart:ystart+ylen].argmax(), scidata[xstart:xstart+xlen,ystart:ystart+ylen].shape)
			p_init = models.Gaussian2D(0.5*np.max(scidata[xstart:xstart+xlen,ystart:ystart+ylen]), xval, yval ,sigmax_guess, sigmay_guess)
			print "Detected regional peak = "+str(np.max(scidata[xstart:xstart+xlen,ystart:ystart+ylen]))+" at ("+str(yval+ystart)+" , "+str(xval+xstart)+")"
			p = fit_p(p_init, X, Y, scidata[xstart:xstart+xlen,ystart:ystart+ylen])
			print "Using initial guess of x = "+str(yval+ystart)+", y = "+str(xval+xstart)+", amp = "+str(clip_level)
			print str(p)
			print "Mean position of fitted Gaussian = ("+str(ystart+p.x_mean[0])+","+str(xstart+p.y_mean[0])+")"
			print "Contours shown are 3 sigma."
			
			if have_patch:
				ell.remove()
			ell = Ellipse(xy=(int(p.x_mean[0]+ystart+0.5), int(p.y_mean[0]+xstart+0.5)),width=3.0*p.x_stddev[0], height=3.0*p.y_stddev[0],angle=p.theta[0]*180.0/np.pi,edgecolor='r', fc='None', lw=1)
			ax.add_patch(ell)
			have_patch = True
			plt.show()
			
def format_coord(x, y):
    col = int(x+0.5)
    row = int(y+0.5)
    if col>=0 and col<dimx and row>=0 and row<dimy:
        z = scidata[row,col]
        return 'x=%1.4f, y=%1.4f, z=%1.4f'%(x, y, z)
    else:
        return 'x=%1.4f, y=%1.4f'%(x, y)

ax.format_coord = format_coord
			
			
cid = fig.canvas.mpl_connect('draw_event', ondraw)
cid = fig.canvas.mpl_connect('button_press_event', onclick)

print "Zoom to region of interest and right click to fit."
print "Note: entire zoomed image will be used in fit."
plt.imshow(scidata, cmap='gray')
plt.colorbar()
plt.show()

#hdu = fits.PrimaryHDU(scidata)
#hdu.writeto('new.fits')