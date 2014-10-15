import copy

class SOP(list):
	
	def __init__(self,arg):
		self.parse(arg)

	def parse(self,exp):
		products = exp.split('+')
		self.extend([product.split('*') for product in products])
	
	def __repr__(self):
		return '+'.join([''.join(p) for p in self])
	
	def __str__(self):
		return '+'.join([''.join(p) for p in self])
	
	def __add__(self,other):
		self_cp = copy.deepcopy(self)
		self_cp.extend(other)
		return self_cp

	def __mul__(self,other):
		result = SOP('')
		result.pop()
		if len(other)==1:
			for product in self:
				tmp = product[:]
				tmp.append(other[0])
				result.append(tmp)
		else:
			for product in other:
				result += self * product
		return result

	def __invert__(self):
		for p in self:
			
	'''
	def __add__(self,other):
		return self + other
	
	def __invert__(self,other):
		result = []
		for product in self:
			if len(product)==1:
				result *= [(-product[0])]
			else:
				return ~product
		return result
	'''

e1 = SOP('a+b')
e2 = SOP('c+d')
#print a

