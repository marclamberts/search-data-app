import streamlit as st
import pandas as pd
import matplotlib as plt
from scipy import stats  # Import the stats module for percentileofscore
import math

# Function to read and preprocess the data
@st.cache
def load_and_process_data(file_path):
    df = pd.read_excel(file_path)
    # Drop duplicate columns from the DataFrame
    df = df.loc[:, ~df.columns.duplicated()]
    return df

def generate_bar_graph(player_name, df):
    player = df[df['Player'] == player_name].iloc[0]

    goals_percentile = stats.percentileofscore(df['Goals'], player['Goals'])
    xg_percentile = stats.percentileofscore(df['xG'], player['xG'])

    # Plotting bar graphs
    fig, axes = plt.subplots(nrows=1, ncols=2, figsize=(12, 5))

    axes[0].bar(['Player'], [goals_percentile], color=['#008000'])
    axes[0].set_title('Goals Percentile')
    axes[0].set_ylim(0, 100)

    axes[1].bar(['Player'], [xg_percentile], color=['#D70232'])
    axes[1].set_title('xG Percentile')
    axes[1].set_ylim(0, 100)

    st.pyplot(fig)

def main():
    st.title("Data scouting app")

    # Create a pop-up for choosing Men or Women
    gender = st.radio("Select Gender", ("Men", "Women"))

    # Determine the file path based on the selected gender
    if gender == "Men":
        file_path = "Scouting men.xlsx"
    else:
        file_path = "Scouting women.xlsx"

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
    st.write(filtered_df[['Player', 'Age', 'Team', 'League', 'Minutes played', 'Goals', 'Assists', 'xG']])

    # Add a button to select a player and generate bar graphs
    selected_player = st.sidebar.selectbox("Select Player", df['Player'].values)
    if st.sidebar.button("Generate Bar Graphs"):
        generate_bar_graph(selected_player, filtered_df)

if __name__ == "__main__":
    main()
