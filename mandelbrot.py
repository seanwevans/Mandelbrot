from numpy import *
from time import clock
from sys import argv
from sean import clear
from pylab import *

def mandelbrot(pict_dim, window, itermax):
	
	(n, m) = pict_dim
	(xmin, xmax, ymin, ymax) = window
	
	ix, iy = mgrid[0:n, 0:m]
	x = linspace(xmin, xmax, n)[ix]
	y = linspace(ymin, ymax, m)[iy]
	
	c = x+complex(0,1)*y
	del x, y
	
	img = zeros(c.shape, dtype=int)
	ix.shape = iy.shape = c.shape = n*m
	z = copy(c)
	
	for i in range(itermax):
		if not len(z): break
		
		multiply(z, z, z)
		add(z, c, z)
		
		rem = abs(z)>4
		
		img[ix[rem], iy[rem]] = i+1
		#img[ix[rem], iy[rem]] = i**i % 256
		
		rem = ~rem
		z = z[rem]
		ix, iy = ix[rem], iy[rem]
		c = c[rem]
		
	return transpose(img)

if __name__ == "__main__":
	import pygame
	from time import clock
	
	pygame.init()
	
	screen_resolution = (w, h) = (500, 500)
	screen = pygame.display.set_mode(screen_resolution)
		
	pict_dim = (w,h)
	window = (xmin, xmax, ymin, ymax) = (-2, 1, -1.5, 1.5)
	detail = 16
	xstep = .5
	ystep = .5
	running = True
	
	while running:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				running = False
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					xmin -= xstep
					xmax -= xstep
				if event.key == pygame.K_DOWN:
					xmin += xstep
					xmax += xstep
				if event.key == pygame.K_LEFT:
					ymin -= ystep
					ymax -= ystep
				if event.key == pygame.K_RIGHT:
					ymin += ystep
					ymax += ystep
				if event.key ==pygame.K_SPACE:		# Exit
					running = False
				if event.key == pygame.K_z:			# Zoom in
					xmin += xstep
					xmax -= xstep
					ymin += ystep
					ymax -= ystep
				if event.key == pygame.K_q:			# Zoom out
					xmin -= xstep
					xmax += xstep
					ymin -= ystep
					ymax += ystep
				if event.key == pygame.K_x:			# More detail
					detail *= 2
				if event.key == pygame.K_c:			# Less detail
					detail = int(detail / 2)
				if event.key == pygame.K_a:
					xstep *= 2
					ystep *= 2
				if event.key == pygame.K_s:
					xstep /= 2
					ystep /= 2
		
				window = (xmin, xmax, ymin, ymax)
				st = clock()
				ma = mandelbrot(pict_dim, window, detail)
				print(window, detail, xstep, ystep, clock()-st)
				surf = pygame.surfarray.make_surface(ma)
				screen.blit(surf, (0,0))
				pygame.display.flip()