import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw, ImageFile
import os

num_box = [0] * 22
classes = []

ImageFile.LOAD_TRUNCATED_IMAGES = True

with open('../model_data/bkseeing_classes.txt') as f:
	for line in f:
		classes.append(line.replace('\n',''))

with open("../train.txt") as f:
	for line in f:
		print(line)
		ok = False
		img = Image.open("../"+line.split(' ')[0].replace('\n',''));
		for box in line.split()[1:]:
			a = list(int(i) for i in box.split(','))
			x = int(box.split(',')[4])
			num_box[x] += 1
			if (x == 21):
				ok = True
				draw = ImageDraw.Draw(img)
				draw.rectangle([a[0], a[1], a[2], a[3]], outline = "green")
		if (ok):
			img.show()
			os.system("pause")

for i in range(22):
	print(classes[i] + ": " + str(num_box[i]))
plt.bar(classes, num_box, width = 0.5, color = "green", linewidth = 0.5)
plt.show()