import os
import sys

filelist = os.listdir('./data/')

for i in range(13):
	x = ''
	if (i < 10):
		x = '0'+str(i)
	else:
		x = str(i)
	newdir='./data/' + 'data'+x+'/'
	os.mkdir(newdir)

	for j in range(i*77, (i+1)*77):
		os.rename('./data/'+filelist[j], newdir+filelist[j])
