import streamlit as st
from google.cloud import firestore
import random
import string
import json
from google.oauth2 import service_account

db = firestore.Client.from_service_account_json("firestore-key.json")

def guardar_datos(dato,user):

    name = ''.join(random.choices(string.ascii_letters, k=10))

    doc_ref = db.collection("users").document(user)
    doc_ref.set({
            name:dato
                }, merge=True)

def buscar_datos(user):
    
    user_ref = db.collection("users").document(user)
    user_Data = user_ref.get()
    user2 = user_Data.to_dict()

    if user2 is not None:
        #busqueda por título
        st.header("Titulo")
        filtro_titulo = st.text_input("Ingresa titulo:")
        
        categorias = ['Adult', 'Business/Corporate', 'Computers and Technology',
       'E-Commerce', 'Education', 'Food', 'Forums', 'Games',
       'Health and Fitness', 'Law and Government', 'News', 'Photography',
       'Social Networking and Messaging', 'Sports', 'Streaming Services',
       'Travel']

        #busqueda por categoría
        st.header("Categoria")
        filtro_categoria = st.multiselect("Categorias", categorias)

        #Filtrar busqueda
        datos_filtrados = [
            dato for dato_id, dato in user2.items() 
            if filtro_titulo.lower() in dato.get("titulo", "")
            and (not filtro_categoria or dato.get("categoria", "") in filtro_categoria)
        ]


        if datos_filtrados:
            #mostrar busqueda
            st.header("Filtered data")
            count=10
            for item in datos_filtrados:
                if st.button(f"Mostrar descripcion de {item['titulo']}, en la categoria: {item['categoria']}",key=count ):
                    st.subheader("Imagen:")
                    st.image(item['imagen'])
                    st.subheader("Titulo:")
                    st.write(item['titulo'])
                    st.subheader("Descripcion:")
                    st.write(item["descripcion"])
                    st.subheader("Categoria:")
                    st.write(item['categoria'])
                    st.subheader("LINK:")
                    st.write(item['link'])
                count+=1
            
        else:    
            st.warning("El usuario aun no ha ingresado paginas web.")
        
        
    else:
        st.warning("El usuario aun no ha ingresado paginas web.")

import os
import firebase_admin
from firebase_admin import credentials

import functools

def run_once(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        if not wrapper.has_run:
            func(*args, **kwargs)
            wrapper.has_run = True
    wrapper.has_run = False
    return wrapper

@run_once
def funcion_a_ejecutar():
    cred = credentials.Certificate("firestore-key.json")
    firebase_admin.initialize_app(cred)
