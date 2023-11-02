
import pandas as pd
from fastapi import FastAPI

app = FastAPI()


#Loanding flat files to be used by the functions
maxplaytime_year_by_genre = pd.read_csv("../Data/maxplaytime_year_by_genre.csv")
maxplaytime_by_user_by_genre = pd.read_csv("../Data/maxplaytime_by_user_by_genre.csv")
games_recommended_by_year = pd.read_csv("../Data/games_recommended_by_year.csv")
more_not_recommended_by_users = pd.read_csv("../Data/games_not_recommended_by_year.csv")
sentiment_analisis = pd.read_csv('../Data/sentiment_analysis_df.csv')
database_recomendations = pd.read_csv('../Data/database_recomendations.csv')


@app.get('/PlayTimeGenre/{genre}')
def PlayTimeGenre(genre: str):
    '''Return the the release year with more played hours for the entered genre'''
    # Get the corresponding year based on the gender
    year = maxplaytime_year_by_genre.loc[maxplaytime_year_by_genre['genres'].str.lower() == genre.lower(), 'release_year'].values
    if len(year) == 0:
        return {f'Videogame release year for the genre {genre}': 'no encontrado'}
    else:
        return {f'Videogame release year for the genre {genre}': str(year[0])}

@app.get('/UserForGenre/{genre}')
def UserForGenre(genre: str):
    '''Return the user who accumulates the most hours played for the given genre and a list of the accumulation of hours played per year.'''
    # Get the corresponding user based on the gender
    user = maxplaytime_by_user_by_genre.loc[maxplaytime_by_user_by_genre['genres'].str.lower() == genre.lower(), 'user_id'].values
    if len(user) == 0:
        return {f'User with more hours played for Gen  {genre}': 'no encontrado'}
    else:
        return {f'User with more hours played for Gen  {genre}': str(user[0])}

@app.get('/UserForGenre/{year}')
def UsersRecommend( year : int ): 
    '''Returns the top 3 recommended games by users for the given year (reviews.recommend = True and positive/neutral reviews).'''
    #Filtering by year
    filtered_df = games_recommended_by_year[games_recommended_by_year['posted_year'] == year]
    #Sorting by  'times_recommended' in a descending order
    sorted_df = filtered_df.sort_values(by='times_recommended', ascending=False)
    #Selecting the 3 first records
    top_3_games = sorted_df.head(3)    
    lista_de_diccionarios = top_3_games[['title']].to_dict(orient='records')
    return lista_de_diccionarios

@app.get('/UsersNotRecommend/{year}')
def UsersNotRecommend( year : int ): 
    '''Returns the top 3 recommended games by users for the given year (reviews.recommend = True and positive/neutral reviews).'''
    #Filtering by year
    filtered_df = more_not_recommended_by_users[more_not_recommended_by_users['posted_year'] == year]
    #Sorting by  'times_recommended' in a descending order
    sorted_df = filtered_df.sort_values(by='times_not_recommended', ascending=False)
    #Selecting the 3 first records
    top_3_games = sorted_df.head(3)    
    lista_de_diccionarios = top_3_games[['title']].to_dict(orient='records')
    if len(lista_de_diccionarios) == 0:
        return []
    else:
        return lista_de_diccionarios
    
@app.get('/sentiment_analysis/{year}')
def sentiment_analysis(year: int):
    '''Ingresa año a consultar, para retornar la Cantidad de reseñas categorizados por sentimiento'''
    Cantidad = sentiment_analisis[sentiment_analisis['year']==year]['sentiment'].to_list()[0]
    return Cantidad

@app.get('/recomendacion_usuario/{id}')
def recomendacion_usuario(id: str):
    '''Ingresa Id de usuario para retornar los juegos recomendados basado en '''
    Recomendations = database_recomendations[database_recomendations['user_id']==id]['recomendations'].to_list()[0]
    return Recomendations