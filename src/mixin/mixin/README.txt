mixin library is a simple metaclass library that aims to bring to python
Ruby like 'include' keyword. Python already supports mixins with multiple
inheritance. The purpose here is to achieve the same result without using
multiple inheritance.

How to use that library ? 
You create a few mixin classes they are same as normal classes. But the self
here is the object that will be mixed in. First import the library.

>>> from mixin import include

Lets create a mixin class. The philosophy behind mixins is to create little 
classes that can be mixed in other classes. In Ruby if your class has a method
called each when you include Enumerable module you get a bunch of methods for free.
Lets implement here a simple one :

>>> class EnumerableMixin(object):
... 	def map(self, func):
...			return [func(i) for i in self.each()]
...

>>> class MyClass(object):
...		include(EnumerableMixin)
...	
...		def __init__(self, *args):
...			self.arr = args
...	
...		def each(self):
...			for i in self.arr:
...				yield i
...

>>> m = MyClass("hello", "dummy")
>>> m.map(lambda s: s.upper()) == ["HELLO", "DUMMY"]
True

You can also mix a class attr runtime also :

>>> class AnotherMixin(object):
...		def mixed(self):
...			return "mixed"
...

>>> MyClass.extend(AnotherMixin)
>>> m = MyClass("hello", "dummy")
>>> m.mixed()
'mixed'


Easy :)