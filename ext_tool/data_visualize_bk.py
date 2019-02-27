import matplotlib as mpl
import matplotlib.pyplot as plt
from PIL import Image
import os

num_box = [0] * 22
classes = []

with open('../model_data/bkseeing_classes.txt') as f:
	for line in f:
		classes.append(line.replace('\n',''))

with open("../train.txt") as f:
	for line in f:
		for box in line.split()[1:]:
			x = int(box.split(',')[4])
			num_box[x] += 1
			# if (x == 1):
			# 	img = Image.open(line.split(' ')[0]);
			# 	img.show()
			# 	os.system("pause")

# for i in range(20):
# 	print(classes[i] + ": " + str(num_box[i]))
plt.bar(classes, num_box, width = 0.5, color = "green", linewidth = 0.5)
plt.show()
for i in range(22):
	print(str(i)+": "+classes[i])
	print(num_box[i])