import pandas as pd
from pandas import DataFrame
import json
import ast

def getData():
    print('Reading meta data csv.')
    mainDS = pd.read_csv("movies_metadata.csv")
    mainDS = mainDS.drop([19730,29503,35587])
    mainDS.drop(['adult','homepage','original_language','overview','spoken_languages','status','tagline','original_title','video', 'poster_path'], axis=1, inplace = True)
    return mainDS

def transformCollection(mainDS):
    # Convert if belongs to a collection to a boolean value.
    print('Transforming the collections column.')
    collections = mainDS['belongs_to_collection']
    isCollection = ~collections.isnull()
    mainDS['belongs_to_collection'] = isCollection
    return mainDS

def getUniqueAndCleanGenres(mainDS):
    print('Cleaning Genres and getting unique list.')
    genres = mainDS['genres'].tolist()
    genreList = []
    cleanGenres = []
    for rawGenre in genres:
        cleanGenre = ast.literal_eval(rawGenre)
        genreString = ''
        for element in cleanGenre:
            genreList.append(element['name'])
            genreString = genreString + element['name'] + ','
        cleanGenres.append(genreString.strip(','))
    mainDS['genres'] = cleanGenres 
    # Set gets unique values and then convert back into list
    uniqueGenres = list(set(genreList))
    return uniqueGenres, mainDS

def castIdToInt(mainDS):
    print('Converting ID to integer data type.')
    ids = mainDS['id'].values
    idList = []
    index = 0
    for item in ids:
        try:
            idList.append(int(item))
            index += 1
        except:
            print(index)
            index += 1
    mainDS['id'] = idList
    return mainDS

def getCastData(mainDS):
    print('Reading cast data. Merging with main dataset.')
    creditData = pd.read_csv('act_dirDS.csv')
    mergedDS = mainDS.merge(creditData, how = 'inner', left_on = 'id', right_on = 'id')

    directors = mergedDS['director'].tolist()
    cleanDirectors = []
    for directorString in directors:
        director = directorString.strip('[]')
        director = director.replace("'", "")
        cleanDirectors.append(director)
    mergedDS['director'] = cleanDirectors

    actors = mergedDS['actors'].tolist()
    cleanActors = []
    for actorString in actors:
        actor = actorString.strip('[]')
        actor = actor.replace("'", "")
        cleanActors.append(actor)
    mergedDS['actors'] = cleanActors
    return mergedDS

def removeNulls(mainDS):
    print('Removing nulls and 0 values.')
    mainDS.dropna(axis = 0, how = 'any', inplace = True)
    mask1 = mainDS['budget'] != 0
    mask2 = mainDS['revenue'] != 0
    mainDS = mainDS[mask1 & mask2]
    mainDS = mainDS.reset_index(drop = True)
    return mainDS

if __name__ == "__main__":
    mainDS = getData()
    mainDS = transformCollection(mainDS)
    uniqueGenres, mainDS = getUniqueAndCleanGenres(mainDS)
    mainDS = castIdToInt(mainDS)
    mainDS = getCastData(mainDS)
    mainDS = removeNulls(mainDS)
    mainDS = mainDS[mainDS['budget']!=0]
    mainDS = mainDS.dropna(axis = 0, how = 'any')
    mainDS.to_csv('mergedData.csv', index = False)
    print('Completed Script. Wrote merged file to csv.')
