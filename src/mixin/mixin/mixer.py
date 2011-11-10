import sys
from mixin.util import wrap_class_meta

__all__ = ['include']

def include(*mixins):
	"""
	The global method that is used in classes to include mixins
	"""
	frame = sys._getframe(1)
	locals = frame.f_locals
	
	if (locals is frame.f_globals) or (
		('__module__' not in locals) and sys.version_info[:3] > (2, 2, 0)):
		raise TypeError("include can be used only from a class definition.")
	
	if '__included_mixins__' in locals:
		raise TypeError("include can be used only once in a class definition.")
	
	locals['__included_mixins__'] = mixins
	wrap_class_meta(_include_mixins, depth=2)


def _extend(cls,*mixins):
	"""
	With that classmethod we will be able to add mixins 
	to the class dynamically
	"""
	for mixin in mixins:
		#here call all of the mixins included methods
		_include_mixin(cls, mixin)
	
	
def _include_mixins(cls):
	"""
	Final method that is called on class to include methods
	"""
	mixins = cls.__dict__['__included_mixins__']
	del cls.__included_mixins__
	for mixin in mixins:
		#here call all of the mixins included methods
		_include_mixin(cls, mixin)
		
	#also lets add a classmethod to the class so we can extend the
	#classes dynamically 
	setattr(cls, "extend", classmethod(_extend))
	
	return cls

def _include_mixin(cls, mixin):
	"""
	Attach a mixin to specified class
	"""
	if hasattr(mixin, 'included') and callable(getattr(mixin, 'included')):
		mixin.included(cls)
		
	mixin_members = dir(mixin)
	for mixin_member in mixin_members:
		mixin_member_obj = getattr(mixin, mixin_member)
		if callable(mixin_member_obj) and not mixin_member.startswith("_") and not mixin_member == 'included':
			if not hasattr(cls, mixin_member):
				setattr(cls,mixin_member, mixin_member_obj.im_func)

