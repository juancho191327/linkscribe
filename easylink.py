import streamlit as st
import pandas as pd
import streamlit_option_menu
from streamlit_option_menu import option_menu
from PIL import Image
import psycopg2
from datetime import datetime
import random
import requests
import json
import os
import database 
from google.cloud import firestore
#LOGIN
import streamlit as st
from firebase_admin import firestore
from firebase_admin import auth
from fastapi import FastAPI, Request

#Conexion al puerto 8080
API_ENDPOINT = os.environ.get("API_ENDPOINT", "http://localhost:8080")

#Crea una nueva variable para contener los resultados del modelo.
if 'dic' not in st.session_state:
    st.session_state.dic = {}

#Titulo del website
st.set_page_config(page_title="LinkScribe")

# Autenticar a Firestore con la JSON-key.
db = firestore.Client.from_service_account_json("firestore-key.json")

#inicializar FASTAPI
app = FastAPI()
database.funcion_a_ejecutar()

#prediccion
def call_api_predict_method(link):
    request_data = [{"link": link}]
    
    request_data_json = json.dumps(request_data)
    headers = {'Content-Type': 'application/json'}
    
    print(request_data_json)
    predict_method_endpoint = f"{API_ENDPOINT}/scrapper/predict"
    response = requests.request("POST",predict_method_endpoint , headers=headers, data=request_data_json)
    response_json = response.json()
    label = response_json
    return label

#establecer parámetros para volver a la pantalla de inicio de sesión
def t():
        st.session_state.signout = False
        st.session_state.signedout = False   
        st.session_state.username = ''

#estructura primaria de la APP
def estructure():
        
    #titulo
    st.markdown("<h1 style='text-align: center;'>LinkScribe APP</h1>", unsafe_allow_html=True)
    st.image("machine-learning.png", caption='By: XYZ')
    
    st.sidebar.subheader("Conexion de usuario")
    #descripcion del modelo
    st.sidebar.write("Conexion exitosa, bienvenido a LinkScribe.(DEMO version)")
    st.sidebar.write('Nombre: ',st.session_state.username)
    st.sidebar.write('Email: ',st.session_state.useremail)
    st.sidebar.button('Sign out', on_click=t) 
    #Crear tablas
    tabs = st.tabs(["LINK", "BUSQUEDAS",])
    return(tabs)

#clasifficasion usando nuestro modelo
def LinkScribe(tabs,user):
    label=[]
    with tabs[0]:
        
        #contenido subpagina
        st.markdown("<h1 style='text-align:;'>Pega un nuevo link:</h1>", unsafe_allow_html=True)
        
        #link
        link = st.text_input("")
        submit_button = st.button("Analizar link",key = 2)

        #check
        if submit_button:
            if link:
                      
                label=call_api_predict_method(link)
                
                st.subheader("Imagen de pagina:")
                st.write("")
                st.image(label[3], caption="Image caption")

                values = list(label)
                st.subheader("Titulo de la web:")
                st.write(str(label[2]).upper())

                st.subheader("Descripcion:")
                st.write(str(label[1]))

                st.subheader("Categoria:",)
                st.write(str(label[0]).upper()) 
                
                st.subheader("LINK:")
                st.write(link) 
                
                #Dictionario con resutados
                mi_diccionario = {
                                'categoria': label[0],
                                'descripcion': label[1],
                                'titulo':label[2],
                                'imagen':label[3],
                                'link':link
                                }
                
                st.session_state.dic = mi_diccionario

                #Guardar en database de sesion actual
                database.guardar_datos(st.session_state.dic,user)
                st.balloons()
            else:
                # Mensaje de error
                st.markdown("<p style='color: red;'>Ingresa una URL</p>", unsafe_allow_html=True)

#Buscar datos
def baseDatos(tabs,user):
     with tabs[1]:
        database.buscar_datos(user)

def app():

    #Chekear usuario
    if 'username' not in st.session_state:
        st.session_state.username = ''
    if 'useremail' not in st.session_state:
        st.session_state.useremail = ''

    #Logs in, holds the username and email and set the state as signed in
    def f(): 
        try:
            user = auth.get_user_by_email(email)
            st.session_state.username = user.uid
            st.session_state.useremail = user.email
            
            global Usernm
            Usernm=(user.uid)
            
            st.session_state.signedout = True
            st.session_state.signout = True    
	        
        except: 
            st.warning('Login Fallida')

    #Inicializar ariables de sing out
    if "signedout"  not in st.session_state:
        st.session_state["signedout"] = False
    if 'signout' not in st.session_state:
        st.session_state['signout'] = False    
        
    #Si ningún usuario ha iniciado sesión, solicite la información de inicio de sesión.
    if  not st.session_state["signedout"]:
        st.title('Bienvenido a LinkScribe:violet[(DEMO)]')
        st.markdown("By **XYZ** *innovation and design*.")
        
        choice = st.selectbox('Login/Signup',['Login','Sign up'])
        email = st.text_input('Email')
        password = st.text_input('Contraseña',type='password')
        
        #Sign up 
        if choice == 'Sign up':
            username = st.text_input("Ingresa tu usuario")
            user_id = username
            if st.button('Crear mi cuenta',key = 1):
                user = auth.create_user(email = email, password = password,uid=username)
                
                st.success('Cuenta creada!')
                st.markdown('Inicia sesion usando tu Email y Contraseña')
                st.balloons()

        else:
            #boton Login    
            st.button('Login', on_click=f)
            
            
    if st.session_state.signout:
                
                #estructura
                tabs=estructure()
                
                #modelo de predicciones   
                LinkScribe(tabs,st.session_state.username)
                
                # Contenido conexion con base de datos
                baseDatos(tabs,st.session_state.username)
                
                
if __name__ == '__main__':
    app()