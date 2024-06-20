import streamlit as st
from recommend_anime_random_forest import recommend_anime_random_forest
from recommend_anime_knn import recommend_anime_knn
from recommend_anime_sentiment import recommend_anime_sentiment

# Menú principal
def main():
    menu = st.sidebar.selectbox("Seleccione una opción:", ["Inicio",
                                                           "Recomendar Anime (Random Forest)", 
                                                           "Recomendar Anime (KNN)",
                                                           "Recomendar Anime por Estado de Ánimo"])

    if menu == "Inicio":
        st.image("img/logo.png", use_column_width=True)
    elif menu == "Recomendar Anime (Random Forest)":
        recommend_anime_random_forest()
    elif menu == "Recomendar Anime (KNN)":
        recommend_anime_knn()
    elif menu == "Recomendar Anime por Estado de Ánimo":
        recommend_anime_sentiment()

if __name__ == "__main__":
   main()
