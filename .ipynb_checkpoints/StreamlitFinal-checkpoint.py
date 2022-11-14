import pandas as pd
import numpy as np
import streamlit as st
from datetime import time
from PIL import Image
import sklearn
from sklearn.neighbors import NearestNeighbors


# Import the datasets 
kids = pd.read_csv('https://raw.githubusercontent.com/Sebastiao199/Project3MRS/main/6_TablesForStreamlit/kids_imdb_rt1.csv')
directors = pd.read_csv('https://raw.githubusercontent.com/Sebastiao199/Project3MRS/main/6_TablesForStreamlit/directors_rt_imdb1.csv')
genre = pd.read_csv('https://raw.githubusercontent.com/Sebastiao199/Project3MRS/main/6_TablesForStreamlit/GenreQuestion.csv')
actor = pd.read_csv('https://raw.githubusercontent.com/Sebastiao199/Project3MRS/main/6_TablesForStreamlit/bestactors.csv')
rec_sys = pd.read_csv('https://raw.githubusercontent.com/Sebastiao199/Project3MRS/main/2_MachineLearning/movies_reco_system.csv')

add_selectbox = st.sidebar.selectbox(
    "Select the topic you want",
    ['Introduction', 'Directors & Genres', "Actors & Actresses", "Kids & Family", 'Recommendation System'])

if add_selectbox == 'Introduction':

    image1 = Image.open('Documents/GitHub/Project3MRS/8_Pictures/intro_picture.jpg')
    #image1 = image1.resize((1200, 800))
    #st.image(image1)


elif add_selectbox == 'Directors & Genres':


    # Created the interval year slider 
    date_range = st.slider('Choose the year interval:', 1900, 2022, value = (1990, 2000))

    #image_director = Image.open('director_picto.png')
    #image_director = image_director.resize((150, 150))
    #st.image(image_director)


    # DIRECTORS : Question about the best movies per director 

    st.subheader('What are the best movies of your favourite director?')

    directors['Rotten Tomatoes rating'] = directors['Rotten Tomatoes rating']/10

    options_dir = st.selectbox('Choose the director:', directors['Director name'].unique())
                                    
    df_dir = directors[(directors['Director name']==options_dir) & (directors['Year'] >= date_range[0]) & (directors['Year'] <= date_range[1])]

    #st.table(df_dir[['Movie title','Year','IMDb rating', 'Rotten Tomatoes rating']].sort_values(by=['IMDb rating','Year', 'Rotten Tomatoes rating'], ascending=False))

    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df_dir[['Movie title','Year','IMDb rating', 'Rotten Tomatoes rating']].sort_values(by=['IMDb rating','Year', 'Rotten Tomatoes rating'], ascending=False).head(5).style.format({'IMDb rating': '{:.1f}', 'Rotten Tomatoes rating': '{:.1f}'}))

    # GENRE: Question about the genre 

    #image_genre = Image.open('genre_picto.png')
    #image_genre = image_genre.resize((150, 150))
    #st.image(image_genre)

    st.subheader('What are the top 5 movies per genre and best reviews?')

    options_genre = st.selectbox('Choose the genre you prefer:', genre['Genre'].unique())

    df_genre = genre[(genre['Genre']==options_genre) & (genre['Year'] >= date_range[0]) & (genre['Year'] <= date_range[1])]

    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)

    st.table(df_genre[['Movie title','Year','IMDb rating', 'Rotten Tomatoes rating', 'Genre']].sort_values(by=['IMDb rating'], ascending=False).head(5).style.format({'IMDb rating': '{:.1f}', 'Rotten Tomatoes rating': '{:.1f}'}))


elif add_selectbox == "Actors & Actresses":


    #image_director = Image.open('actors_picto.png')
    #image_director = image_director.resize((150, 150))
    # st.image(image_director, width = 150)
    #st.image(image_director)


        # ACTORS: Question about the actors 
    st.subheader('What are the best Actors / Actresses?')

    actor['category'] = actor['category'].str.title()

    options_actors = st.selectbox('Choose the Actor / Actress:', actor['category'].unique())

    df_actor = actor[(actor['category']==options_actors)].head(10)

    st.table(df_actor[['Staff name','IMDb rating', 'Nb movies', 'Ranking']].sort_values(by=['Ranking'], ascending=False).style.format({'IMDb rating': '{:.1f}', 'Ranking': '{:.1f}'}))

    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)


