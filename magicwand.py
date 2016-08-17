from scipy import misc
import numpy as np
from collections import deque

class Point:
	def __init__(self,x,y,img,threshold):
		self.data = img[y][x]
		self.x = x
		self.y = y
		self.width = img.shape[1]
		self.height = img.shape[0]
		self.threshold = threshold

	def childs(self):
		return_list = []
		if (self.y+1) < self.height:
			return_list.append((self.x, self.y+1))
		if (self.y-1) >= 0:
			return_list.append((self.x, self.y-1))
		if (self.x-1) >= 0:
			return_list.append((self.x-1, self.y))
		if (self.x+1) < self.width:
			return_list.append((self.x+1, self.y))
		return return_list

	def inThreshold(self,other_data):
		if (np.linalg.norm(self.data - other_data)) < self.threshold:
			return True
		else:
			return False

def run(filename, x, y, threshold , ouputfile):
	input_img = misc.imread(filename)
	input_img = preprocess_img(input_img)

	output_img = input_img.copy()
	bit_map = np.zeros(input_img.shape[:2])
	bit_map.fill(255)
	queue = deque()

	#first element
	first = Point(x,y,input_img,threshold)
	bit_map[y][x] = 0;
	queue.append(first)
	# #set bit map

	while len(queue) > 0 :
		cur = queue.popleft()
		childs = cur.childs()
		for (newx,newy) in childs:
			if (bit_map[newy][newx]) == 255 and first.inThreshold(input_img[newy][newx]):
				bit_map[newy][newx] = 0;
				queue.append(Point(newx,newy,input_img,threshold))
	output_img = np.dstack((output_img, bit_map))
	misc.imsave(ouputfile,output_img)



def preprocess_img(img):
	new_img = np.zeros((img.shape[0]+2,img.shape[1]+2,img.shape[2]))
	new_img.fill(255)
	new_img[1:img.shape[0]+1,1:img.shape[1]+1] = img
	return new_img


if __name__ =='__main__':
	import sys
	import os
	if(len(sys.argv)!=6):
		print("Usage:python magicwand.py [filename/directory] [ouputfile/directory] [x] [y] [threshold]")
	else:
		if (os.path.isdir(sys.argv[1])):
			list_of_files = os.listdir(sys.argv[1])
			for each in list_of_files:
				if (each.endswith('jpg') or each.endswith('jpeg')):
					new_name = each.split('.')[0] + '.png'
					print(new_name)
					run(sys.argv[1]+'/'+each, int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[2]+'/'+new_name)
		else:	
			run(sys.argv[1], int(sys.argv[3]), int(sys.argv[4]), int(sys.argv[5]), sys.argv[2])
