from math import sin, cos, tan, atan, sqrt, radians

imgw = 1920
imgh = 1080

a = radians(42.5) # camera vertical view angle +/-3
b = radians(69.4) # camera horizontal view angle +/-3
aGAO = radians(39) # camera optical angle (to z-axis)

AO = 80 # distance from camera to ground
CO = tan(aGAO - a/2)*AO

AC = sqrt(AO*AO + CO*CO)

AF = cos(a/2)*AC
AG = AO/cos(aGAO) # optical line

# trapezium to triangle angle

GO = tan(aGAO)*AO
RO = AO/tan(aGAO)

PQ = 2*tan(b/2)*AF # PQ get through F

CD = 2*sin(a/2)*AC

def to_coord(x, y):
	x = x - imgw/2
	y = imgh/2 - y

	rx, ry = 0, 0

	HF = abs(y/imgh*CD)
	aGAE = atan(HF/AF)
	aEAO = aGAO + aGAE if y >= 0 else aGAO - aGAE
	EO = tan(aEAO)*AO
	ry = EO

	imX = x/imgw*(AG*PQ/AF)
	rx = imX*(EO + RO)/(GO + RO)
	print ('Camera POV:', rx, ry)
	return rx, ry

if __name__ == '__main__':
	to_coord(300, 300)