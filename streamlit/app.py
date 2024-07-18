import streamlit as st
import pickle
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_absolute_percentage_error
from data_processing import *
from PIL import Image

# Custom CSS for styling
st.markdown("""
    <style>
        .main {
            background-color: #2c3e50;
            padding: 20px;
            color: #ecf0f1;
        }
        .stButton>button {
            background-color: #DC143C;
            color: white;
            border-radius: 10px;
            border: none;
            padding: 10px 20px;
            font-size: 16px;
            margin: 10px 0;
        }
        .stSlider>div[data-baseweb="slider"] {
            background: none;
        }
        .stSlider>div[data-baseweb="slider"] > div {
            background: #2c3e50;
        }
        .stSlider>div[data-testid="stTickBar"] > div {
            background: #2c3e50;
        }
        h1 {
            color: #DC143C;
            font-size: 36px;
            text-align: center;
        }
        h2, h3 {
            color: #DC143C;
        }
        .stSelectbox, .stTextInput, .stNumberInput, .stSlider, .stTextArea {
            margin-bottom: 10px;
        }
        .stMarkdown p {
            font-size: 18px;
            color: #ecf0f1;
        }
        .stRadio > div > label {
            color: #ecf0f1;
        }
    </style>
""", unsafe_allow_html=True)

# Header
st.markdown("<h1>Box Office Prediction Model \n</h1>", unsafe_allow_html=True)
image = Image.open("img/cine.jpg")
st.image(image, caption="", use_column_width=True)

# Function to load models
def load_model(path):
    with open(path, 'rb') as f:
        model = pickle.load(f)
    return model

# Load models
model_high = load_model('model_high.pkl')
model_low = load_model('model_low.pkl')

# Main layout
st.subheader("Select Budget Type")
budget_type = st.radio("Choose the budget type for your movie:", ("Low Budget (10M max.)", "High Budget"))

# Display corresponding slider based on budget type
if budget_type == "Low Budget (10M max.)":
    budget = st.slider("Select your movie budget:", min_value=50000, max_value=10000000, step=50000, value=50000)
    
else:
    budget = st.slider("Select your movie budget (in millions):", min_value=10, max_value=400, step=1, value=10)
    budget = budget * 1e6
    image = Image.open('img/gilito.jpeg')
    st.image(image, caption="Wow, I see you're going all out for your movie... I like that", use_column_width=True)

st.write("Selected budget:", int(budget))

# Use columns for inputs
col1, col2 = st.columns(2)

with col1:
    st.subheader("Select Runtime")
    runtime = st.slider("Select your movie runtime:", min_value=60, max_value=240, step=1, value=60)
    if runtime > 210:
        image = Image.open("img/maxresdefault.jpg")
        st.image(image, caption="Isn't that too long...?", use_column_width=True)
    st.write("Selected runtime:", runtime)

    st.subheader("Select Cast")
    if "selected_actors" not in st.session_state:
        st.session_state.selected_actors = []

    # Function to filter actors based on user input
    def filter_actors(input_text):
        return [actor for actor in actors_list if input_text.lower() in actor.lower()]

    # Text input for dynamic filtering
    input_text = st.text_input("Introduce an actor's name:")

    # Filter the list of actors based on the input
    filtered_actors = filter_actors(input_text)

    # Display the filtered suggestions in a select box if there are matches
    if filtered_actors:
        selected_actor = st.selectbox("Suggestions for actor/actress:", options=filtered_actors)
        if st.button("Add selected actor/actress"):
            if selected_actor not in st.session_state.selected_actors:
                st.session_state.selected_actors.append(selected_actor)

    lead_actor = st.session_state.selected_actors[0] if len(st.session_state.selected_actors) > 0 else None
    supporting_actor_1 = st.session_state.selected_actors[1] if len(st.session_state.selected_actors) > 1 else None
    supporting_actor_2 = st.session_state.selected_actors[2] if len(st.session_state.selected_actors) > 2 else None
    one_actor = st.session_state.selected_actors[3] if len(st.session_state.selected_actors) > 3 else None
    another_actor = st.session_state.selected_actors[4] if len(st.session_state.selected_actors) > 4 else None

    # Display the list of selected actors and their roles
    if st.session_state.selected_actors:
        st.subheader("Selected Actors/Actresses")
        st.markdown(f"**Lead Actor/Actress:** {lead_actor}")
        st.markdown(f"**Supporting Actor/Actress 1:** {supporting_actor_1}")
        st.markdown(f"**Supporting Actor/Actress 2:** {supporting_actor_2}")
        st.markdown(f"**Another Actor/Actress:** {one_actor}")
        st.markdown(f"**Another Actor/Actress:** {another_actor}")
    selected_cast = st.session_state.selected_actors

    actors_set = set(topActorDict.keys())
    list_set = set(selected_cast)
    intersection = actors_set.intersection(list_set)
    if len(intersection) > 2:
        image_path = 'img/rick.jpg'
        image = Image.open(image_path)
        st.image(image, caption="Hey, hey, hey, I think I know those actors, but I don't remember from where...", use_column_width=True)

