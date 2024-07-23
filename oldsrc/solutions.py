import numpy as np
from itertools import product
from scipy.special import jv, jn_zeros


pi, cos, sin = np.pi, np.cos, np.sin

def wave_solution(r, theta, t, A, B, a, c, ns, ms):

    u = np.zeros((len(r), len(theta)))

    nlist = np.linspace(0, ns, ns+1, dtype = 'int')
    mlist = np.linspace(1, ms, ms, dtype = 'int')

    for n in nlist:

        z_n = jn_zeros(n, ms)

        for m in mlist:
            l_nm = z_n[m-1] / a

            # for this solution, we are only looking at the case when initial velocity is 0
            # this means that the C and D coefficients for sin(l_nm*c*t) are zero.
            # just to make it a little simpler :)

            u = u + jv(n, l_nm*r) \
            * cos(l_nm*c*t) \
               * ((A[n][m-1]*cos(n*theta) + B[n][m-1]*sin(n*theta)))
            
        
            
    # for i in product(nlist , mlist):
    #     (n, m) = i

    #     z_nm = jn_zeros(n, m)
    #     l_nm = z_nm / a

    #     # for this solution, we are only looking at the case when initial velocity is 0
    #     # this means that the C and D coefficients for sin(l_nm*c*t) are zero.
    #     # just to make it a little simpler :)

    #     u = u + jv(n, l_nm*r) \
    #         * cos(l_nm*c*t) \
    #            * ((A[n][m]*cos(n*theta) + B[n][m]*sin(n*theta)))

    return u
        
