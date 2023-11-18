import streamlit as st
import pandas as pd

# Function to read and preprocess the data
@st.cache
def load_and_process_data(file_path):
    df = pd.read_excel(file_path)
    # Drop duplicate columns from the DataFrame
    df = df.loc[:, ~df.columns.duplicated()]
    return df

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

    if player_name:
        # Search for the player in the DataFrame and display their information
        player_info = df[df['Player'].str.contains(player_name, case=False, na=False)]
        if not player_info.empty:
            st.write(player_info[['Player', 'Age', 'Team', 'Minutes played', 'Goals', 'Assists', 'xG', 'xA']])
        else:
            st.write("Player not found")

    # Filter the DataFrame based on selected filters
    filtered_df = df[(df['League'] == selected_league) & (df['Team'] == selected_team)]

    # Display the filtered DataFrame
    st.write(filtered_df[['Player', 'Age', 'Team', 'League', 'Minutes played', 'Goals', 'Assists', 'xG', 'xA']])

if __name__ == "__main__":
    main()
