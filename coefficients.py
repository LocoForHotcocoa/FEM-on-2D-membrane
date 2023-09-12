import numpy as np
from scipy.special import jv, jn_zeros
import math

pi, cos, sin = np.pi, np.cos, np.sin

dr = .05
dtheta = .1

# ----------------------------------------------------------------------------
# user defined initial functions for t=0
# you can add or change these but make sure f(a, theta) = 0

# if you add more functions, 
# make sure to add it to the cosint() and sinint() on line 62

def func1(r, theta, a):
    return .5*(math.exp(a*a) - math.exp(r*r))

def func2(r, theta, a):
    return cos(3*theta)*sin(r/a * pi)

def func3(r, theta, a):
    return cos(5*theta)*sin(r/a*2*pi)

# ----------------------------------------------------------------------------
# polar integral with an initial function as a parameter

def polarint(func, rmin, rmax, thetamin, thetamax):
    sum = 0
    
    for r in np.linspace(rmin, rmax, int((rmax-rmin) / dr)):
        for theta in np.linspace(thetamin, thetamax, int((thetamax - thetamin) / dtheta)):
            darea = func(r, theta) * r * dr * dtheta
            sum += darea

    return sum

# ----------------------------------------------------------------------------
# calculates both A and B for all (n,m)

def coef(ns, ms, a, choice):

    A = np.zeros((ns+1, ms))
    B = np.zeros((ns+1, ms))


    print('\n\ncalculating coefficients...\n')

    nlist = np.linspace(0, ns, ns+1, dtype = 'int')
    mlist = np.linspace(1, ms, ms, dtype = 'int')

    for n in nlist:

        z_n = jn_zeros(n, ms)

        for m in mlist:
            print(f'n = {n}, m = {m}:')
            l_nm = z_n[m-1] / a

# ----------------------------------------------------------------------------
# choice of intitial function, either func1 or func2
# you can add your own functions as long as f(a, theta) = 0

            def cosint(r, theta):

                if choice == 1:
                    return func1(r, theta, a) * jv(n, l_nm * r) * cos(n*theta)
                elif choice == 2:
                    return func2(r, theta, a) * jv(n, l_nm * r) * cos(n*theta)
                elif choice == 3:
                    return func3(r, theta, a) * jv(n, l_nm * r) * cos(n*theta)
                
            def sinint(r, theta):
                
                if choice == 1:
                    return func1(r, theta, a) * jv(n, l_nm * r) * sin(n*theta)
                elif choice == 2:
                    return func2(r, theta, a) * jv(n, l_nm * r) * sin(n*theta)
                elif choice == 3:
                    return func3(r, theta, a) * jv(n, l_nm * r) * sin(n*theta)
                
# ----------------------------------------------------------------------------

            if n == 0:
                A[n][m-1] = 1 / (pi * a*a * jv(1, z_n[m-1])**2) * polarint(cosint, 0, a, -pi, pi)
                B[n][m-1] = 0
            else:
                A[n][m-1] = 2 / (pi * a*a * jv(n+1, z_n[m-1])**2) * polarint(cosint, 0, a, -pi, pi)
                B[n][m-1] = 2 / (pi * a*a * jv(n+1, z_n[m-1])**2) * polarint(sinint, 0, a, -pi, pi)

            print(f'\tA = {A[n][m-1]}, B = {B[n][m-1]}')

    return (A,B)


# def sin_coef(ns, ms, a, choice):

#     B = np.zeros((ns+1, ms))
#     print('\n\ncalculating cosine coefficients...\n')

#     nlist = np.linspace(0, ns, ns+1, dtype = 'int')
#     mlist = np.linspace(1, ms, ms, dtype = 'int')

#     for n in nlist:

#         z_n = jn_zeros(n, ms)

#         for m in mlist:
#             print(f'n = {n}, m = {m}:')
#             l_nm = z_n[m-1] / a

#             def integrand(r, theta):
#                 return func1(r, theta) * jv(n, l_nm * r) * sin(n*theta)
            
#             if n == 0:
#                 B[0][m-1] = 0
#             else:
#                 B[n][m-1] = 2 / (pi * a*a * jv(n+1, z_n[m-1])**2) * polarint(integrand, 0, a, -pi, pi)
#             print(B[n][m-1])

#     return B


# # def sin_coef(nlist, mlist, a):

# #     B = np.zeros((nlist, mlist))

# #     for i in product(nlist, mlist):
# #         (n, m) = i

# #         z_nm = jn_zeros(n, m)
# #         l_nm = z_nm / a

# #         def integrand(r, theta): 
# #             func1(r, theta) * jv(n, l_nm * r) * sin(n*theta)

# #         if n == 0:
# #             B[n][m] = 0
# #         else:
# #             B[n][m] = 2 / (pi * a*a * jv(1, z_nm)**2) * polarint(integrand, 0, a, -pi, pi)

# #     return B
        


    
# # n = 10
# # m = 10

# # A = cos_coef(2,2, 1)
# # B = sin_coef(2,2, 1)

# # print(A)
# # print(B)
# (A, B) = coef(2,2,1, '1')
# print(A)