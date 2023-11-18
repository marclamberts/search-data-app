import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from mplsoccer import PyPizza

from scipy import stats  # Import the stats module for percentileofscore
import math

# Function to read and preprocess the data
@st.cache
def load_and_process_data(file_path):
    df = pd.read_excel(file_path)
    # Drop duplicate columns from the DataFrame
    df = df.loc[:, ~df.columns.duplicated()]
    return df

# Function to generate radar chart
def generate_radar_chart(player_name, df, params):
    player = df.loc[df['Player'] == player_name].reset_index()
    player = list(player.loc[0])[3:]

    values = []
    for x in range(len(params)):
        values.append(math.floor(stats.percentileofscore(df[params[x]], player[x])))

    for n, i in enumerate(values):
        if i == 100:
            values[n] = 99

    baker = PyPizza(
        params=params,  # list of parameters
        straight_line_color="white",  # color for straight lines
        straight_line_lw=1,  # linewidth for straight lines
        last_circle_lw=1,  # linewidth of the last circle
        other_circle_lw=1,  # linewidth for other circles
        other_circle_ls="-."  # linestyle for other circles
    )

    # color for the slices and text
    slice_colors = ["#008000"] * 5 + ["#FF9300"] * 5 + ["#D70232"] * 6
    text_colors = ["#000000"] * 8 + ["black"] * 5

    # plot pizza
    fig, ax = baker.make_pizza(
        values,  # list of values
        figsize=(8, 8.5),  # adjust figsize according to your need
        param_location=110,  # where the parameters will be added
        color_blank_space="same",
        slice_colors=slice_colors,
        kwargs_slices=dict(
            edgecolor="white",
            zorder=2, linewidth=1
        ),  # values to be used when plotting slices
        kwargs_params=dict(
            color="black", fontsize=12,
            va="center", alpha=.5
        ),  # values to be used when adding parameter
        kwargs_values=dict(
            color="white", fontsize=12,
            zorder=3,
            bbox=dict(
                edgecolor="white", facecolor="#000000",
                boxstyle="round,pad=0.2", lw=1
            )
        )  # values to be used when adding parameter-values
    )

    # add title
    fig.text(
        0.515, 0.97, f"{player_name}\n\n", size=25,
        ha="center", color="black"
    )

    # add subtitle
    fig.text(
        0.515, 0.932,
        "Per 90 Percentile Rank CF BEL2\n\n",
        size=15,
        ha="center", color="black"
    )

    fig.text(
        0.09, 0.005, f"Minimal 500 minutes", color="black")

    # add credits
    notes = '@lambertsmarc'
    CREDIT_1 = "by Marc Lamberts | @lambertsmarc \ndata: Wyscout\nAll units per 90"
    CREDIT_2 = '@lambertsmarc'
    CREDIT_2 = "inspired by: @Worville, @FootballSlices, @somazerofc & @Soumyaj15209314"
    CREDIT_3 = "by Alina Ruprecht | @alina_rxp"

    fig.text(
        0.99, 0.005, f"{CREDIT_1}\n{CREDIT_2}", size=9,
        color="white",
        ha="right"
    )

    # add text
    fig.text(
        0.34, 0.935, "Attacking      Defending     Key passing                ", size=14, color="black"
    )

    # add rectangles
    fig.patches.extend([
        plt.Rectangle(
            (0.31, 0.9325), 0.025, 0.021, fill=True, color="#008000",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.475, 0.9325), 0.025, 0.021, fill=True, color="#ff9300",
            transform=fig.transFigure, figure=fig
        ),
        plt.Rectangle(
            (0.632, 0.9325), 0.025, 0.021, fill=True, color="#d70232",
            transform=fig.transFigure, figure=fig
        ),
    ])

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

    # Add a button to select a player and generate radar chart
    selected_player = st.sidebar.selectbox("Select Player", df['Player'].values)
    if st.sidebar.button("Generate Radar Chart"):
        params = filtered_df.columns[5:]  # Assuming the numerical columns start from the 5th position
        generate_radar_chart(selected_player, filtered_df, params)

if __name__ == "__main__":
    main()
