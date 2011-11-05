import sys

__all__ = ['MetaMixer']

class MetaMixer(type):
	
	def extend(cls, mixin):
		MetaMixer.mix_class(cls, mixin)
	
	@staticmethod	
	def mix_class(cls, mixin):
		if hasattr(mixin, 'included') and callable(getattr(mixin, 'included')):
			mixin.included(cls)
		
		mixin_members = dir(mixin)
		for mixin_member in mixin_members:
			mixin_member_obj = getattr(mixin, mixin_member)
			if callable(mixin_member_obj) and not mixin_member.startswith("_") and not mixin_member == 'included':
				if not hasattr(cls, mixin_member):
					setattr(cls,mixin_member, mixin_member_obj.im_func)
				
	def __init__(cls, name, bases, attrs):
		if hasattr(cls, 'includes'):
			for mixin in getattr(cls, 'includes'):
				#here call all of the mixins included methods
				MetaMixer.mix_class(cls, mixin)

