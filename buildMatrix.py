# Thomas Kosciuch
# thomas.kosciuch@mail.utoronto.ca
# Nov 28th 2018
# updated Nov. 29th 2018

from __future__ import division    # solution to complete division using floats
from tqdm import tqdm
import numpy as np                 # 

## RETURNS BOUNDARY NODES
def boundsA(x_nodes,y_nodes,debug='n'):
    """Package builds the a-matrix for finite-difference discretization"""
    """return  w_bound, e_bound, n_bound, s_bound """
    dim = x_nodes * y_nodes         # specified to reduce calculations
    w_bound = [0] * y_nodes         # creating 0-matricies to find
    e_bound = [0] * y_nodes         # all boundary nodes
    s_bound = [0] * x_nodes
    n_bound = [0] * x_nodes

    if debug == 'y':  # Debugger notifies progress            
        print("finding boundaries")
    for i in range (x_nodes):            # boundary nodes are populated
        s_bound[i] = i                   # used to populate matricies 
        n_bound[i] = (dim - x_nodes + i)
    for i in range (y_nodes):            
        w_bound[i] = (i * x_nodes)
        e_bound[i] = (i+1) * x_nodes -1

    if debug == 'y':   # Debugger prints boundary nodes
        xB = "n:" + str(n_bound) + "\n"+ " s:" + str(s_bound) 
        yB = "e:" + str(e_bound) + "\n"+ " w:" + str(w_bound) 
        print("boundaries: \n",  xB, "\n",  yB)
    return w_bound, e_bound, s_bound, n_bound

## APPLIES CENTRAL DIFFERENCE
def CDiff(x_nodes,y_nodes,D_x, D_y, F_x, F_y, Boundary, debug="n"):
    """
    Requires:
    x_nodes = number of nodes along x 
    y_nodes = number of nodes along y
    D_x = Diffusivity along x, type = float
    D_y = Diffusivity along y, type = float
    F_x = Force along X, type = matrix (x by y)
    F_y = Force along Y, type = matrix (x by y)
    Optional:
    debug, "y" if you want debug, off by default
    """
    ## setting up stuff (simple math)
    dim = x_nodes * y_nodes         # specified to reduce calculations
    w_bound = [0] * y_nodes         # creating 0-matricies to find
    e_bound = [0] * y_nodes         # all boundary nodes
    s_bound = [0] * x_nodes
    n_bound = [0] * x_nodes

    if debug == 'y':  # Debugger notifies progress            
        print("finding boundaries")

    for i in range (x_nodes):            # boundary nodes are populated
        s_bound[i] = i                   # used to populate matricies 
        n_bound[i] = (dim - x_nodes + i)
    for i in range (y_nodes):            
        w_bound[i] = (i * x_nodes)
        e_bound[i] = (i+1) * x_nodes -1

    if debug == 'y':   # Debugger prints boundary nodes
        xB = "n:" + str(n_bound) + "\n"+ " s:" + str(s_bound) 
        yB = "e:" + str(e_bound) + "\n"+ " w:" + str(w_bound) 
        print("boundaries: \n",  xB, "\n",  yB)
    # Declaring variables
    a_w        = [0] * dim              # Creating empty matricies for all nodes
    a_e        = [0] * dim
    a_s        = [0] * dim
    a_n        = [0] * dim
    sp_p       = 0
    su_p       = 0
    B          = [0] * dim
    sp_W       = [0] * dim
    su_W       = [0] * dim
    sp_E       = [0] * dim
    su_E       = [0] * dim
    sp_S       = [0] * dim
    su_S       = [0] * dim
    sp_N       = [0] * dim
    su_N       = [0] * dim

    #Boundaries
    phi_W = Boundary[0]
    phi_E = Boundary[1]
    phi_S = Boundary[2]
    phi_N = Boundary[3]

    ## answer matricies ##
    a = [0] * dim                      # make a 
    for i in range(dim):               # 0-array
        a[i] = [0] * dim
    B   = [0] * dim

    # POPULATING USING CENTRAL DIFFERENCE
    print("populating central difference")
    pbar = tqdm(range(dim))              # load progress bar
    for i in range(dim):
        pbar.update(1)                   # progress indicator
        if i not in  w_bound:       # populating non-boundary conditions
            a[i][i - 1]        = a[i][i - 1] - (D_x + (F_x[i - 1] / 2))
            a[i][i]            = a[i][i] + (D_x + (F_x[i - 1] / 2))
        if i not in  e_bound:
            a[i][i + 1]        = a[i][i + 1] - (D_x - (F_x[i + 1] / 2))
            a[i][i]            = a[i][i] + (D_x - (F_x[i + 1] / 2))
        if i not in  s_bound:
            a[i][i - x_nodes]  = a[i][i - x_nodes] - (D_y + (F_y[i - x_nodes] / 2))
            a[i][i]            = a[i][i] + (D_y + (F_y[i - x_nodes] / 2))
        if i not in  n_bound:
            a[i][i + x_nodes]  = a[i][i + x_nodes] - (D_y - (F_y[i + x_nodes] / 2))
            a[i][i]            = a[i][i] + (D_y - (F_y[i + x_nodes] / 2))
        if i in      w_bound:      # populating boundary conditions
            sp_W[i]            = -(2*D_x + F_x[i])
            su_W[i]            = (2*D_x + F_x[i])* phi_W
            a[i][i]            = a[i][i] - sp_W[i]
            B[i]               = B[i] + su_W[i]
        if i in      e_bound:
            sp_E[i]            = -(2*D_x - F_x[i])
            su_E[i]            = (2*D_x - F_x[i])* phi_E
            a[i][i]            = a[i][i] - sp_E[i]
            B[i]               = B[i] + su_E[i]
        if i in      s_bound:
            sp_S[i]            = -(2*D_y + F_y[i])
            su_S[i]            = (2*D_y + F_y[i])* phi_S
            a[i][i]            = a[i][i] - sp_S[i]
            B[i]               = B[i] + su_S[i]
        if i in      n_bound:
            sp_N[i]            = -(2*D_y - F_y[i])
            su_N[i]            = (2*D_y - F_y[i]) * phi_N
            a[i][i]            = a[i][i] - sp_N[i]
            B[i]               = B[i] + su_N[i]
    return a, B


