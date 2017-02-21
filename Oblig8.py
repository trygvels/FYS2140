from scitools.std import *
from matplotlib.pyplot import *

N = 1000
hbarc = 1240.0/(2*pi) #nmeV
V0 = 10.0             #eV
a = 1.0               #nm
m = 0.511*10**6       #eV/c**2


z = linspace(0.001, 2*pi, N)
"""
z0 = a/hbarc*sqrt(2*m*V0)
zsqrA = zeros(N)
for i in range(N):
	zsqrA[i] = sqrt((z0/z[i])**2-1)
#plot(z, zsqrA,z, -1/tan(z))  #-1/tan(z) for anti og tan(z) for sym
ylim(0,15)
show()
"""
z1 = 1.479 #Fra sym plot
z2 = 2.955 #Fra Antisym plot


#SYMMETRISK k=k1
z=z1
l = z/a
k1 = l*tan(l*a)
k2 = -l*1/tan(l*a)
k = k1
A = (exp(k*a)*cos(l*a))/sqrt(a+1/k)
B = 1/sqrt(a+1/k)

x = linspace(-3,3,N)
psi = zeros(N)
for i in range(N):
	if x[i]>a:
		psi[i] = A*exp(-k*x[i])
	elif -a <= x[i] <= a:
		psi[i] = B*cos(l*x[i])
	else:
		psi[i] = A*exp(k*x[i]) 
psi1=abs(psi)**2

#ANTISYMMETRISK k=k2
z=z2
l = z/a
k1 = l*tan(l*a)
k2 = -l*1/tan(l*a)
k = k2
A = (exp(k*a)*sin(l*a))/sqrt(a+1/k)
B = 1/sqrt(a+1/k)

psi = zeros(N)
for i in range(N):
	if x[i]>a:
		psi[i] = A*exp(-k*x[i])
	elif -a <= x[i] <= a:
		psi[i] = B*sin(l*x[i])
	else:
		psi[i] = -A*exp(k*x[i]) 
psi2=abs(psi)**2

plot(x, psi1, x,psi2)
show()

