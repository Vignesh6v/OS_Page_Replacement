#!/usr/bin/env python
import math
import sys
import os
import string


def get_file(file_name):
	#defaut values
	flag = True
	page_ref = []
	total_pages = 0


	file = open(file_name)
	for line in file:
		line.strip('')
		if flag:
			total_pages = int(line)
			print 'Total Pages:{}'.format(total_pages)
			flag = False
			continue

		page_ref.append(int(line))
	file.close()
	return [total_pages, page_ref]


def pff(total_pages,page_ref):
	#If F too small, then large no.of page fautls. Thus F is set to an optimum value(40). On inc the value F beyond, that page fault will become constant.

	x = 0.01*total_pages
	f = math.ceil(x)
	print 'PF: {}'.format(f)

	# default values
	count_lastfault = 0
	count_lastTenfrms = 0
	max_frms = 0
	count_maxfrms = 0
	count_totalpagefault = 0
	resident_Set = dict()

	for pr in page_ref:
		if pr in resident_Set:
			count_lastfault +=1
			resident_Set[pr] = 1 
		else:
			count_totalpagefault += 1

			if count_lastfault < f:
				resident_Set[pr] = 1
			else:
				temp = dict()
				for pair in resident_Set:
					if resident_Set[pair] == 0:
						temp[pair] = resident_Set[pair]
					else:
						resident_Set[pair] = 0
				for key in temp:
					resident_Set.pop(key,None)

				temp.clear()
				resident_Set[pr] = 1

			count_lastfault = 0

		size = len(resident_Set)
		if size < 10:
			count_lastTenfrms +=1
		if size > max_frms:
			max_frms = size
			count_maxfrms = 1
		elif size == max_frms:
			count_maxfrms += 1


	print 'Total page faults: {}'.format(count_totalpagefault)
	print 'Count on: no of frames in memory less than 10: {}'.format(count_lastTenfrms)
	print 'Count on: max no of frames in memeory: {}'.format(count_maxfrms)
	print 'Max # of frames used at a time: {}'.format(max_frms)




#variable interval sampling working set
def vsvw(total_pages,page_ref):
	m = math.ceil(0.45*total_pages)
	q = math.ceil(0.40*total_pages)
	l = math.ceil((0.10*total_pages)+total_pages)


	#If Q has a very large value, then L  will trigger to reset the bits.
	print 'M: {}, L: {}, Q: {}'.format(m,l,q)

	resident_Set = dict()
	count_lastTenfrms = 0
	max_frms = 0
	count_maxfrms = 0
	intrvl_pagefault = 0
	elapsed_time = 0 
	count_totalpagefault = 0

	for pr in page_ref:
		if pr in resident_Set:
			resident_Set[pr] = 1
		else:
			intrvl_pagefault +=1
			count_totalpagefault +=1

			if (intrvl_pagefault < q):
				resident_Set[pr] = 1
			elif (intrvl_pagefault >= q and elapsed_time < m):
				resident_Set[pr] = 1
			elif intrvl_pagefault >= q:
				temp = dict()
				for pair in resident_Set:
					if resident_Set[pair] ==0:
						temp[pair]=resident_Set[pair]
					else:
						resident_Set[pair] = 0

				for key in temp:
					resident_Set.pop(key,None)

				temp.clear()
				resident_Set[pr] = 1
				elapsed_time = 0
				intrvl_pagefault = 1

		elapsed_time +=1
		if elapsed_time >= l:
			temp = dict()
			for pair in resident_Set:
				if resident_Set[pair] == 0:
					temp[pair] = resident_Set[pair]
				else:
					resident_Set[pair] = 0

			for key in temp:
				resident_Set.pop(key,None)

			temp.clear()
			elapsed_time = 0
			intrvl_pagefault = 0

		size = len(resident_Set)
		if size < 10:
			count_lastTenfrms +=1
		elif size > max_frms:
			max_frms = size
			count_maxfrms = 1
		elif size == max_frms:
			count_maxfrms +=1


	print 'Total Page Faults: {}'.format(count_totalpagefault)
	print 'Count on: no of frames in the memory less than 10: {}'.format(count_lastTenfrms)
	print 'Count on: max no of frames in memory: {} '.format(count_maxfrms)
	print 'Max # of frames used at a time: {}'.format(max_frms)





def main():
	try:
		file_name = sys.argv[-1]
		items = get_file(file_name)
		total_pages, page_ref = items[0],items[1]
		#print total_pages, page_ref
		print '----------------------------------------------------'
		print 'PFF'
		pff(total_pages,page_ref)
		print '----------------------------------------------------'
		print 'VSVW'
		vsvw (total_pages,page_ref)

	except:
		print 'Enter a proper file name'

if __name__=='__main__':main()




