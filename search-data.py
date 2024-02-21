import streamlit as st
import pandas as pd
from scipy import stats
import math

# Function to read and preprocess the data
@st.cache
def load_and_process_data(file_path):
    df = pd.read_excel(file_path)
    # Drop duplicate columns from the DataFrame
    df = df.loc[:, ~df.columns.duplicated()]
    return df

def generate_percentile_ranks(player_name, df):
    player = df[df['Player'] == player_name].iloc[0]

    goals_percentile = stats.percentileofscore(df['Goals'], player['Goals'])
    xg_percentile = stats.percentileofscore(df['xG'], player['xG'])

    # Display percentile ranks as text
    st.write(f"{player_name}'s Percentile Ranks:")
    st.write(f"Goals Percentile: {goals_percentile}%")
    st.write(f"xG Percentile: {xg_percentile}%")

def main():
    st.title("Data scouting app")

    # Set the file path directly since we're using only one file
    file_path = "Scouting men 2324.xlsx"

    # Load data using the caching function
    df = load_and_process_data(file_path)

    # Create a sidebar column on the left for filters
    st.sidebar.title("Search")

    # Dropdown menu for selecting League
    leagues = df['League'].unique()
    selected_league = st.sidebar.selectbox("Select League", leagues)

    # Filter teams based on the selected league
    teams_in_selected_league = df[df['League'] == selected_league]['Team'].unique()

    # Dropdown menu for selecting Team
    selected_team = st.sidebar.selectbox("Select Team", teams_in_selected_league)

    # Create a text input for the user to enter a player name
    player_name = st.sidebar.text_input("Search Player by Name")

    # Filter the DataFrame based on selected filters
    filtered_df = df[(df['League'] == selected_league) & (df['Team'] == selected_team)]

    # Display the filtered DataFrame
    st.write(filtered_df[['Player', 'Team', 'League', 'Minutes played', 'Goals', 'Assists', 'xG']])

    # Add a button to select a player and display percentile ranks
    selected_player = st.sidebar.selectbox("Select Player", df['Player'].values)
    if st.sidebar.button("Display Percentile Ranks"):
        generate_percentile_ranks(selected_player, filtered_df)

if __name__ == "__main__":
    main()
