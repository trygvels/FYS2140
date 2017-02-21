from math import e, pi

z = 1.+1j

print z

print e**(z)

print e**(-z)

print e**(z)*e**(-z)

def Mnu(T):
	M = (2*pi*(h*nu)**3)/((hc)**2*e**(h*nu/(kb*T))-1)
	return M
