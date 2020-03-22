from math import sin, cos, tan, atan, sqrt, radians



def to_coord(x, y,h):
	imgh = 1080
	imgw = 1920

	a = radians(42.5) # camera vertical view angle +/-3
	b = radians(69.4) # camera horizontal view angle +/-3
	aGAO = radians(50) # camera optical angle (to x-axis)  # goc cua camera so mat phang ngang 50

	AO = 140-h # distance from camera to ground # khoang cach tu cam xuong mat dat (mat ngang dit qua dua) #116
	CO = tan(aGAO - a/2)*AO

	AC = sqrt(AO*AO + CO*CO)

	AF = cos(a/2)*AC
	AG = AO/cos(aGAO) # optical line

# trapezium to triangle angle

	GO = tan(aGAO)*AO # projection of AG on ground
	RO = AO/tan(aGAO) 

	PQ = 2*tan(b/2)*AF # real world scaled width, PQ across F

	CD = 2*sin(a/2)*AC # real world scaled height
	x = x - imgw/2
	y = imgh/2 - y

	rx, ry = 0, 0

	HF = abs(y/imgh*CD) # real-scaled-height on image from (x, y) point to optical point
	aGAE = atan(HF/AF)
	aEAO = aGAO + aGAE if y >= 0 else aGAO - aGAE
	EO = tan(aEAO)*AO
	ry = EO

	imX = x/imgw*(AG*PQ/AF) 
	rx = imX*(EO + RO)/(GO + RO)
	#rx = int(rx)
	#ry = int(ry)
	print ('Camera POV:', rx, ry)
	return rx, ry

def to_coord_from_depth(x, y, depth):
	x = x - imgw/2
	y = imgh/2 - y

	rx, ry = 0, 0

	# Distance from camera to image in pixel
	hPixel = (imgw/2/tan(b/2) + imgh/2/tan(a/2)) / 2 # in pixels

	# Depth value in corresponding pixel of image
	depthPixel = sqrt(x*x + y*y + hPixel*hPixel) # pixels

	rx = depth/depthPixel*x # Real coordinate x
	ry = depth/depthPixel*sqrt(y*y + hPixel*hPixel)*sin(aGAO + atan(y/hPixel)) # Real coordinate y

	#rx = int(rx)
	#ry = int(ry)

	print ('Camera POV:', rx, ry)
	return rx, ry

if __name__ == '__main__':
	to_coord(300, 300)
	to_coord_from_depth(300, 300, 241.29857024)