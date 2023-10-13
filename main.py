import streamlit as st
from streamlit_option_menu import option_menu
import frontend.page as page

class MultiApp:

    def __init__(self):
        self.apps = []

    def add_app(self, title, func):

        self.apps.append({
            "title": title,
            "function": func
        })

    def run():
        page.app()          
             
    run()            
         
