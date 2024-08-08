import streamlit as st
import requests 
import json

if __name__ == "__main__":
    URL = "http://localhost:5000/search/"
    query = st.text_input(label="Input the Search Query")
    if query:
        resonpse = requests.get(url=URL,
                                params={"query":query}).json()['results']

        for title,url in resonpse:
            st.write(f"[{title}]({url})") 
