import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

# similar to record-attendance.py need to record table topics attendance
# table: table_topics; columns: meeting_id, speaker_member_id, topic 

def record_table_topics():

    # extract the last meeting ID from the meetings table
    meetings_sql = """
        SELECT
            meeting_id
        FROM
            meetings
        ORDER BY
            meeting_id DESC
        LIMIT 1
    """

    conn = st.connection('minutes', type='sql')

    meetings = conn.query(meetings_sql)

    # create a list of the last 3 meeting IDs
    meeting_ids = meetings['meeting_id'].tolist()

    meeting_id = meeting_ids[0]

    # create a streamlit to accept meeting ID and editable dataframe of members
    members_sql = f"""
select members.member_id, members.name
from 
attendance left join members 
on attendance.member_id = members.member_id
where is_current_member = 1 and attendance.meeting_id = {meeting_id}
order by name;
"""


    members = conn.query(members_sql)
   

    # add a column called "topic" to the members dataframe

    # add a column that can tell if the member attempted table topic, called "participated" - and a check box

    members['participated'] = False
    members['topic'] = "                                     "

    # create a streamlit form to accept user input
    with st.form(key='attendance_form'):

        members = st.data_editor(members)
        # add a submit button
        submit_button = st.form_submit_button(label='Submit')

    
    # return the meeting ID and the dataframe of members
    return meeting_id, members


# create a streamlit page to record table topics: member_id, first_name, topic
# 

meeting_id, members = record_table_topics()

# display memebers dataframe again and confirm with user if they want to submit 
# the data to the database

st.write(members)

# create a streamlit form to accept user input
with st.form(key='confirm_form'):
    # add a submit button
    submit_button = st.form_submit_button(label='Submit')

    # if the user clicks the submit button, then insert the data into the database
    # table table_topics with columns meeting_id, speaker_member_id, topic
    if submit_button:
        # create a connection to the minutes database
        conn = st.connection('minutes', type='sql')

        # get a session for the connection 
        session = conn.session

        # loop through the members dataframe
        for index, row in members.iterrows():
            # extract the member_id and topic from the row
            member_id = row['member_id']
            topic = row['topic']

            # create a sql statement to insert the data into the table_topics table
            table_topics_sql = """
                INSERT INTO table_topics (meeting_id, speaker_member_id, topic)
                VALUES (:meeting_id, :member_id, :topic)
            """

            # create a dictionary of parameters to pass to the query
            params = {
                'meeting_id': meeting_id,
                'member_id': member_id,
                'topic': topic
            }

            # insert the data into the table_topics table only if the member attempted table topics
            if row['participated'] == True:
                session.execute(table_topics_sql, params)

        session.commit()

        # display a success message
        st.success('Table Topics  has been recorded.')

