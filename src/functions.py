import streamlit as st
import pydeck as pdk


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