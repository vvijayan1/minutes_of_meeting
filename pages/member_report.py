import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os
from utilities import *
from datetime import date
from st_pages import Page, show_pages, add_page_title

def select_member_and_date():
    # Get current members
    members = get_current_members()
    
    # Create a selectbox for member selection
    selected_member = st.selectbox(
        'Select a member:',
        options=members['name'],
        format_func=lambda x: f"{x} (ID: {members[members['name'] == x]['member_id'].values[0]})"
    )
    
    # Get the member_id of the selected member
    selected_member_id = members[members['name'] == selected_member]['member_id'].values[0]
    
    today = date.today()
    current_year = today.year

    if today.month <= 6:
            default_date = date(current_year, 1, 1)
    else:
            default_date = date(current_year, 7, 1)


    default_date_value = date.fromisoformat(default_date.strftime('%Y-%m-%d'))

    # Create a date input for the from date
    from_date = st.date_input(
        "Select a start date:",
        value=default_date_value,
        min_value=datetime(2024, 1, 1).date(),
        max_value=datetime.now().date()
    )
    
    # Create a submit button
    submit_button = st.button("Generate Report")

    # Return the selected values 
    return selected_member_id, from_date


def get_member_participation(member_id, start_date):
    # Convert start_date to string format for SQL query
    start_date_str = start_date.strftime('%Y-%m-%d')
    
    # SQL query to get member participation
    sql_query = f"""
    SELECT 
        m.meeting_date,
        COALESCE(
            (CASE
                WHEN rt. president_member_id = {member_id} THEN 'President'
                WHEN rt.tod_member_id = {member_id} THEN 'Toastmaster of the Day'
                WHEN rt.saa_member_id = {member_id} THEN 'Sergeant-at-Arms'
                WHEN rt.ttm_member_id = {member_id} THEN 'Table Topics Master'
                WHEN rt.general_evaluator_member_id = {member_id} THEN 'General Evaluator'
                WHEN rt.timer_member_id = {member_id} THEN 'Timer'
                WHEN rt.ah_counter_member_id = {member_id} THEN 'Ah-Counter'
                WHEN rt.grammarian_member_id = {member_id} THEN 'Grammarian'
                WHEN s.speaker_member_id = {member_id} THEN '(Prepared) Speaker'
                WHEN s.evaluator_member_id = {member_id} THEN 'Evaluator'
                WHEN tt.speaker_member_id = {member_id} THEN 'Table Topics Speaker'

                ELSE 'Absent'
            END),
            'Absent'
        ) AS participation
    FROM 
        meetings m
    LEFT JOIN role_takers rt ON m.meeting_id = rt.meeting_id
    LEFT JOIN prepared_speeches s ON m.meeting_id = s.meeting_id
    LEFT JOIN table_topics tt ON m.meeting_id = tt.meeting_id

    WHERE 
        m.meeting_date >= '{start_date_str}' and (
        rt. president_member_id = {member_id} or 
        rt.tod_member_id = {member_id} or 
        rt.saa_member_id = {member_id} or 
        rt.ttm_member_id = {member_id} or 
        rt.general_evaluator_member_id = {member_id} or 
        rt.timer_member_id = {member_id} or 
        rt.ah_counter_member_id = {member_id} or 
        rt.grammarian_member_id = {member_id} or 
        s.speaker_member_id = {member_id} or   
        s.evaluator_member_id = {member_id} or 
        tt.speaker_member_id = {member_id} )

    GROUP BY 
        m.meeting_date
    ORDER BY 
        m.meeting_date DESC    

    """
    
    # Execute the query
    conn = st.connection('minutes', type='sql')
    df = conn.query(sql_query)
    
    # Pivot the dataframe to have dates as index and participation as column
    df_pivot = df.pivot(index='meeting_date', columns='participation', values='participation')
    df_pivot = df_pivot.fillna('')
    
    # Combine all columns into one
    df_pivot['Participation'] = df_pivot.apply(lambda row: ' '.join(row.dropna()), axis=1)
    
    # Keep only the 'Participation' column
    df_final = df_pivot[['Participation']]
    
    return df_final

def display_member_participation(member_id, start_date):
    df = get_member_participation(member_id, start_date)
    
    st.subheader(":violet[Member Participation]")
    st.dataframe(df)


html_temp = """
<div style="background-color:#772432;padding:1px">
<h3 style="color:#A9B2B1;text-align:center;">Know participation by member</h3>
</div>
"""
st.markdown(html_temp,unsafe_allow_html=True)

st.write(":blue[Beta feature. Please report any issues to the app developer]")
# Call the function
member_id, start_date = select_member_and_date()

# Display the selected values (you can remove this later if not needed)

display_member_participation(member_id, start_date)
