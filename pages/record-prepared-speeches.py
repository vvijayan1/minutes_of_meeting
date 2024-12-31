import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utilities import *



def record_speeches():

    last_meeting_ids = get_last_meeting_ids()

    # create a streamlit form to accept speaker, evaluator, title, project_name
    # speaker and evaluator are select boxes with values from the get_current_members function


    # get the current members 
    members = get_current_members()

    # memers is a dataframe with member_id and first_name columns
    # combine the member_id and first_name columns into a single column 
    # separated by a comma and space
    members['member_name'] = members['member_id'].astype(str) + ', ' + members['name']


    with st.form(key='speeches_form'):
        # add a selectbox for the meeting ID
        meeting_id = st.selectbox('Meeting ID', last_meeting_ids)

        # add a selectbox for the speaker and use the first_name column as the display

        speaker = st.selectbox('Speaker', members['member_name'])

        # extract the member_id from the speaker
        speaker_member_id = speaker.split(',')[0]

        # add a selectbox for the evaluator
        evaluator = st.selectbox('Evaluator', members['member_name'])

        # extract the member_id from the evaluator
        evaluator_member_id = evaluator.split(',')[0]

        # add a text input for the title
        title = st.text_input('Title')

        # add a text input for the project_name
        project_name = st.text_input('Project')

        # add a submit button
        submit_button = st.form_submit_button(label='Submit')
    

    # display the meeting ID, speaker, evaluator, title, and project and confirm that the user wants to submit
    st.write('Meeting ID: ', meeting_id)
    st.write('Speaker: ', speaker)
    st.write('Evaluator: ', evaluator)
    st.write('Title: ', title)
    st.write('Project: ', project_name)

    if st.button('Confirm Prepared Speech'):
        # create a connection to the minutes database
        conn = st.connection('minutes', type='sql')

        session = conn.session

        # create a sql statement to insert the data into the database
        speeches_sql = """
            INSERT INTO prepared_speeches (
                meeting_id,
                speaker_member_id,
                evaluator_member_id,
                speech_title,
                project_name
            )
            VALUES (
                :meeting_id,
                :speaker_member_id,
                :evaluator_member_id,
                :title,
                :project_name
            )
        """

        

        # create a dictionary of parameters to pass to the query
        params = {
            'meeting_id': meeting_id,
            'speaker_member_id': speaker_member_id,
            'evaluator_member_id': evaluator_member_id,
            'title': title,
            'project_name': project_name
        }


        # insert the data into the database
        session.execute(speeches_sql, params)


        session.commit()

        # display a message that the data was inserted
        st.write('Prepared speech data inserted into database')


record_speeches()
