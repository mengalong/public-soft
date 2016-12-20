#coding:utf8

#装饰器实例学习
#

#memo传递进来的是函数
def memo(func):
	cache = {}

	#wrap是包裹函数，做一些预处理
	def wrap(*args):
		print args
		if args not in cache:
			cache[args] = func(*args)
		return cache[args]

	#返回wrap
	return wrap

#斐波那契数列，输出第N项的值

@memo
def fibonacci(n):
	if n <= 1:
		return 1
	return fibonacci(n - 1) + fibonacci(n - 2)

#print fibonacci(50)


#总共有10个台阶的楼梯，从下面走到上面，一次只能迈一个太极，并且不能后退
#走完这个楼梯有多少种方法

@memo
def climb(n, steps):
	count = 0
	if n == 0:
		count = 1
	elif n > 0:
		for step in steps:
			count += climb(n-step, steps)
	return count


print climb(2, (1,2,3))
