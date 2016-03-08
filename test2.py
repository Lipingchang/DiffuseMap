import math
def entropy(x):
	return -x*math.log(x)


print 2*entropy(1.0/3)+3*entropy(1.0/9)
