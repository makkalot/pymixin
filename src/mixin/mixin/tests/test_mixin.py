from mixin import MetaMixer

class MixinClass(object):

	@staticmethod
	def included(cls):
		print "MixinClass : I was included on %s"%cls

	def mixed_method(self):
		return "mixed"	

class EnumMixin(object):
	
	def map(self):
		return [i for i in self.each()]

class M(object):
	
	__metaclass__ = MetaMixer
	includes = [MixinClass,EnumMixin]

	def __init__(self, a, b):
		self.a = a
		self.b = b
		self.ar = [self.a, self.b]
	
	def each(self):
		for i in self.ar:
			yield i

class AnotherMixin(object):
	
	def extended(self):
		return "extended"

def test_mixer():
	m = M(1,2)
	assert m.mixed_method() == "mixed"
	assert m.map() == [1,2]
 
	M.extend(AnotherMixin)
	m = M(2,3)
	m.extended() == "extended"

