
num_box = [0] * 20

with open("../train.txt") as f:
	for line in f:
		for box in line.split()[1:]:
			num_box[int(box.split(',')[4])] += 1
print(num_box)