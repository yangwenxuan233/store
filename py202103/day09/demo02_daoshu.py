import numpy as np
import matplotlib.pyplot as plt
x = np.arange(-10,10.1,0.1)
y = x**2
plt.plot(x,y)
plt.show()


''' 
链式求导sigmoid函数的导函数
F(x)=1/(1+e^(-x))
t = 1+e^(-x)
f(t)=1/t=t^(-1)
f'(t)=-1*t^(-2)
t1=e^(-x)
t=1+t1
t'(t1)=1
F'(t1) = F'(t)*t'(t1)=-t^(-2)*1*t1'(t2(x))
t2(x)=-x
t1'(x)=e^(t2(x))*1*t2(x)=e^(-x)*(-1)
F(x)=t^(-2)*1*e^(-x)
    =(1+e^(-x))^(-2)*e^(-x)
    =(1/(1+e^(-x))^2)*e^(-x)
    =e^(-x)/(1+e^(-x))*(1/(1+e^(-x))
    =(1-e^(-x)/(1+e^(-x))-1/1+e^(-x))*(1/(1+e^(-x))
    =(1-F(x))*F(x)
    '''

