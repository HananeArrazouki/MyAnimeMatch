import streamlit as st
from recommend_anime_random_forest_ import recommend_anime_random_forest
from recommend_anime_knn import recommend_anime_knn

# Menú principal
def main():
    menu = st.sidebar.selectbox("Seleccione una opción:", ["Recomendar Anime (Random Forest)", "Recomendar Anime (KNN)"])

    if menu == "Recomendar Anime (Random Forest)":
        recommend_anime_random_forest()
    elif menu == "Recomendar Anime (KNN)":
        recommend_anime_knn()

if __name__ == "__main__":
   main()
