import streamlit as st
import pydeck as pdk
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import os
import random
import pymc3 as pm
import itertools


def plot_pydeck(df, latitude, longitude):
    st.pydeck_chart(pdk.Deck(
         map_style='mapbox://styles/mapbox/light-v9',
         initial_view_state=pdk.ViewState(
             latitude=latitude,
             longitude=longitude,
             zoom=11,
             pitch=50,
         ),
         layers=[
             pdk.Layer(
                'HexagonLayer',
                data=df,
                get_position='[lon, lat]',
                radius=200,
                elevation_scale=4,
                elevation_range=[0, 1000],
                pickable=True,
                extruded=True,
             ),
             pdk.Layer(
                 'ScatterplotLayer',
                 data=df,
                 get_position='[lon, lat]',
                 get_color='[200, 30, 0, 160]',
                 get_radius=200,
             ),
         ],
     ))
    
    
def HomePage():


    if os.path.exists('./rate.csv'):
        csv = pd.read_csv('./rate.csv')
        types = list(csv['type'])
        locations = list(csv['location'])
        titles = list(csv['title'])
        bottons = list(csv['botton'])
        conversions = list(csv['conversion'])

    else:
        types = []
        locations = []
        titles = []
        bottons = []
        conversions = []

    # nums
    nums = [0, 1]
    arr = np.zeros(3)
    combinations = itertools.product(nums, repeat=3)
    combinations = [list(c) for c in combinations]

    # title
    title = random.choice(nums)
    titles.append(title)
    arr[0] = title

    # map
    location = random.choice(nums)
    locations.append(location)
    arr[1] = location

    # botton
    botton = random.choice(nums)
    bottons.append(botton)
    arr[2] = botton
    
    visualize(title, location, botton)
    
    rt = st.button("Return")
    conversions.append(rt == False)
    idx = combinations.index(list(arr))
    types.append(idx)

    #rate_list = [1,2,3,4,5]
    #rate = st.sidebar.selectbox("Rate Page Design 1 - 5", options=rate_list)
    if rt != None:
        df = pd.DataFrame(list(zip(types, locations, titles, bottons, conversions)), 
                     columns=['type', 'location', 'title', 'botton', 'conversion'])
        df.to_csv('./rate.csv')

def visualize(title, location, botton):
    
    if title == 0:
        st.latex(r'''\text{Time to Explore}''')
    else:
        st.markdown(":radioactive_sign: Time to Explore :radioactive_sign:")
        
    if location == 0:
        map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        plot_pydeck(map_data, 37.76, -122.4)
    else:
        map_data = pd.DataFrame(
        np.random.randn(1000, 2) / [50, 50] + [37.76, -122.4],columns=['lat', 'lon'])
        st.map(map_data)
        
    if botton == 0:
        st.button("Learn more")
    else:
        st.button("Go to checkout")
    
    
    
def Modeling():

    csv = pd.read_csv('./rate.csv')

    _,n = np.unique(csv['type'], return_counts=True)
    cv = [np.sum(csv.groupby('type').get_group(i)['conversion']) for i in range(8)]

    z = np.zeros((8, 3))
    combinations = itertools.product([0,1], repeat=3)
    for idx, c in enumerate(combinations):
        z[idx, :] = c
    
    st.latex(r'''\text{Equation}''')
    st.latex(r'''\alpha～\mathcal{N}(0，10)''')
    st.latex(r'''\beta1～\mathcal{N}(0，10)''')
    st.latex(r'''\beta2～\mathcal{N}(0，10)''')
    st.latex(r'''\beta3～\mathcal{N}(0，10)''')
    st.latex(r'''\theta=\alpha + \beta1 \times location + \beta3 \times titles + \beta3 \times bottons''')
    st.latex(r'''\sigma(t) = \frac{1}{1 + \exp (-t)}''')
    st.latex(r'''Observe～\binom{N}{\sigma(\theta)}''')
    st.latex(r'''\text{Modeling}''')

    with pm.Model() as model:
        alpha = pm.Normal('alpha', mu=0, sigma=10)
        beta = pm.Normal('beta', mu=0, sigma=10, shape=3)
        comb = alpha + beta[0] * z[:, 0] + beta[1] * z[:, 1] + beta[2] * z[:, 2]
        theta = pm.Deterministic('theta', 1/(1+pm.math.exp(-comb)))
        obs = pm.Binomial('obs', p=theta, n=list(n), observed=cv)
        trace = pm.sample(5000, chains=2)
        #pm.plot_trace(trace, compact=True)
        st.dataframe(pm.summary(trace))
    
    # 施策ごとの有効性
    t = trace['beta'][:, 0]
    m = trace['beta'][:, 1]
    b = trace['beta'][:, 2]
    
    index = ['Effectiveness of Text', 'Effectiveness of Map', 'Effectiveness of Botton']
    result_list = [(t > 0).mean(), (m > 0).mean(), (b > 0).mean()]
    
    for i in range(8):
        for j in range(8):
            result = (trace['theta'][:, i] - trace['theta'][:, j] > 0).mean()
            index.append('Ration of {i}th Theta minus {j}th Theta'.format(i=i, j=j))
            result_list.append(result)
            
    df = pd.DataFrame(
    result_list,
    columns = ['Effectiveness'],
    index=index)
    
    st.latex(r'''\text{Result of hypothesis}''')
    st.table(df)
    
    pm.summary(trace).to_csv('./modeling.csv') 
            

def ShowBest():
    df = pd.read_csv('./modeling.csv')
    idx_mean_max = df.iloc[4:, :]['mean'].idxmax()
    nums = [0, 1]
    arr = np.zeros(3)
    combinations = itertools.product(nums, repeat=3)
    combinations = [list(c) for c in combinations]
    
    mean_max_combination = combinations[idx_mean_max]
    title = mean_max_combination[0]
    location = mean_max_combination[1]
    botton = mean_max_combination[2] 
    
    st.latex(r'''\text{Visualizing UI which has highest mean of } \theta''')
    visualize(title, location, botton)
    
            