import streamlit as st
import os
from st_pages import Page, show_pages, add_page_title



if 'MEETINGS_IN_DEV' not in os.environ:
    
    show_pages(
        [ Page("home.py", "Home", "🏠"),
            Page("pages/insights.py", "Insights across time", ":bulb:"),
            Page("pages/minutes.py", "Meeting Minutes", ":chart:"),
            Page("pages/member_report.py", "Member Participation", ":bar_chart:"),
        ]
    )


st.title("Public Speaking Club Meeting Insights")

st.page_link("pages/insights.py", label="What happed over a period of time", icon="🧐")
st.page_link("pages/minutes.py", label="Extract full details of a meeting", icon="📜")
st.page_link("pages/member_report.py", label="Know participation by member", icon="👤")
st.divider()

st.write(":orange[For the curious:]")
st.write(":one: This is a hobby project of a member of the public speaking club.")
st.write(":two: Data is ingested from [here](https://btmcminutes.blogspot.com/)")
st.write(":three: Suggestions or ideas are most welcome; if you are here, I am sure you know the app developer")






