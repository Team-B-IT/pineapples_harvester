from PIL import Image

error_list = []
with open("../train_tmp.txt") as f:
	for line in f:
		# print(line)
		line = line.split()
		image = 0
		try:
			image = Image.open(line[0])
		except:
			continue
		w, h = image.size
		for t in line[1:]:
			t = t.split(",")
			# print(t)
			box = []
			for i in t:
				i = int(i)
				# print(i)
				box.append(i)
			# print(box)
			if (box[0] not in range(0, w)
				or box[2] not in range(0, w)
				or box[1] not in range(0, h)
				or box[3] not in range(0, h)):
				error_list.append(line[0])
				print(line[0] + " Error!", h, w, box)
				break
count = 0
print(len(error_list))
fw = open("../train.txt", "w")
with open("../train_tmp.txt") as f:
	for line in f:
		if line.split()[0] not in error_list:
			fw.write(line)
			count += 1
			if count == 5000:
				break
fw.close()