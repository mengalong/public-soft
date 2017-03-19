#coding: utf8

#如何定义带参数的装饰器

#装饰器工厂
def typeassert(*ty_args, **ty_kargs)
	def decorator(func):
		#获取函数和参数类型的映射
		#func->a,b
		#d = {'a':int, 'b': str}

		def wrap(*args, **kargs):
			# arg in d, instance(arg, d[arg])
			return func(*args, **kargs)
		return wrapper
	return decorator
