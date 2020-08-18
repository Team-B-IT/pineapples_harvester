from math import sin, cos, tan, atan, sqrt, radians

imgw = 1280
imgh = 720
a = radians(42.5) # camera vertical view angle +/-3,, goc mo cua cam theo phuong doc
b = radians(69.4) # camera horizontal view angle +/-3, goc mo cua cam theo phuong ngang
cameraHeight = 135 #1m4

angleToHorizon = 35 #goc ss mp ngang=35 do 1,29h / 83cm x
aGAO = radians(90-angleToHorizon) # camera optical angle (to x-axis)  # goc cua camerg ngang 50 la so mat phan
#tu dong 10 den dong 46 klo can thiet

# AO = 140-40 # distance from camera to ground # khoang cach tu cam xuong mat dat (mat ngang dit qua dua) #116
# CO = tan(aGAO - a/2)*AO

# AC = sqrt(AO*AO + CO*CO)

# AF = cos(a/2)*AC
# AG = AO/cos(aGAO) # optical line

# # trapezium to triangle angle

# GO = tan(aGAO)*AO # projection of AG on ground
# RO = AO/tan(aGAO) 

# PQ = 2*tan(b/2)*AF # real world scaled width, PQ across F

# CD = 2*sin(a/2)*AC # real world scaled height

# def to_coord(x, y):
# 	x = x - imgw/2
# 	y = imgh/2 - y

# 	rx, ry = 0, 0

# 	HF = abs(y/imgh*CD) # real-scaled-height on image from (x, y) point to optical point
# 	aGAE = atan(HF/AF)
# 	aEAO = aGAO + aGAE if y >= 0 else aGAO - aGAE
# 	EO = tan(aEAO)*AO
# 	ry = EO

# 	imX = x/imgw*(AG*PQ/AF) 
# 	rx = imX*(EO + RO)/(GO + RO)
# 	#rx = int(rx)
# 	#ry = int(ry)
# 	print ('Camera POV:', rx, ry)
# 	return rx, ry

def to_coord_from_depth(x, y, depth):
	x = x - imgw/2
	y = imgh/2 - y

	rx, ry, rz = 0, 0, 0

	# Distance from camera to image in pixel
	hPixel = (imgw/2/tan(b/2) + imgh/2/tan(a/2)) / 2 # in pixels #FG'

	# Depth value in corresponding pixel of image
	depthPixel = sqrt(x*x + y*y + hPixel*hPixel) # FS'

	rx = depth/depthPixel*x # Real coordinate x SY
	ry = depth/depthPixel*sqrt(y*y + hPixel*hPixel)*sin(aGAO + atan(y/hPixel)) # Real coordinate y

	#rx = int(rx)
	#ry = int(ry)
	# depth += 5.0
	rz = cameraHeight - sqrt(depth * depth - (rx * rx + ry * ry))
	rx = rx*1.08
	ry = ry*1.02
	depth = float("{0:.2f}".format(depth))
	rx = float("{0:.2f}".format(rx))
	ry = float("{0:.2f}".format(ry))
	rz = float("{0:.2f}".format(rz))
	print('depth: ', depth)
	print ('Camera POV (X,Y,Z):', rx, ry, rz)
	return rx, ry, rz

if __name__ == '__main__':
	# to_coord(882, 112)
	to_coord_from_depth(812, 302, 235)
