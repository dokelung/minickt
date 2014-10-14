class Product(frozenset):

	def __init__(self,arg):
		super(Product, self).__init__(arg)

	def __repr__(self):
		return '('+','.join([str(var) for var in self])+')'

	def __str__(self):
		return '('+','.join([str(var) for var in self])+')'

	def __add__(self,other):
		return SOP([self,other])

	def __mul__(self,other):
		return self | other

	def __invert__(self):
		return SOP([Product([-var]) for var in self])

	def inv(self):
		return SOP([Product([-var]) for var in self])

	def andWith(self,other):
		return self | other

	def orWith(self,other):
		return SOP([self,other])

	def isOne(self):
		if len(self):
			return True
		return False

class SOP(set):

	def __init__(self,arg):
		super(SOP, self).__init__(arg)

	def __repr__(self):
		return '+'.join([str(p) for p in self])

	def __str__(self):
		return '+'.join([str(p) for p in self])

	def __add__(self,other):
		return self | other

	def __mul__(self,other):
		return SOP([p1.andWith(p2) for p1 in self for p2 in other])

	def __invert__(self):
		sop = SOP(Product([]))
		for p in self:
			sop |= p.inv()
		return sop

	def inv(self):
		sop = SOP(Product([]))
		for p in self:
			sop |= p.inv()
		return sop

	def andWith(self,other):
		return SOP([p1.andWith(p2) for p1 in self for p2 in other])

	def orWith(self,otehr):
		return  self | other

	def isZero(self):
		if len(self)==0:
			return True
		return False

	#def clear(self):
	#	return self
	#	pass
	
	def clear(self):
		self = list(self)
		clear_lst = []
		for i,p in enumerate(self):
			for v in p:
				if -v in p:
					clear_lst.append(i)

		#print 'clst',clear_lst

		tmp = []
		for i in range(len(self)):
			#print i,
			if not i in clear_lst:
				#print 'append', self[i]
				tmp.append(self[i])
			else:
				pass
				#print 'hello'

		return SOP(tmp)

		#self = SOP([self[i] for i in range(len(self)) if not i in clear_lst])
		