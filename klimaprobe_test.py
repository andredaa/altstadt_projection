# Testprogramm klimaprobe on Raspberry Pi
# Version 0.4

import sys
import time
import board
import neopixel
import pygame
import random
import colorsys

#initialisiere Leinwand
pygame.init()
screen=pygame.display.set_mode((1024, 768),pygame.FULLSCREEN)
screen.fill((0,0,0))
pygame.display.update()
pygame.mouse.set_visible(False)

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 1428

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.5, auto_write=False,
                           pixel_order=ORDER)

# draw rectangles from pixels	
def show_matrix1():
	rh=12 # rectangle height
	rw=42 # rectangle width
	pix=-1
	for x in range(12):
		for y in range(60):
			pix+=1
			pygame.draw.rect(screen, pixels[pix] ,(x*2*rw+10, 740-(y*rh), rw, rh))
		for y in range(59):
			pix+=1
			pygame.draw.rect(screen, pixels[pix] ,(x*2*rw+rw+10, 734-(y*rh), rw, rh))		
	pygame.display.update()

# draw (hexa) polygons from pixels	
def show_matrix():
	pix=-1
	for x in range(12):
		for y in range(60):
			pix+=1
			posx=x*2*42+10
			posy=740-(y*12)
			plist=[(posx,posy),(posx+6,posy-6),(posx+36,posy-6),(posx+42,posy),(posx+36,posy+6),(posx+6,posy+6)]
			pygame.draw.polygon(screen, pixels[pix], plist)
		for y in range(59):
			pix+=1
			posx=x*2*42+42+10
			posy=734-(y*12)
			plist=[(posx,posy),(posx+6,posy-6),(posx+36,posy-6),(posx+42,posy),(posx+36,posy+6),(posx+6,posy+6)]
			pygame.draw.polygon(screen, pixels[pix], plist)					
	pygame.display.update()
	
# read events and draw all
def show_all():
	# check for events
	for event in pygame.event.get():
		if (event.type == pygame.QUIT) or (event.type == pygame.KEYDOWN):
			pixels.fill((0,0,0))
			pixels.show()
			show_matrix()
			sys.exit()
	#paint all 		
	pixels.show()
	show_matrix()

# rotate Pixel
def pxrot(n):
	n*=3
	pixels.buf = pixels.buf[-n:] + pixels.buf[:-n]
	return

# shift Pixel
def pxshift(n):
	n*=3
	if n==0:
		return
	if n>0:
		pixels.buf = bytearray(n) + pixels.buf[:-n]
	else:
		pixels.buf = pixels.buf[-n:] + bytearray(-n)
	return

# create colors
mycolors=[]
step=1.0/714
cpoint=0.0
for x in range(714):
	mycolors.extend([int(i) for i in colorsys.hsv_to_rgb(cpoint,0.9,180)])
	cpoint=cpoint+step

# Indizes der 24 unteren LED	
unten = (0  , 60,119,179,238,298,357,417,476,536,595,655,
	   714,774,833,893,952,1012,1071,1131,1190,1250,1309,1369)

# mainloop
while True:
	#rainbow
	print(len(pixels.buf))
	for i in range(714):
		pixels[i]=(mycolors[i*3],mycolors[i*3+1],mycolors[i*3+2])
	for i in range(714):
		pixels[i+714]=(mycolors[i*3],mycolors[i*3+1],mycolors[i*3+2])
		
	#fadein
	x=0.0
	while x<0.5:
		pixels.brightness=x
		show_all()
		x=x+0.015
		
	#rotate Rainbow
	for i in range(140):
		pxrot(20)
		show_all()

	#fadeout
	x=0.5
	while x>0:
		pixels.brightness=x
		show_all()
		x=x-0.015
	pixels.fill((0,0,0))
	pixels.brightness=0.5
	
	#white ring
	pixels.fill((0,0,0))
	for i in unten:
		pixels[i]=(150,150,150)
	pixels.show()
	for i in range(58):
		pxshift(1)
		show_all()	
	for i in range(58):
		pxshift(-1)
		show_all() 
	pixels.fill((0,0,0))	
	  
	#snakes
	# movement: -59 links oben, 60 rechts oben, 59 rechts unten, -60 links unten	   
	for m in range(4):
		for n in range(9):
			col=random.randint(0,714)
			#col=713
			farbe=((mycolors[col*3],mycolors[col*3+1],mycolors[col*3+2]))
			pos=random.choice(unten)
			pixels[0]=(farbe)
			for i in range(random.randint(4,15)):
				pxrot(60)
				pixels[pos]=(farbe)
				show_all()

		now=time.time()
		while time.time()<now+4: #Laufzeit 4s
			pxrot(60)
			for i in unten:
				pixels[i]=(0,0,0)
			show_all()

	#von unten nach oben herausschieben
	for i in range(60):
		for i in unten:
			pixels[i]=(0,0,0)
		pxshift(1)
		show_all()	
		
	time.sleep(2)
	
	for n in range(2):
		# aus probe_1.py script übernommen und angepasst
		points = list(range(1428))
		random.shuffle(points)	
		for block in range(56):	
			for i in points[block*28:block*28+28]:
				pixels[i]=(i%255,0,255-i%255)
			show_all()

		time.sleep(2)
			
		random.shuffle(points)
		#for block in range(56):
		for block in range(56):	
			for i in points[block*28:block*28+28]:
				pixels[i] =(0,0,0)
			show_all()
				
		time.sleep(2)

exit()