elif add_selectbox == "Kids & Family":

    date_range = st.slider('Choose the year interval:', 1900, 2022, value = (1990, 2000))


    # KIDS: Question about the best movies for kids 

    st.subheader('What are the best movies for kids?')

    #st.subheader('*Where are the orders going to?*')

    options_kids = st.selectbox('Choose the studio:', kids['Studio'].unique())
                                
    df_mov = kids[(kids['Studio']==options_kids) & (kids['Year'] >= date_range[0]) & (kids['Year'] <= date_range[1])]#[['movie_title','tomatometer_rating']]
    #df_mov.round({'IMDb rating': 2, 'Rotten Tomatoes rating': 2})
    #df_mov.round(2)
    #st.table(df_mov[['Movie Title', 'Year', 'Studio', 'IMDb rating', 'Rotten Tomatoes rating']].sort_values(by='Year', ascending=False))

    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    st.table(df_mov[['Movie Title', 'Year', 'Studio', 'IMDb rating', 'Rotten Tomatoes rating']].sort_values(by=['IMDb rating','Year', 'Rotten Tomatoes rating'], ascending=False).head(5).style.format({'IMDb rating': '{:.1f}', 'Rotten Tomatoes rating': '{:.1f}'}))

    #image_kids = Image.open('child_pictures.png')
    #image_kids = image_kids.resize((600, 400))
    # st.image(image_kids, width = 150)
    #st.image(image_kids)

else:
    st.subheader('What is your favourite movie?')
    
    rec_sys['Year'] = rec_sys['startYear_x'].astype(str)
    rec_sys['title_year'] = rec_sys['primaryTitle']+' '+rec_sys['Year']
    
    options_reco = st.selectbox('Choose a movie:', rec_sys['title_year'].unique())
    
    X=rec_sys[['startYear_st', 'runtimeMinutes_st', 'averageRating_st', 'numVotes_st', 'action', 'adult', 'adventure', 'animation', 'biography',
       'comedy', 'crime', 'documentary', 'drama', 'family', 'fantasy', 'fi',
       'game', 'history', 'horror', 'music', 'musical', 'mystery', 'news',
       'reality', 'romance', 'sci', 'short', 'show', 'sport', 'talk',
       'thriller', 'tv', 'war', 'western']]     

    model = NearestNeighbors(n_neighbors=6)
    model.fit(X)
    
    array_1, array_2 = model.kneighbors(rec_sys.loc[rec_sys['title_year'] == options_reco, ['startYear_st', 'runtimeMinutes_st', 'averageRating_st', 'numVotes_st', 'action', 'adult', 'adventure', 
    'animation', 'biography','comedy', 'crime', 'documentary',
    'drama', 'family', 'fantasy', 'fi','game', 'history', 'horror', 'music', 'musical', 'mystery', 'news',
    'reality', 'romance', 'sci', 'short', 'show', 'sport', 'talk','thriller', 'tv', 'war', 'western']])
    
    index_array = array_2
    index_list = index_array.flatten().tolist() #to appear in vertical
    index_df = pd.DataFrame(index_list).rename(columns={0:'Index_array'})
    
    rec_sys.drop(['level_0'], axis=1, inplace=True)
    rec_sys.reset_index(inplace=True)
    Output_final=index_df.merge(rec_sys, how='left', left_on='Index_array', right_on='level_0')
    
    hide_table_row_index = """
                <style>
                thead tr th:first-child {display:none}
                tbody th {display:none}
                </style>
                """
    st.markdown(hide_table_row_index, unsafe_allow_html=True)
    Output_final = Output_final.rename(columns = {'averageRating':'IMDb rating', 'primaryTitle':'Movie title',
                                                  'genres_x':'Genres'})

    st.table(Output_final[['Movie title', 'Genres', 'IMDb rating']].iloc[1:6].style.format({'IMDb rating': '{:.1f}'}))