with col2:
    st.subheader("Select Director")
    director_written = st.text_input("Introduce your director's name:")
    filtered_directors = [dir for dir in directors_list if director_written.lower() in dir.lower()]
    if filtered_directors:
        director = st.selectbox("Suggestions for director:", options=filtered_directors)
        st.write("You selected as director:", director)
    else:
        st.write("No matches found")

    st.subheader("Select Screenwriter")
    screenwriter_written = st.text_input("Introduce your screenwriter's name:")
    filtered_writers = [writ for writ in writers_list if screenwriter_written.lower() in writ.lower()]
    if filtered_writers:
        writer = st.selectbox("Suggestions for screenwriter:", options=filtered_writers)
        st.write("You selected as screenwriter:", writer)
    else:
        st.write("No matches found")

    st.subheader("Select Month Release")
    release_month = st.selectbox('Select the release month:', options=['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December'])
    st.write("You selected:", release_month)
    season = get_season(release_month)
    if season == 'Spring':
        image_path = 'img/primavera.jpg' 
        image = Image.open(image_path)
        st.image(image, caption="Allergies season, ugh...", use_column_width=True)
    elif season == 'Winter':
        image_path = "img/invierno.jpg" 
        image = Image.open(image_path)
        st.image(image, caption="What did you ask Santa for???", use_column_width=True)
    elif season == 'Summer':
        image_path = 'img/verano.jpg' 
        image = Image.open(image_path)
        st.image(image, caption="Alexa, play Bad Bunny! (8)", use_column_width=True)
    elif season == 'Autumn':
        image_path = 'img/otono.jpg' 
        image = Image.open(image_path)
        st.image(image, caption="I love Autumn...", use_column_width=True)


    st.subheader("Select Language")
    selected_language = st.selectbox("Select a language for your movie:", languages)
    st.write("You selected:", selected_language)

    st.subheader("Select Production Countries")

    if "country_list" not in st.session_state:
        st.session_state.country_list = [""]

    if not st.session_state.country_list:
        st.session_state.country_list.append("")

    st.session_state.country_list[0] = st.selectbox(
        "Country 1:", 
        options=countries, 
        key="country_0"
    )

    if st.button("Add a production country"):
        st.session_state.country_list.append("")

    for i in range(1, len(st.session_state.country_list)):
        st.session_state.country_list[i] = st.selectbox(
            f"Country {i+1}:",
            options=countries,
            key=f"country_{i}"
        )

    if st.session_state.country_list:
        selected_countries_str = ", ".join(country for country in st.session_state.country_list if country)
        st.markdown(f"**Production Countries:** {selected_countries_str}")

    selected_countries = [country for country in st.session_state.country_list if country]

    if "United States" in selected_countries:
        image_path = 'img/hollywood.jpg' 
        image = Image.open(image_path)
        st.image(image, caption="Here's for the ones who dream, foolish as they may seem...", use_column_width=True)

st.subheader("Select Genres")

if "genre_list" not in st.session_state:
    st.session_state.genre_list = [""] 

st.session_state.genre_list[0] = st.selectbox(
    "Genre 1:", 
    options=genres_list, 
    key="genre_0",
    index=0 
)

# Botón para añadir un nuevo género
if st.button("Add a genre"):
    st.session_state.genre_list.append("")

# Mostrar la lista de select boxes adicionales para los géneros
for i in range(1, len(st.session_state.genre_list)):
    st.session_state.genre_list[i] = st.selectbox(
        f"Genre {i+1}:", 
        options=genres_list, 
        key=f"genre_{i}",
        index=0
    )

# Mostrar la lista de géneros seleccionados
if st.session_state.genre_list:
    selected_genres_str = ", ".join(st.session_state.genre_list)
    st.markdown(f"**Genres:** {selected_genres_str}")

selected_genres = st.session_state.genre_list

if "Action" in selected_genres:
        image_path = 'img/accion.jpg'
        image = Image.open(image_path)
        st.image(image, caption="Put some explosions in there!", use_column_width=True)
if "Comedy" in selected_genres:
        image_path = 'img/comedia.jpg'  
        image = Image.open(image_path)
        st.image(image, caption="Put some gags!", use_column_width=True)
if "Science Fiction" in selected_genres:
        image_path = 'img/sci-fi.jpg' 
        image = Image.open(image_path)
        st.image(image, caption="I would like some robots too...", use_column_width=True)
if "Romance" in selected_genres:
        image_path = 'img/romance.jpg'  
        image = Image.open(image_path)
        st.image(image, caption="Gossip! I need to gossip!", use_column_width=True)
if "Horror" in selected_genres:
        image_path = 'img/horror.jpg'  
        image = Image.open(image_path)
        st.image(image, caption="Some horror would be amazing...", use_column_width=True)
if "Animation" in selected_genres:
        image_path = 'img/animatio.jpg'  
        image = Image.open(image_path)
        st.image(image, caption="And my movie will be animated. Animation is also a big genre!", use_column_width=True)

st.subheader("Select Production Companies")

if "selected_production_companies" not in st.session_state:
    st.session_state.selected_production_companies = []

