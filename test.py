
# coding: utf-8

# #Tutorial of Pytff
#
# First lets import the required modules
#

# In[2]:

import os
import random

import numpy as np

import pytff


# In[3]:
PATH = os.path.abspath(os.path.dirname(__file__))
tff = pytff.TFFCommand(tff_path=os.path.join(PATH, "_bin", "tff"))
periods = np.random.rand(10)
times = np.random.rand(10, 50)
values = np.random.rand(*times.shape)
tff_data, dff_data, match_data = tff.analyze(periods, times, values)


# ## Real Data Example

data = np.loadtxt(os.path.join(PATH, "data", "ogle.dat"))
periods = np.array([0.6347522])
times = data[:,0].reshape(1, len(data[:,0]))
values = data[:,1].reshape(1, len(data[:,1]))
tff_data, dff_data, match_data = tff.analyze(periods, times, values)
tff_data
tff_data[0]
tff_data["period"]






