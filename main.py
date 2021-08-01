import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import random
import pymc3 as pm
from src.functions import plot_pydeck



def main():
    activities = ["Home", "Modeling"]
    choice = st.sidebar.selectbox("Sidebar", activities)
    
    if choice == 'Home':
        homepage()
        
    if choice == 'Modeling':
        Modeling()
        

def homepage():


    if os.path.exists('./rate.csv'):
        csv = pd.read_csv('./rate.csv')
        ratings = list(csv['rate'])
        locations = list(csv['location'])
        titles = list(csv['title'])
        bottons = list(csv['botton'])

    else:
        ratings = []
        locations = []
        titles = []
        bottons = []

    # nums
    nums = [0, 1]

    # title
    title = random.choice(nums)
    if title == 0:
        st.markdown("**Time to Explore**")
    else:
        st.markdown(":radioactive_sign: Explore your self :radioactive_sign:")
    titles.append(title)

    # map
    location = random.choice(nums)
    if location == 0:
        map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [35.69, 139.70],columns=['lat', 'lon'])
        plot_pydeck(map_data, 35.69, 139.70)
    else:
        map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        plot_pydeck(map_data, 37.76, -122.4)
    locations.append(location)

    # botton
    botton = random.choice(nums)
    if botton == 0:
        st.button("Learn more")
    else:
        st.button("Go to checkout")
    bottons.append(botton)


    rate_list = [1,2,3,4,5]
    rate = st.sidebar.selectbox("Rate Page Design 1 - 5", options=rate_list)
    if rate != None:
        ratings.append(rate)
        df = pd.DataFrame(list(zip(ratings, locations, titles, bottons)), 
                     columns=['rate', 'location', 'title', 'botton'])
        df.to_csv('./rate.csv')


    
    
def Modeling():

    csv = pd.read_csv('./rate.csv')
    ratings = list(csv['rate'])
    locations = list(csv['location'])
    titles = list(csv['title'])
    bottons = list(csv['botton'])
    st.text("Equation")
    st.latex(r'''\alpha～N(0，10)''')
    st.latex(r'''\beta1～N(0，10)''')
    st.latex(r'''\beta2～N(0，10)''')
    st.latex(r'''\beta3～N(0，10)''')
    st.latex(r'''\theta=\alpha + \beta1 \times location + \beta3 \times titles + \beta3 \times bottons''')
    st.latex(r'''\sigma(t) = \frac{1}{1 + \exp (-t)}''')
    st.latex(r'''review～N(\sigma(\theta)，10)''')
    st.text("Modeling...")

    with pm.Model() as model:
        alpha = pm.Normal('alpha', mu=0, sigma=10)
        beta = pm.Normal('beta', mu=0, sigma=10, shape=3)
        comb = alpha + beta[0] * locations + beta[1] * titles + beta[2] * bottons
        theta = pm.Deterministic('theta', 1/(1+pm.math.exp(-comb)))
        obs = pm.Normal('obs', mu=theta, sigma=5, observed=ratings)
        trace = pm.sample(5000, chains=2)
        pm.plot_trace(trace, compact=True)
        st.dataframe(pm.summary(trace).iloc[:4, :])
            
            
            
if __name__ == "__main__":
    main()