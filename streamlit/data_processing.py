import pandas as pd
import numpy as np
import pickle
import streamlit as st
from collections import defaultdict, OrderedDict

with open('topGenreDict.pkl', 'rb') as f:
    topGenreDict = pickle.load(f)
with open('genre_index_dict.pkl', 'rb') as f:
    genre_index_dict = pickle.load(f)
with open('topActorDict.pkl', 'rb') as f:
    topActorDict = pickle.load(f)
with open('actor_rank_dict.pkl', 'rb') as f:
    actor_rank_dict = pickle.load(f)
with open('top_100_actors_set.pkl', 'rb') as f:
    top_100_actors_set = pickle.load(f)
with open('topDirectorDict.pkl', 'rb') as f:
    topDirectorDict = pickle.load(f)
with open('top_25_directors_set.pkl', 'rb') as f:
    top_25_directors_set = pickle.load(f)
with open('director_rank_dict.pkl', 'rb') as f:
    director_rank_dict = pickle.load(f)
with open('topWriterDict.pkl', 'rb') as f:
    topWriterDict = pickle.load(f)
with open('top_25_writers_set.pkl', 'rb') as f:
    top_25_writers_set = pickle.load(f)
with open('writer_rank_dict.pkl', 'rb') as f:
    writer_rank_dict = pickle.load(f)
with open('topCompanyDict.pkl', 'rb') as f:
    topCompanyDict = pickle.load(f)
with open('top_25_companies_set.pkl', 'rb') as f:
    top_25_companies_set = pickle.load(f)
with open('company_rank_dict.pkl', 'rb') as f:
    company_rank_dict = pickle.load(f)

actors_list = list(topActorDict.keys())
directors_list = list(topDirectorDict.keys())
writers_list = list(topWriterDict.keys())
genres_list = list(topGenreDict.keys())
companies_list = list(topCompanyDict.keys())

def getGenreRank(genres, genre_index_dict):
    total_rank = sum(genre_index_dict[g] for g in genres)
    rank = total_rank / len(genres)
    return rank

def calculate_actor_ranking(actors):
    if isinstance(actors, list):
        rankings = [actor_rank_dict[actor] for actor in actors]
        return sum(rankings) / len(rankings) if len(rankings) > 0 else len(topActorDict) + 1
    else:
        return len(topActorDict) + 1

def count_top_100_actors(cast):
    return sum(1 for actor in cast if actor in top_100_actors_set)

def has_top_25_directors(director):
    return 1 if director in top_25_directors_set else 0

def has_top_25_writers(writer):
    return 1 if writer in top_25_writers_set else 0

def has_top_25_companies(companies):
    return 1 if any(company in top_25_companies_set for company in companies) else 0

def calculate_director_ranking(director):
    if isinstance(director, str):
        return director_rank_dict.get(director, len(topDirectorDict) + 1)
    else:
        return len(topDirectorDict) + 1

def calculate_writer_ranking(writer):
    if isinstance(writer, str):
        return writer_rank_dict.get(writer, len(topWriterDict) + 1)
    else:
        return len(topWriterDict) + 1

def calculate_company_ranking(companies):
    if isinstance(companies, list):
        rankings = [company_rank_dict[company] for company in companies]
        return sum(rankings) / len(rankings) if len(rankings) > 0 else len(topCompanyDict) + 1
    else:
        return len(topCompanyDict) + 1
    
languages = [
    "English",        # en
    "Hindi",          # hi
    "French",         # fr
    "Russian",        # ru
    "Japanese",       # ja
    "Spanish",        # es
    "Tamil",          # ta
    "Chinese",        # zh
    "Korean",         # ko
    "German",         # de
    "Italian",        # it
    "Chinese",        # cn (used for Simplified Chinese)
    "Portuguese",     # pt
    "Polish",         # pl
    "Dutch",          # nl
    "Danish",         # da
    "Swedish",        # sv
    "Indonesian",     # id
    "Romanian",       # ro
    "Greek",          # el
    "Norwegian Bokmål", # nb
    "Norwegian",      # no
    "Hebrew",         # he
    "Telugu",         # te
    "Malayalam"       # ml
]

countries = [
    "United States", "India", "France", "Russia", "Japan", "Spain",
    "China", "Germany", "Italy", "Portugal", "Poland", "Netherlands",
    "Denmark", "Sweden", "Indonesia", "Romania", "Greece", "Norway",
    "Israel", "Brazil", "Mexico"
]

def add_country():
    st.session_state.country_list.append("")

def get_season(month):
    if month in ["December", "January", "February"]:
        return "Winter"
    elif month in ["March", "April", "May"]:
        return "Spring"
    elif month in ["June", "July", "August"]:
        return "Summer"
    elif month in ["September", "October", "November"]:
        return "Autumn"
    
def check_usa(selected_countries):
    return 1 if "United States" in selected_countries else 0

with open('encoder.pkl', 'rb') as f:
    encoder = pickle.load(f)