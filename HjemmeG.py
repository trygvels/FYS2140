import time
start_time = time.time()


# Tools for sparse matrices
import scipy.sparse as sparse
import scipy.sparse.linalg

# Numerical tools
from numpy import *

# Plotting library
from matplotlib.pyplot import *

"""Physical constants"""
_E0p = 0.511        # Rest energy for a proton [MeV]
_hbarc = 0.1973      # [MeV pm]
_c = 3.0e2           # Spees of light [pm / as]

N = 61
energi = zeros(N)
transa = zeros(N)
refla = zeros(N)
Analtransa = zeros(N)
i = 0
for l in linspace(1,6,N):
    a = 1.0
    m = 0.511/(_c**2)

    def Psi0( x ):
        '''
        Initial state for a travelling gaussian wave packet.
        '''
        x0 = -5.0 # [pm]
        a = 1.0 # [pm]
        #l = 0.01 # [pm^-1]

        A = ( 1. / ( 2 * pi * a**2 ) )**0.25
        K1 = exp( - ( x - x0 )**2 / ( 4. * a**2 ) )*exp(1j*l*x)

        return A * K1

    def potentialWell( x, V0=1.0, L=0.25 ):
        """
        Gives the potential for a potential well of depth depth and width width.

        @param depth Gives the depth of the potential well. Given as the magnitude
        (positive integer / double / float).
        @param width Gives the width of the potential well. Given as positive
        integer definig the fraction of the x spectrum to contain the well. For
        example, 1 will mean that the well covers the whole spectrum and 0.5 that
        it covers half of it.
        """
        # Declare new empty array with same length as x
        potential = zeros( len( x ) )


        potential[ (np.abs(x-0)).argmin() : (np.abs(x-L)).argmin()] = V0

        return potential


    if __name__ == '__main__':
        nx = 10001 # Number of points in x direction
        dx = 0.01 # Distance between x points [pm]

        # Use zero as center, same amount of points each side
        a = - 0.5 * nx * dx
        b = 0.5 * nx * dx
        x = linspace( a, b, nx )

        # Time parameters
        T = 0.1 # How long to run simulation [as]
        dt = 1e-3 # The time step [as]
        t = 0
        time_steps = int( T / dt ) # Number of time steps

        # Constants - save time by calculating outside of loop
        k1 = + ( 1j * _hbarc * _c) / (2. * _E0p )
        k2 = - ( 1j * _c ) / _hbarc

        # Create the initial state Psi
        Psi = Psi0(x)
        
        # Create the matrix containing central differences. It it used to
        # approximate the second derivative.
        data = ones((3, nx))
        data[1] = -2*data[1]
        diags = [-1,0,1]
        D2 = k1 / dx**2 * sparse.spdiags(data,diags,nx,nx)
        #print size(D2)
        # Identity Matrix
        I = sparse.identity(nx)

        # Create the diagonal matrix containing the potential.
        V_data = potentialWell(x)
        V_diags = [0]
        V = k2 * sparse.spdiags(V_data, V_diags, nx, nx)
        '''
        # Put mmatplotlib in interactive mode for animation
        ion()

        # Setup the figure before starting animation
        fig = figure() # Create window
        ax = fig.add_subplot(111) # Add axes
        line, = ax.plot( x, abs(Psi)**2, label='$|\Psi(x,t)|^2$' ) # Fetch the line object

        # Also draw a green line illustrating the potential
        ax.plot( x, V_data, label='$V(x)$' )

        # Add other properties to the plot to make it elegant
        fig.suptitle("Solution of Schrodinger's equation with potential well") # Title of plot
        ax.grid('on') # Square grid lines in plot
        ax.set_xlabel('$x$ [pm]') # X label of axes
        ax.set_ylabel('$|\Psi(x, t)|^2$ [1/pm] and $V(x)$ [MeV]') # Y label of axes
        ax.legend(loc='best') # Adds labels of the lines to the window
        #draw() # Draws first window
        '''
        # Time loop
        while t < T:
            """
            For each iteration: Solve the system of linear equations:
            (I - k/2*D2) u_new = (I + k/2*D2)*u_old
            """
            # Set the elements of the equation
            A = (I - dt/2*(D2 + V))
            b = (I + dt/2. * (D2 + V)) * Psi

            # Calculate the new Psi
            Psi = sparse.linalg.spsolve(A,b)

            # Update time
            t += dt

            # Plot this new state
            #line.set_ydata( abs(Psi)**2 ) # Update the y values of the Psi line
            #draw() # Update the plot

        # Turn off interactive mode
        ioff()
      #  print "done"
        halvvegs = round(nx/2)
        refleksjon = trapz(abs(Psi[:halvvegs])**2, x[:halvvegs])
        transmisjon = trapz(abs(Psi[halvvegs+1:])**2, x[halvvegs+1:])
     #   print 'refleksjon = %g, transmisjon = %g, sum = %g' %(refleksjon, transmisjon, refleksjon+transmisjon)
        
        energi[i] = ((_hbarc/_c)**2*(l**2+1/(4*a**2)))/(2*m)
        transa[i] = transmisjon
        refla[i] = refleksjon
	
	L = 0.25
	#V = 1.
	m = 0.511/(_c**2)

	Analtransa[i]= 1/(1.+1./(4*energi[i]*(1.-energi[i]))*(sinh(L*_c/_hbarc*sqrt(2*m*(1-energi[i]))))**2)

        i += 1
        # Add show so that windows do not automatically close
        #show()
    #print "time----", (time.time()-start_time)



plot(energi,transa);
plot(energi,refla); 
plot(energi, Analtransa); 
xlabel('E / [MeV]'); ylabel('Sannsynlighet'); title('Sannsynlighet for Transmisjon og Refleksjon numerisk'); 
legend(['Transmisjon', 'Refleksjon', 'Analytisk Transmisjon '], loc='upper center')
show()
