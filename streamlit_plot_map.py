import numpy as np
import pandas as pd
#import streamlit as st
import scipy as sci
map_data = pd.DataFrame(np.random.randn(1000, 2),columns=['lat','lon'])

n1=np.ndarray(shape=(2,2),dtype=int,)*5
print(n1)
n2 = np.full((3,4),"Hello")
print(n2)
