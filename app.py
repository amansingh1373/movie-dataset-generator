import streamlit as st
import pandas as pd
import json

# Read the JSON file
with open('data.json') as file:
    json_data = json.load(file)

# Convert JSON data to DataFrame
df = pd.DataFrame(json_data)

# Create Streamlit app
def main():
    st.title("Movie Data")
    
    # Display the movie data table
    st.subheader("Movie Data Table")
    st.dataframe(df)
    
    # Show selected movie details
    st.subheader("Selected Movie Details")
    selected_movie = st.selectbox("Select a movie", df['name'])
    movie_details = df[df['name'] == selected_movie].iloc[0]
    st.write("Name:", movie_details['name'])
    st.write("Release Year:", movie_details['releaseyear'])
    st.write("Certificate:", movie_details['certificate'])
    st.write("Duration:", movie_details['duration'])
    st.write("Genre:", movie_details['genre'])
    st.write("Rating:", movie_details['rating'])
    st.write("Director:", movie_details['director'])
    st.write("Cast:", movie_details['cast'])

if __name__ == '__main__':
    main()
