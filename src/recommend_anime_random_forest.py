import streamlit as st
import joblib
import pandas as pd

# Cargar el dataset
data = pd.read_csv("models/scraping_animeList.csv")

def recommend_anime_random_forest():
   # Cargar el modelo preentrenado
   modelo_ = joblib.load("models/model.pkl")

   # Sección para seleccionar la cantidad de RAM
   Type = st.selectbox(
      'Seleccione el tipo',
      ('TV', 'Movie', 'ONA', 'OVA', 'Special', 'TV Special')
   )

   # Sección para seleccionar el sistema operativo
   Source = st.selectbox(
      'Seleccione el Source',
      ('Manga', 'Original', 'Visual novel', 'Light novel', 'Web novel', 'Game', 'Other', 'Novel', '4-koma manga', 
       'Web manga', 'Book', 'Pivture book', 'Mixed media', 'Card game', 'Music', 'Radio')
   )

   # Sección para seleccionar la arquitectura de bits
   Rating = st.selectbox(
      'Seleccione el Rating',
      ('PG-13 - Teens 13 or older', 
       'G - All Ages',
       'PG - Children',
       'Rx - Hentai',
       'R - 17+ (violence & profanity)',
       'R+ - Mild Nudity')
   )

   # Línea divisoria para mejorar la presentación
   # st.divider()
   st.markdown("")

   if st.button("Obtener Recomendaciones"):
      # Crear un DataFrame con las selecciones del usuario
      X = pd.DataFrame([[Type, Source, Rating]],
                              columns=['Type', 'Source', 'Rating'])

      # Renombrar columnas para mayor claridad
      X = X.rename(columns={'Type': 'Type', 'Source': 'Source', 'Rating': 'Rating'})

      X = X[['Type', 'Source', 'Rating']]

      X = X.replace({'TV': 1, 'Movie': 2, 'ONA': 3, 'OVA': 4, 'Special': 5, 'TV Special': 6})
      X = X.replace({'Manga': 1, 'Original': 2, 'Visual novel': 3, 'Light novel': 4, 'Web novel': 5, 
                     'Game': 6, 'Other': 7, 'Novel': 8, '4-koma manga': 9, 'Web manga': 10, 
                     'Book': 11, 'Pivture book': 12, 'Mixed media': 13, 'Card game': 14, 
                     'Music': 15, 'Radio': 16, 'Unknown': 17})
      X = X.replace({'PG-13 - Teens 13 or older': 1, 'G - All Ages': 2, 'PG - Children': 3, 
                     'Rx - Hentai': 4, 'R - 17+ (violence & profanity)': 5, 'R+ - Mild Nudity': 6})

      # Realizar predicciones utilizando el modelo cargado
      prediction = modelo_.predict(X)[0]

      # Filtrar animes con puntajes similares
      similar_animes = data[(data['Score'] >= prediction - 1) & (data['Score'] <= prediction + 1)]

      # Seleccionar tres animes aleatorios de la lista
      recommended_animes = similar_animes.sample(5)

      # Mostrar el resultado al usuario
      st.text(f"This instance is a {prediction}")

      # Mostrar la lista de animes recomendados al usuario
      st.text("Animes recomendados:")
      for index, anime in recommended_animes.iterrows():
         col1, col2 = st.columns(2)
         with col1:
            st.image(anime['Image_URL'], caption=anime['Title'], width=200)
         with col2:
            st.write(f"**Título:** {anime['Title']}", style={"margin-left": "20px"})
            # Verificar si Demographic está vacío o nulo
            if pd.isna(anime['Demographic']) or anime['Demographic'] == '':
               st.write(f"**Demographic:** Unknown")
            else:
               st.write(f"**Demographic:** {anime['Demographic']}")
            st.write(f"**Studios:** {anime['Studios']}")
            st.write(f"**Popularity:** {anime['Popularity']}")
            st.write(f"**Favorites:** {anime['Favorites']}")
            st.write(f"**Genres:** {anime['Genres']}")
            st.write(f"**Year:** {anime['Year']}")
            st.write(f"**Score:** {anime['Score']}")
         st.write("")
         st.write("")
         st.write("")
         st.write("")