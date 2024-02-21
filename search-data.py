import streamlit as st
import pandas as pd
from scipy import stats

# Function to read and preprocess the data
@st.cache(allow_output_mutation=True)
def load_and_process_data(file_path):
    try:
        # Attempt to read the Excel file
        df = pd.read_excel(file_path, engine='openpyxl')
        # Drop duplicate columns from the DataFrame
        df = df.loc[:, ~df.columns.duplicated()]
        return df
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()  # Return an empty DataFrame on failure

def generate_percentile_ranks(player_name, df):
    try:
        player = df[df['Player'] == player_name].iloc[0]

        goals_percentile = stats.percentileofscore(df['Goals'], player['Goals'])
        xg_percentile = stats.percentileofscore(df['xG'], player['xG'])

        # Display percentile ranks as text
        st.write(f"{player_name}'s Percentile Ranks:")
        st.write(f"Goals Percentile: {goals_percentile}%")
        st.write(f"xG Percentile: {xg_percentile}%")
    except Exception as e:
        st.error(f"Error generating percentile ranks: {e}")

def main():
    st.title("Data scouting app")

    file_path = "Scouting men 2324.xlsx"  # Set the file path directly

    df = load_and_process_data(file_path)

    if df.empty:
        st.warning("No data to display. Please check the file path and format.")
        return

    st.sidebar.title("Search")

    try:
        leagues = df['League'].unique()
        selected_league = st.sidebar.selectbox("Select League", leagues)

        teams_in_selected_league = df[df['League'] == selected_league]['Team'].unique()
        selected_team = st.sidebar.selectbox("Select Team", teams_in_selected_league)

        filtered_df = df[(df['League'] == selected_league) & (df['Team'] == selected_team)]

        if not filtered_df.empty:
            st.write(filtered_df[['Player', 'Team', 'League', 'Minutes played', 'Goals', 'Assists', 'xG']])
            selected_player = st.sidebar.selectbox("Select Player", filtered_df['Player'].unique())
            if st.sidebar.button("Display Percentile Ranks"):
                generate_percentile_ranks(selected_player, filtered_df)
        else:
            st.warning("No players found for the selected filters.")
    except Exception as e:
        st.error(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
