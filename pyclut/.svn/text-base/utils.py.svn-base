
def clamp(x, min=0, max=1):
	if x>max: return max
	elif x<min: return min
	else: return x

def clamp_angle(x):
	if x<0: x+=360
	if x>360: x-=360
	return x

def get_keyval(event):
	"""Depending on the clutter version, the key value on a KeyEvent
	can be access by event.key.keyval or event.keyval"""
	if hasattr(event, "key"):
		return event.key.keyval
	else:
		return event.keyval

class AbstractMethodNotImplemented(Exception): pass



