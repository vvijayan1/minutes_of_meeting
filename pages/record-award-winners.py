import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utilities import *

def record_award_winnerss():

    last_meeting_ids = get_last_meeting_ids()

    members = get_current_members()

    members['member_name'] = members['member_id'].astype(str) + ', ' + members['first_name']

    # create a streamlit form to accept user intput for the awards table which has the columns
    # meeting_id, best_speaker_id, best_table_topics_speaker_id, best_evaluator_id, 
    # best_role_taker_id, best_auxillary_role_taker_id

    with st.form(key='award_winners_form'):

        # add a selectbox for the meeting ID
        meeting_id = st.selectbox('Meeting ID', last_meeting_ids)

        # add a selectbox for the best speaker
        best_speaker = st.selectbox('Best Speaker', members['member_name'])

        # extract the member_id from the best speaker
        best_speaker_id = best_speaker.split(',')[0]

        # add a selectbox for the best table topics speaker
        best_table_topics_speaker = st.selectbox('Best Table Topics Speaker', members['member_name'])

        # extract the member_id from the best table topics speaker
        best_table_topics_speaker_id = best_table_topics_speaker.split(',')[0]

        # add a selectbox for the best evaluator
        best_evaluator = st.selectbox('Best Evaluator', members['member_name'])

        # extract the member_id from the best evaluator
        best_evaluator_id = best_evaluator.split(',')[0]

        # add a selectbox for the best role taker
        best_role_taker = st.selectbox('Best Role Taker', members['member_name'])

        # extract the member_id from the best role taker
        best_role_taker_id = best_role_taker.split(',')[0]

        # add a selectbox for the best auxillary role taker
        best_auxillary_role_taker = st.selectbox('Best Auxillary Role Taker', members['member_name'])

        # extract the member_id from the best auxillary role taker
        best_auxiliary_role_taker_id = best_auxillary_role_taker.split(',')[0]

        # add a submit button
        submit_button = st.form_submit_button(label='Submit')

    # display the form results
    st.write('Meeting ID: ', meeting_id)
    st.write('Best Speaker: ', best_speaker)
    st.write('Best Table Topics Speaker: ', best_table_topics_speaker)
    st.write('Best Evaluator: ', best_evaluator)
    st.write('Best Role Taker: ', best_role_taker)
    st.write('Best Auxillary Role Taker: ', best_auxillary_role_taker)

    if st.button('Confirm award winners'):

        conn = st.connection('minutes', type='sql')

        session = conn.session

        # create a sql statement to insert the data into the awards table
        awards_sql = """
            INSERT INTO awards (
                meeting_id,
                best_speaker_id,
                best_table_topics_speaker_id,
                best_evaluator_id,
                best_role_taker_id,
                best_auxiliary_role_taker_id
            )
            VALUES (
                :meeting_id,
                :best_speaker_id,
                :best_table_topics_speaker_id,
                :best_evaluator_id,
                :best_role_taker_id,
                :best_auxiliary_role_taker_id
            )
        """

        params = {
            'meeting_id': meeting_id,
            'best_speaker_id': best_speaker_id,
            'best_table_topics_speaker_id': best_table_topics_speaker_id,
            'best_evaluator_id': best_evaluator_id,
            'best_role_taker_id': best_role_taker_id,
            'best_auxiliary_role_taker_id': best_auxiliary_role_taker_id
        }

        session.execute(awards_sql, params)
        session.commit()
        # close the session
        session.close()

        st.success('Award winners have been recorded.')

record_award_winnerss()