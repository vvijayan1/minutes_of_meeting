import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime

def record_attendance():

    # create a dataframe that has member id, member_name and a checkbox that tells if the member is present 

    # create a connection to the minutes database
    conn = st.connection('minutes', type='sql')

    # create a sql statement to query the members table
    members_sql = """
        SELECT
            member_id,
            name
        FROM
            members
        WHERE is_current_member = 1
        ORDER BY
            name
    """


    # query the members table and return a dataframe
    members = conn.query(members_sql)

    # create a new column in the dataframe that will hold the checkbox value
    members['present'] = False

    # extract the last 3 meeting IDs from the meetings table
    meetings_sql = """
        SELECT
            meeting_id
        FROM
            meetings
        ORDER BY
            meeting_id DESC
        LIMIT 1
    """

    # query the meetings table and return a dataframe
    meetings = conn.query(meetings_sql)

    print(meetings)

    # create a list of the last 3 meeting IDs
    meeting_ids = meetings['meeting_id'].tolist()

    # create a streamlit to accept meeting ID and editable dataframe of members

    # create a streamlit form to accept user input
    with st.form(key='attendance_form'):
        # add a selectbox for the meeting ID
        meeting_id = st.selectbox('Meeting ID', meeting_ids)

        # add a dataframe of members
        members = st.data_editor(members)

        # add a submit button
        submit_button = st.form_submit_button(label='Submit')

        # return the meeting ID and the dataframe of members
        return meeting_id, members
    


# create a streamlit page that provides a form to record attendance

# add a title to the page
st.title('Record Attendance')

# call the accept_user_input function and store the start and end dates
meeting_id, members = record_attendance()

# print the number of members present and who was present along with their id and first names
st.write('Number of Members Present:', members['present'].sum())
st.write('Members Present:')
st.write(members[members['present'] == True][['member_id', 'name']])

# ask for user confirmation to record the attendance
if st.button('Confirm Attendance'):
    
    st.write('Confirming Attendance...')

    # record the attendance into the attendance table
    # create a connection to the minutes database
    conn = st.connection('minutes', type='sql')

    # create a sql statement to query the attendance table
    attendance_sql = """
        INSERT INTO
            attendance
        VALUES
            (:meeting_id, :member_id);
    """

    # loop through the members dataframe and insert the attendance into the attendance table
    # the attendace table has only meeting_id and member_id - for only those members that are present

    with conn.session as session:

        for index, row in members[members['present'] == True].iterrows():
            params = {
                'meeting_id': meeting_id,
                'member_id': row['member_id']
            }


            session.execute(attendance_sql, params)

        session.commit()

        session.close()


    st.write('Attendance Recorded!')






