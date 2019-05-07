# Testprogramm klimaprobe on Raspberry Pi
import time
import board
import neopixel
import tkinter as tk
import random

#initialisiere Leinwand
root=tk.Tk()
root.attributes('-fullscreen', True)
root.geometry("%dx%d+0+0" % (1024,768))
root.bind("<Escape>", lambda e: root.destroy())

canvas=tk.Canvas()
canvas=tk.Canvas(root, width=1024, height=768, bg='black', bd=0, highlightthickness=0)
canvas.pack()
root.update()

# Choose an open pin connected to the Data In of the NeoPixel strip, i.e. board.D18
# NeoPixels must be connected to D10, D12, D18 or D21 to work.
pixel_pin = board.D18

# The number of NeoPixels
num_pixels = 1428

# The order of the pixel colors - RGB or GRB. Some NeoPixels have red and green reversed!
# For RGBW NeoPixels, simply change the ORDER to RGBW or GRBW.
ORDER = neopixel.GRB

pixels = neopixel.NeoPixel(pixel_pin, num_pixels, brightness=0.3, auto_write=False,
                           pixel_order=ORDER)
	
def paint(pixnr, col_r, col_g, col_b):
	#breite 42
	#hoehe  12
	i=int(pixnr%119)
	line=int(pixnr/119)*2
	ofs=0	
	if i>59:
		i=i-59
		line=line+1
		ofs=6
	pixcolor="#"+"%02X" % col_r+"%02X" % col_g+"%02X" % col_b
	#canvas.create_rectangle(line*20,600-(i*10),(line*20)+20,600-(i*10+10), fill=pixcolor, width=0)
	canvas.create_rectangle(line*42,768-(i*12-ofs),(line*42)+42,768-(i*12+12-ofs), fill=pixcolor, width=0)
	root.update()

while True:
	points = list(range(1428))
	random.shuffle(points)	
	for block in range(56):	
		for i in points[block*28:block*28+28]:
			pixels[i]=(i%255,0,255-i%255)
			paint(i,i%255,0, 255-i%255)
		pixels.show()

	time.sleep(2)
		
	random.shuffle(points)
	for block in range(56):	
		for i in points[block*28:block*28+28]:
			pixels[i] =(0,0,0)
			paint(i,50,50,50)
		pixels.show()
		
	time.sleep(2)
	canvas.delete('all')
