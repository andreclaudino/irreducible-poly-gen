#!/usr/bin/env python
# coding: utf-8

# # Gerador de irredutíveis

# In[141]:


from sympy.abc import *
from sympy.polys import *
from sympy import symbols
from functools import reduce
from sympy import randprime, Rational
from multiprocessing import Process
import pathlib
import numpy as np


# ## Gerador de redutíveis
# 
# A técnica utilizada para gerar redutíveis é gerar os redutíveis, multiplicá-los e combinar os coeficientes resultantes. Portandos, vamos criar redutíveis base.

# In[12]:


ai = symbols('a0:4')
bj = symbols('b0:4')


# In[23]:


pis = [(x-a) for a in ai]
pjs = [(y-b) for b in bj]


# In[109]:


abi = ai+bj

def coefs():
    return {u: Rational(randprime(-40, 40), randprime(-40, 40)) for u in abi}

def pij(gx, gy):
    parte_x = reduce(lambda u,v: u*v, pis[:gx], 1)
    parte_y = reduce(lambda u,v: u*v, pjs[:gy], 1)
   
    return (parte_x*parte_y).subs(coefs()).ratsimp()

from sympy import factor_list

def geratriz(basedir, gx, gy):
    count = 0
    limit = 1000000
    
    while count < limit:
        p = pij(gx, gy) + pij(gx, gy) - pij(gx, gy)

        if len(factor_list(p)[1]) == 1:
            dirname = f"{basedir}/gx={gx}/gy={gy}"
            filename = f"{dirname}/{hash(p)}"
            pathlib.Path(dirname).mkdir(parents=True, exist_ok=True)
            np.save(filename, np.array([p]))
            count =  count + 1

for gx in np.arange(3, 0, -1):
    for gy in np.arange(1, gx+1):
        p = Process(target=geratriz, args=("irredutiveis", gx, gy))
        p.start()
    p.join()


# In[ ]:




