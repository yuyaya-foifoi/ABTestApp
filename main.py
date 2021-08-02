import streamlit as st
from src.functions import HomePage, Modeling, ShowBest


def main():
    activities = ["Home", "Modeling", "BestUI"]
    choice = st.sidebar.selectbox("Sidebar", activities)
    
    if choice == 'Home':
        HomePage()
        
    if choice == 'Modeling':
        Modeling()
        
    if choice == 'BestUI':
        ShowBest()
        


if __name__ == "__main__":
    main()