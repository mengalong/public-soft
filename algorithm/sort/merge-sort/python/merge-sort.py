#!/usr/bin/env python

def spli(lists):
	if len(lists) <= 1:
		return lists
	
	num = len(lists) / 2
	left = spli(lists[:num])
	right = spli(lists[num:])
	
	return dichotomia_sort(left, right)

def dichotomia_sort(left,right):
	l,r = 0,0
	result = []
	while l < len(left) and r < len(right):
		if left[l] < right[r]:
			result.append(left[l])
			l += 1
		else:
			result.append(right[r])
			r += 1
	result += right[r:]
	result += left[l:]
	return result

print spli([4,6,3,8,1,2,9])
		
