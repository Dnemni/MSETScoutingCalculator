import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime

st.set_page_config(
    page_title="MSET Scouting Calculator",
    page_icon="📱",  # You can use any emoji as an icon
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("MSET Scouting Calculator")

# Set theme
theme = {
    "backgroundColor": "#afc9f7",
    "secondaryBackgroundColor": "#8f98ea",
    "textColor": "#000000",
}

st.markdown(
    """
    <style>
        body {
            background-color: %(backgroundColor)s;
        }
        .secondaryBackgroundColor {
            background-color: %(secondaryBackgroundColor)s;
        }
        .markdown-text-container {
            color: %(textColor)s;
        }
    </style>
    """ % theme,
    unsafe_allow_html=True,
)


#Input
st.sidebar.title("Requirement Weighting")

atts = ["ampsFailedAuton", "ampsFailedTeleop", "ampsScoredAuton", "ampsScoredTeleop", "groundAuton", "groundTeleop", "speakersFailedAuton", "speakersFailedTeleop", "speakersScoredAuton", "speakersScoredTeleop"]


with st.sidebar:
    attributes = st.multiselect("Which attributes do you want to utilize?", atts, [])
    

class SideBarSetup:
    def getWeight(self, i, a):
        with st.sidebar:
            weight = st.number_input("What weightage should" + attributes[i] + "have?", key = "attname " + str(a), placeholder = "100")
        return weight/100
    

sblist = []
weightages = []
for x in range (len(attributes)):
    globals()["sb" + str(x)] = SideBarSetup()
    globals()["wt" + str(x)] = globals()["sb" + str(x)].getWeight(x, x)
    weightages.append((attributes[x], globals()["wt" + str(x)]))
    sblist.append(globals()["sb" + str(x)])

# Assuming 'data' is your DataFrame containing team data
data = pd.read_csv("DATA.csv")

# Initialize an empty DataFrame to store the rankings
rank_data = pd.DataFrame(data["scoutName"])


# Calculate rankings for each attribute and add them to rank_data
for attribute in atts:
    rank_data[attribute + '_rank'] = (data[attribute].rank(ascending=False, method = "min"))
    rank_data[attribute + '_rank'] = len(rank_data[attribute + '_rank']) + 1 - rank_data[attribute + '_rank']
    #rank_data[attribute + '_rank'] = rank_data[attribute + '_rank']*weight


# Display the updated DataFrame
rank = 0
data["rank"] = 0
for ind in rank_data.index:
    for attribute, weight in weightages:
        item = rank_data.loc[ind, attribute + '_rank']
        itmwt = item * weight
        rank += itmwt
    data.loc[ind, "rank"] = rank
    rank = 0

st.dataframe(rank_data)
st.dataframe(data)