# APPLIES UPWIND DIFFERENCE
def UDiff(x_nodes,y_nodes,D_x, D_y, F_x, F_y, Boundary, debug="n"):
    """
    Requires:
    x_nodes = number of nodes along x 
    y_nodes = number of nodes along y
    D_x = Diffusivity along x, type = float
    D_y = Diffusivity along y, type = float
    F_x = Force along X, type = matrix (x by y)
    F_y = Force along Y, type = matrix (x by y)
    Optional:
    debug, "y" if you want debug, off by default
    """
    ## setting up stuff (simple math)
    dim = x_nodes * y_nodes         # specified to reduce calculations
    w_bound = [0] * y_nodes         # creating 0-matricies to find
    e_bound = [0] * y_nodes         # all boundary nodes
    s_bound = [0] * x_nodes
    n_bound = [0] * x_nodes

    if debug == 'y':  # Debugger notifies progress            
        print("finding boundaries")
    for i in range (x_nodes):            # boundary nodes are populated
        s_bound[i] = i                   # used to populate matricies 
        n_bound[i] = (dim - x_nodes + i)
    for i in range (y_nodes):            
        w_bound[i] = (i * x_nodes)
        e_bound[i] = (i+1) * x_nodes -1

    if debug == 'y':   # Debugger prints boundary nodes
        xB = "n:" + str(n_bound) + "\n"+ " s:" + str(s_bound) 
        yB = "e:" + str(e_bound) + "\n"+ " w:" + str(w_bound) 
        print("boundaries: \n",  xB, "\n",  yB)
 
    dim = x_nodes* y_nodes

    a_w        = [0] * dim              # Creating empty matricies for all nodes
    a_e        = [0] * dim
    a_s        = [0] * dim
    a_n        = [0] * dim
    sp_p       = 0
    su_p       = 0
    B          = [0] * dim
    sp_W       = [0] * dim
    su_W       = [0] * dim
    sp_E       = [0] * dim
    su_E       = [0] * dim
    sp_S       = [0] * dim
    su_S       = [0] * dim
    sp_N       = [0] * dim
    su_N       = [0] * dim

       #Boundaries
    phi_W = Boundary[0]
    phi_E = Boundary[1]
    phi_S = Boundary[2]
    phi_N = Boundary[3]

    ## answer matricies ##
    a = [0] * dim                      # make a 
    for i in range(dim):               # 0-array
        a[i] = [0] * dim
    B                          = [0] * dim
    # POPULATING USING CENTRAL DIFFERENCE
    print("populating upwind difference")
    pbar = tqdm(range(dim))
    for i in range(dim):
        pbar.update(1)
        if i not in w_bound:       # populating non-boundary nodes
            a[i][i - 1]        = a[i][i - 1] - (D_x + max((F_x[i - 1]),0))
            a[i][i]            = a[i][i] + (D_x + max((F_x[i - 1]),0))
        if i not in e_bound:
            a[i][i + 1]        = a[i][i + 1] - (D_x + max(-(F_x[i + 1]),0))
            a[i][i]            = a[i][i] + (D_x + max(-(F_x[i + 1]),0))
        if i not in s_bound:
            a[i][i - x_nodes]  = a[i][i - x_nodes] - (D_y + max((F_y[i - x_nodes]),0))
            a[i][i]            = a[i][i] + (D_y + max((F_y[i - x_nodes]),0))
        if i not in n_bound: 
            a[i][i + x_nodes]  = a[i][i + x_nodes] - (D_y + max(-(F_y[i + x_nodes]),0))
            a[i][i]            = a[i][i] + (D_y + max(-(F_y[i + x_nodes]),0)) 
        if i in w_bound:           # populating boundary nodes
            sp_W[i]            = -(2*D_x + max((F_x[i]),0))
            su_W[i]            = (2*D_x +  max((F_x[i]),0))* phi_W
            a[i][i]            = a[i][i] - sp_W[i] 
            B[i]               = B[i] + su_W[i]
        if i in e_bound:     
            sp_E[i]            = -(2*D_x + max(-(F_x[i]),0))
            su_E[i]            = (2*D_x + max(-(F_x[i]),0))* phi_E
            a[i][i]            = a[i][i] - sp_E[i]
            B[i]               = B[i] + su_E[i]
        if i in s_bound:     
            sp_S[i]            = -(2*D_y + max((F_y[i]),0))
            su_S[i]            = (2*D_y +  max((F_y[i]),0))* phi_S
            a[i][i]            = a[i][i] - sp_S[i]
            B[i]               = B[i] + su_S[i]
        if i in n_bound:     
            sp_N[i]            = -(2*D_y + max(-(F_y[i]),0))
            su_N[i]            = (2*D_x + max(-(F_y[i]),0))* phi_N
            a[i][i]            = a[i][i] - sp_N[i]
            B[i]               = B[i] + su_N[i]    
    return a, B




