import numpy as np
#choose the first 5 equation and the last one.
A=np.mat('50,-20,-20,-20,0,0; -20,30,0,0,0,0; -10,0,40,0,-20,-20; -20,0,0,30,0,-20; 0,-10,-20,0,20,0; 1,1,1,1,1,1') 
b=np.array([0,0,0,0,0,1])       
x=np.linalg.solve(A,b)         
print ('Solution',x)
