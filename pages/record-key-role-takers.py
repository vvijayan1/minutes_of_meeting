import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
from utilities import *

def record_key_role_takers():

    last_meeting_ids = get_last_meeting_ids()

    members = get_current_members()

    members['member_name'] = members['member_id'].astype(str) + ', ' + members['name']

    # create a streamlit form to accept user input for the table role_takers which has columns 
    # meeting_id,  president_member_id, saa_member_id, tod_member_id, ttm_member_id, timer_member_id, ah_counter_member_id, grammarian_member_id, general_evaluator_member_id

    with st.form(key='key_role_takers_form'):

        # add a selectbox for the meeting ID
        meeting_id = st.selectbox('Meeting ID', last_meeting_ids)

        # add a selectbox for the president
        president = st.selectbox('President', members['member_name'])

        # extract the member_id from the president
        president_member_id = president.split(',')[0]

        # add a selectbox for the saa
        saa = st.selectbox('SAA', members['member_name'])

        # extract the member_id from the saa
        saa_member_id = saa.split(',')[0]

        # add a selectbox for the tod
        tod = st.selectbox('TOD', members['member_name'])

        # extract the member_id from the tod
        tod_member_id = tod.split(',')[0]

        # add a selectbox for the ttm
        ttm = st.selectbox('TTM', members['member_name'])

        # extract the member_id from the ttm
        ttm_member_id = ttm.split(',')[0]

        # add a selectbox for the timer
        timer = st.selectbox('Timer', members['member_name'])

        # extract the member_id from the timer
        timer_member_id = timer.split(',')[0]

        # add a selectbox for the ah_counter
        ah_counter = st.selectbox('Ah Counter', members['member_name'])

        # extract the member_id from the ah_counter
        ah_counter_member_id = ah_counter.split(',')[0]

        # add a selectbox for the grammarian
        grammarian = st.selectbox('Grammarian', members['member_name'])

        # extract the member_id from the grammarian
        grammarian_member_id = grammarian.split(',')[0]

        # add a selectbox for the ge
        ge = st.selectbox('GE', members['member_name'])

        # extract the member_id from the ge
        general_evaluator_member_id = ge.split(',')[0]

        # add a submit button
        submit_button = st.form_submit_button(label='Submit')

    # display the meeting ID, president, saa, tod, ttm, timer, ah_counter, grammarian, and ge and confirm that the user wants to submit
    st.write('Meeting ID: ', meeting_id)
    st.write('President: ', president)
    st.write('SAA: ', saa)
    st.write('TOD: ', tod)
    st.write('TTM: ', ttm)
    st.write('Timer: ', timer)  
    st.write('Ah Counter: ', ah_counter)
    st.write('Grammarian: ', grammarian)
    st.write('GE: ', ge)

    if st.button('Confirm Key Role Takers'):
        # create a connection to the minutes database
        conn = st.connection('minutes', type='sql')

        session = conn.session

        # create a sql statement to insert the data into the database
        key_role_takers_sql = """
            INSERT INTO role_takers (
                meeting_id,
                president_member_id,
                saa_member_id,
                tod_member_id,
                ttm_member_id,
                timer_member_id,
                ah_counter_member_id,
                grammarian_member_id,
                general_evaluator_member_id
            )
            VALUES (
                :meeting_id,
                :president_member_id,
                :saa_member_id,
                :tod_member_id,
                :ttm_member_id,
                :timer_member_id,
                :ah_counter_member_id,
                :grammarian_member_id,
                :general_evaluator_member_id
            )
        """

        # create a dictionary of parameters to pass to the query
        params = {
            'meeting_id': meeting_id,
            'president_member_id':  president_member_id,
            'saa_member_id': saa_member_id,
            'tod_member_id': tod_member_id,
            'ttm_member_id': ttm_member_id,
            'timer_member_id': timer_member_id,
            'ah_counter_member_id': ah_counter_member_id,
            'grammarian_member_id': grammarian_member_id,
            'general_evaluator_member_id': general_evaluator_member_id
        }

        # insert the data into the key_role_takers table
        session.execute(key_role_takers_sql, params)

        # commit the transaction
        session.commit()

        # close the session
        session.close()

        # display a success message
        st.success('Key Role Takers Recorded')

record_key_role_takers()