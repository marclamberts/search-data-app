import streamlit as st
import pandas as pd

# Function to read and preprocess the data
@st.cache
def load_and_process_data(file_path):
    # Assuming the file is an Excel file. Adjust the function if it's a different format.
    df = pd.read_excel(file_path)
    # Drop duplicate columns from the DataFrame
    df = df.loc[:, ~df.columns.duplicated()]
    return df

def main():
    st.title("Player Data Scouting App")

    # Set the file path directly since we're using only one file
    file_path = "Scouting men 2324.xlsx"

    # Load data using the caching function
    df = load_and_process_data(file_path)

    # Sidebar filters
    st.sidebar.title("Filters")

    # Dropdown for selecting League
    leagues = df['League'].unique()
    selected_league = st.sidebar.selectbox("League", leagues)

    # Dropdown for selecting Team based on League
    teams = df[df['League'] == selected_league]['Team'].unique()
    selected_team = st.sidebar.selectbox("Team", teams)

    # Text input for searching by Player name
    search_query = st.sidebar.text_input("Search Player by Name").lower()

    # Filtering the DataFrame based on selections
    filtered_df = df[df['League'] == selected_league]
    filtered_df = filtered_df[filtered_df['Team'] == selected_team]

    # Further filter by player name if there is a search query
    if search_query:
        filtered_df = filtered_df[filtered_df['Player'].str.lower().str.contains(search_query)]

    # Displaying the filtered DataFrame
    if not filtered_df.empty:
        st.write(filtered_df)
    else:
        st.write("No matching records found.")

if __name__ == "__main__":
    main()
