# this is a streamlit page that provides analysis of several aspects of meetings 

import streamlit as st
from utilities import *


def accept_user_input():
    # create a streamlit form to accept user input
    with st.form(key='analysis_form'):
        # add a date input for the start date
        start_date = st.date_input('Start Date')

        # add a date input for the end date
        end_date = st.date_input('End Date')

        # add a submit button
        submit_button = st.form_submit_button(label='Submit')

    # return the start and end dates
    return start_date, end_date


def get_chronic_absentees(meeting_list):
    # create a connection to the minutes database
    conn = st.connection('minutes', type='sql')

    # get a session for the connection
    session = conn.session()

    # create a list to hold the chronic absentees
    chronic_absentees = []

    # loop through the meeting list
    for meeting in meeting_list:

        # get the attendance for the meeting
        attendance = session.query(Attendance).filter(Attendance.meeting_id == meeting).all()

        # loop through the attendance
        for member in attendance:
            # if the member is not present, then add them to the chronic absentees list
            if member.present == 0:
                chronic_absentees.append(member.member_id)

    # return the list of chronic absentees
    return chronic_absentees


def main(): 
    accept_user_input()

main()