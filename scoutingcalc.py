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

atts = ["Speaker notes during auton", "Amplified speaker notes during teleop", "Total speaker notes during teleop", "Amp notes during auton", "Amp notes during teleop", "Drops/Fails", "Blocked Shots", "Times Blocked", "Total Fails (Drops + Blocks)", "Spotlight", "Buddy Climb", "Trap", "Onstage"]
#    total speaker notes auton (integer); amplified note (integer); total speaker notes teleop (integer); amp notes auton (integer); amp notes teleop (integer); drop/fail (integer); spotlight (bool); buddy climb (bool); trap (bool); onstage (bool)

with st.sidebar:
    attributes = st.multiselect("Which attributes do you want to utilize?", atts, [])

st.write(attributes)

class SideBarSetup:
    def getWeight(self, i, a):
        with st.sidebar:
            weight = st.number_input("What weightage should" + attributes[i] + "have?", key = "attname " + str(a), placeholder = "100")
        return weight
    

sblist = []
weightages = []
for x in range (len(attributes)):
    globals()["sb" + str(x)] = SideBarSetup()
    globals()["wt" + str(x)] = globals()["sb" + str(x)].getWeight(x, x)
    weightages.append((attributes[x], globals()["wt" + str(x)]))
    sblist.append(globals()["sb" + str(x)])


st.header("Ranked Table")

def wtRank(thisAtt, thisCol):
    for wt, desAtt in thisAtt:
        rank =  thisCol * wt
    return rank
            

data = pd.read_csv("MOCK_DATA.csv")
rank_data = pd.DataFrame(df["name"],df["match_number"], df["team_number"], df["color"])
for col in data.columns[4:]:
    rank_data[col] = data[col].rank(ascending = false)
    rank_data["New_" + col] = wtRank(attributes[0], rank_data[col])
    
st.write(rank_data)

#(21-rank_data["ground_pickup_auton"][1])*wt

st.dataframe(data)