def filter_companies(input_text):
    if not input_text:
        return companies_list 
    return [company for company in companies_list if input_text.lower() in company.lower()]

input_text = st.text_input("Introduce a production company name:")

# Obtener las compañías filtradas basadas en el texto ingresado
filtered_companies = filter_companies(input_text)

# Asegurarse de que haya una opción vacía para la selección inicial
options = filtered_companies

# Casilla de selección que se actualiza dinámicamente según el texto ingresado
if options:
    selected_company = st.selectbox("Suggestions for production company:", options=options, index=0)
else:
    selected_company = ""

# Botón para agregar la compañía seleccionada a la lista
if st.button("Add selected production company"):
    if selected_company and selected_company not in st.session_state.selected_production_companies:
        st.session_state.selected_production_companies.append(selected_company)

# Mostrar la lista de compañías seleccionadas
if st.session_state.selected_production_companies:
    selected_companies_str = ", ".join(st.session_state.selected_production_companies)
    st.markdown(f"**Production Companies:** {selected_companies_str}")

selected_companies = st.session_state.selected_production_companies

if "Marvel Studios" in selected_companies:
        image_path = 'img/marvel.jpg'  
        image = Image.open(image_path)
        st.image(image, caption="You're taking the easy way out, huh?", use_column_width=True)
if "Warner Bros. Pictures" in selected_companies:
        image_path = 'img/warner.jpg' 
        image = Image.open(image_path)
        st.image(image, caption="I like Warner to be honest, but it's not what it used to be.", use_column_width=True)
if "Universal Pictures" in selected_companies:
        image_path = 'img/universal.jpg'  
        image = Image.open(image_path)
        st.image(image, caption="You're going to colaborate with minions. Remember that.", use_column_width=True)

genre_rank = getGenreRank(selected_genres, genre_index_dict)
actor_rank = calculate_actor_ranking(selected_cast)
top_100_actor_count = count_top_100_actors(selected_cast)
director_rank = calculate_director_ranking(director)
has_top_25_director = has_top_25_directors(director)
writer_rank = calculate_writer_ranking(writer)
has_top_25_writer = has_top_25_writers(writer)
has_top_25_company = has_top_25_companies(selected_companies)
num_production_companies = len(selected_companies)
company_rank = calculate_company_ranking(selected_companies)
in_english = 1 if selected_language == "English" else 0
produced_in_US = check_usa(selected_countries)
num_production_countries = len(selected_countries)
release_year = 2024


################################################################################################################################
    
# Button for prediction
if st.button('Predict Revenue'):
    # LabelEncoder for month, season and year
    release_month = encoder.transform([release_month])[0] if release_month in encoder.classes_ else -1
    season = encoder.transform([season])[0] if season in encoder.classes_ else -1
    release_year = encoder.transform([release_year])[0] if release_year in encoder.classes_ else -1

    features = [
        produced_in_US, runtime, season, num_production_companies, 
        top_100_actor_count, writer_rank, num_production_countries, budget, 
        actor_rank, has_top_25_writer, release_month, has_top_25_director, in_english, 
        release_year, has_top_25_company, director_rank, company_rank, genre_rank
    ]
    
    # Indices of features to apply log+1 transformation
    indices_to_log_transform = [3, 4, 5, 6, 7, 8, 15, 16, 17]  # Adjust these indices as needed
    transformed_features = [np.log1p(features[i]) if i in indices_to_log_transform else features[i] for i in range(len(features))]
    
    # Ensure the features are in the correct shape
    features_array = np.array(transformed_features).reshape(1, -1)

    feature_names = [
        'produced_in_US', 'runtime', 'season', 'num_production_companies', 
        'top_100_actor_count', 'writer_rank', 'num_production_countries', 'budget', 
        'actor_rank', 'has_top_25_writer', 'release_month', 'has_top_25_director', 'in_english', 
        'release_year', 'has_top_25_company', 'director_rank', 'company_rank', 'genre_rank'
    ]

    # Create dataframe
    df = pd.DataFrame(features_array, columns=feature_names)

    # Select appropriate model based on budget
    if budget >= 10000000:
        prediction = model_high.predict(df)
        error = 0.28
    else:
        prediction = model_low.predict(df)
        error = 0.22

    # Convert prediction from log scale
    prediction = np.expm1(prediction)[0] / 1e6

    if prediction * 1e6 > 2 * budget:
        error_amount = round(error * prediction, 2)
        benefit = ((prediction*1e6 - budget) / (prediction * 1e6)) * 100
        image_path = 'img/mrbeast.jpg'
        image = Image.open(image_path)
        st.image(image, caption="You will be rich! Congrats! Go for it :)", use_column_width=True)
    else:
        error_amount = error * prediction
        image_path = 'img/arruinado.jpg'
        image = Image.open(image_path)
        st.image(image, caption="Maybe you could try with another options...?", use_column_width=True)
         
    st.write(f'The predicted revenue for your movie is: ${prediction:.2f}M ± ${error_amount}M, with a {benefit:.2f}% benefit.')