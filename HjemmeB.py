from matplotlib.pyplot import *
from numpy import *
x = linspace(-4*10**-12,8*10**-12, 1000)
a = 1*10**-12
x0 = 2*10**-12
def f(x):
	f = (2*pi*a**2)**(1/4)*exp(-(x-x0)**2/(4*a**2))
	return f
plot(x,f(x))
xlabel('x [pm]')
ylabel('$|\Psi(x, t)|^2$ [Enhetslos]')
grid('on')
show()
