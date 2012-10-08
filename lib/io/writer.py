'''
Created on Sep 24, 2012

@author: shawn
'''
from lib.options.config import configuration as config
import __builtin__

class FileWrapper(object):
	def __init__(self,obj):
		self._obj = obj

	def close(self,*args,**kwargs):
		print "Closing file..."
		self._obj.close(*args,**kwargs)

	def __getattr__(self, attr):
		# see if this object has attr
		# NOTE do not use hasattr, it goes into
		# infinite recurrsion
		if attr in self.__dict__:
			# this object has it
			return getattr(self, attr)
		# proxy to the wrapped object
		return getattr(self._obj, attr)

def marked_open(*params):
	global _open
	#print params
	if len(params) > 1 and (params[1] == 'w' or params[1] == 'wb' or params[1] == 'w+'):
		print "Opening file..."
		return FileWrapper(_open(*params))
	else:
		return _open(*params)

_open = __builtin__.open
__builtin__.open = marked_open
"""
def __defattr__(self,attr):
	if hasattr(self.obj, attr):
		attr_value = getattr(self.obj,attr)
		if isinstance(attr_value,types.MethodType):
			def callable(*args, **kwargs):
				return attr_value(*args, **kwargs)
			return callable
		else:
			return attr_value
	else:
		raise AttributeError
"""