##### M A T R I X   F U N D A M E N T A L S #####
def meshposition(x_nodes,y_nodes,dx,dy):
    y_pos_temp    = [0] * y_nodes          # empty matrix for  x - values along x
    x_pos_temp    = [0] * x_nodes          # empty matrix for  y - values along y 
    x_pos_temp[0] = dx / 2                 # this is the first x-position
    y_pos_temp[0] = dy / 2                 # this is the first y-position

    for i in range (x_nodes - 1):          # populating x - values along x
        x_pos_temp[i+1] = x_pos_temp[i] + dx
        
    for i in range (y_nodes - 1):          # populating y - values along y 
        y_pos_temp[i+1] = y_pos_temp[i] + dy
    x_pos, y_pos = np.meshgrid(x_pos_temp, y_pos_temp)   
    x_pos = np.array(x_pos).flatten()      # flattens matrix to 1 by x*y 
    y_pos = np.array(y_pos).flatten()      # to strengthen consistency 
    return x_pos, y_pos

# this changes the dimensions of the A matrix - but i dont think i use it.:
#for i in range(dim):

def List2Matrix(X,x_nodes,y_nodes):
    print("list2Matrix")
    dim = x_nodes * y_nodes
    Ans = [0] * x_nodes    
    for i in range(y_nodes):
        Ans[i] = [0] * y_nodes
    for i in range(dim):
        row_num, col_num = divmod(i, x_nodes)
        Ans[row_num][col_num] = X[i]
    return Ans
    print("printed")

def CircV(x_pos,y_pos,x_length,y_length,dim):
    x_u   = [0] * dim                    # u(x) values are populated
    x_v   = [0] * dim                    # u(y) values
    r     = [0] * dim                  # value of r 
    theta = [0] * dim                  # value of theta 
    for i in range (dim):  
        r    [i] = ((x_pos[i] - x_length / 2) ** 2 + ( y_pos[i] - y_length/2 ) ** 2) ** (0.5) 
        denominat_temp = ( y_pos[i] - y_length / 2 ) 
        numerator_temp = ( x_pos[i] - x_length / 2 ) 
        theta[i] = np.arctan2(denominat_temp, numerator_temp) 
        x_u  [i] = - r [i] * np.sin(theta[i])    
        x_v  [i] = + r [i] * np.cos(theta[i]) 
    return x_u, x_v
