update = "../../data/"

f = open("../train.txt")
lines = []
for line in f:
	# lines.append(update + line)
	lines.append(line)

f = open("../train.txt", "w")
for line in lines:
	f.write(line[3:])