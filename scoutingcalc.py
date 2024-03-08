import altair as alt
import numpy as np
import pandas as pd
import streamlit as st
import datetime

st.set_page_config(
    page_title="MSET Scouting Data Visualizer",
    page_icon=":chart:",  # You can use any emoji as an icon
    layout="centered",
    initial_sidebar_state="expanded",
)

st.title("MSET Scouting Data Visualizer")

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

atts = ["Speaker notes during auton", "Amplified speaker notes during teleop", "Total speaker notes during teleop", "Amp notes during auton", "Amp notes during teleop", "Total drops", "Spotlight", "Buddy Climb", "Trap", "Onstage"]
#    total speaker notes auton (integer); amplified note (integer); total speaker notes teleop (integer); amp notes auton (integer); amp notes teleop (integer); drop/fail (integer); spotlight (bool); buddy climb (bool); trap (bool); onstage (bool)

with st.sidebar:
    attributes = st.multiselect("Which attributes do you want to utilize?", atts, [])

st.write(attributes)

class SideBarSetup:
    def bar(self):
        st.sidebar.header("----------")
        
    def getWeight(self, i, a):
        with st.sidebar:
            weight = st.number_input("What weightage should" + attributes[i] + "have?", key = "attname " + str(a), placeholder = "100")
        return weight
    

sblist = []
weightages = []
for x in range (len(attributes)):
    st.write(x)
    globals()["sb" + str(x)] = SideBarSetup()
    if(x>0):
        globals()["sb" + str(x)].bar()
    globals()["wt" + str(x)] = globals()["sb" + str(x)].getWeight(x, x)
    weightages.append((attributes[x], globals()["wt" + str(x)]))
    st.write(weightages)
    sblist.append(globals()["sb" + str(x)])

st.write(weightages)


"""
def basicTeamBoxPlot(tmevscr):
    #Charts
    df = pd.DataFrame([(event, score) for event, scores in tmevscr.items() for score in scores], columns=['Event', 'Points Scored'])

    boxplot = alt.Chart(df).mark_boxplot(extent="min-max", size = 50).encode(
        alt.X("Event:N", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")),
        alt.Y("Points Scored:Q", axis=alt.Axis(labels=True, ticks=True, domain=True, grid=True, domainColor="white", gridColor="white", labelColor="black", tickColor="white", titleColor="black")).scale(zero=False),
        alt.Color("Event:N").legend(None),
        ).properties(
            width=400,
            height=300
        ).configure_title(
            fontSize=16,
            anchor='start'
        )
    # Display the boxplot
    st.altair_chart(boxplot, use_container_width=True)
    
teams_info = []
sblist = []
sb0 = SideBarSetup()
tm0 = sb0.tmnumIN(0)
tmy0 = sb0.tmyrIN(0, tm0)
evnt0 = sb0.tmyrevIN(0, tm0, tmy0)
teams_info.append((tm0, tmy0, evnt0))
sblist.append(sb0)
x = 1

if 'buttonClick' not in st.session_state:
    st.session_state.buttonClick = 0

#buttonClick = 0
if st.button("Add Team", type="primary", key=f"add_team_{x}"):
    st.session_state.buttonClick += 1

tab1, tab2 = st.tabs(["Plots", "Awards"])

for i in range (st.session_state.buttonClick):
    globals()["sb" + str(x)] = SideBarSetup()
    globals()["sb" + str(x)].bar()
    globals()["tm" + str(x)] = globals()["sb" + str(x)].tmnumIN(x)
    globals()["tmy" + str(x)] = globals()["sb" + str(x)].tmyrIN(x, globals()["tm" + str(x)])
    globals()["evnt" + str(x)] = globals()["sb" + str(x)].tmyrevIN(x, globals()["tm" + str(x)], globals()["tmy" + str(x)])
    teams_info.append((globals()["tm" + str(x)], globals()["tmy" + str(x)], globals()["evnt" + str(x)]))
    sblist.append(globals()["sb" + str(x)])
    x += 1

with tab1:
    st.header("Score Visualization")
    
    # Display charts for each team
    for idx, (tm, tmy, evnt) in enumerate(teams_info):
        evscr = getscoreinfo(tm, tmy, evnt)
        nevscr = getscoreinfoNew(tm, tmy, evnt)
                
        st.write("Team " + str(tm) + " Event Scores Boxplot")
        basicTeamBoxPlot(evscr)
        
        st.write("Team " + str(tm) + " Predicted vs Actual Scores Scatterplot")
        individualTeamScatterPlot(nevscr)

with tab2:
    st.header("Awards & Stats")
    for idx, (tm, tmy, evnt) in enumerate(teams_info):
        st.write("Team " + str(tm) + ":")
        awards = tba.team_awards(int(tm), int(tmy))
        
        if len(awards) == 0:
            st.write('In %d, team %d won no awards.' % (tmy, int(tm)))
        elif len(awards) == 1:
            st.write('In %d, team %d won %d award: %s.' % (tmy, int(tm), len(awards), ", ".join('%s (%s)' % (award.name, award.event_key) for award in awards)))
        else:
            st.write('In %d, team %d won %d awards: %s.' % (tmy, int(tm), len(awards), ", ".join('%s (%s)' % (award.name, award.event_key) for award in awards)))
"""