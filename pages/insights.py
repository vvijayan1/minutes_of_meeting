# this is a streamlit page that provides analysis of several aspects of meetings 

import streamlit as st
from utilities import *
import numpy as np
import pandas as pd


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


def get_meeting_list(start_date, end_date):
    
    meeting_ids_sql = f"select meeting_id from meetings where date between '{start_date}' and '{end_date}'"
    
    conn = st.connection('minutes', type='sql')

    meeting_ids = conn.query(meeting_ids_sql)

    return meeting_ids

def get_meeting_attendance(meeting_ids_csv):

    meeting_attendance_sql = f"select meeting_id, member_id from attendance where meeting_id in ({meeting_ids_csv})"
    members_sql = f"select member_id, first_name from members"

    conn = st.connection('minutes', type='sql')

    meeting_attendance = conn.query(meeting_attendance_sql)
    all_members = conn.query(members_sql)


    unique_meeting_ids = meeting_attendance['meeting_id'].unique().tolist()
    unique_member_ids = all_members['member_id'].unique().tolist()


    # define a dictionary that has indexes
    attendance_matrix_df = pd.DataFrame(index = unique_member_ids, 
                      columns = unique_meeting_ids)
    
    
    attendance_matrix_df.loc[326062][1419] = 'HAHA'

 
    for index, row in meeting_attendance.iterrows():
        meeting_id = row['meeting_id']
        member_id = row['member_id']
        attendance_matrix_df.loc[member_id][meeting_id] = 'P'


    member_dict = all_members.set_index('member_id')['first_name'].to_dict()

    print(member_dict)

    for current_index in attendance_matrix_df.index:
        if current_index in member_dict:
            new_index_label = member_dict[current_index]
            attendance_matrix_df.rename(index={current_index: new_index_label}, inplace=True)


    attendance_matrix_df['Count_P'] = attendance_matrix_df[unique_meeting_ids].apply(lambda row: row.eq('P').sum(), axis=1)
    attendance_matrix_df_sorted = attendance_matrix_df.sort_values(by='Count_P', ascending=False).drop('Count_P', axis=1)

    # change column IDs to meeting dates 
    meeting_sql = f"select meeting_id, date from meetings where meeting_id in ({meeting_ids_csv})"
    meeting_dates = conn.query(meeting_sql)

    meeting_dates_dict = meeting_dates.set_index('meeting_id')['date'].to_dict()
    print(meeting_dates_dict)

    attendance_matrix_df_sorted = attendance_matrix_df_sorted.rename(columns=meeting_dates_dict)

    st.dataframe(attendance_matrix_df_sorted)


    return meeting_attendance





    
def main(): 
    start_date, end_date = accept_user_input()
    st.write('Start Date:', start_date)
    st.write('End Date:', end_date)

    meeting_list = get_meeting_list(start_date, end_date)

    # convert elements of the df into a csv
    meeting_ids_csv = ','.join([str(i) for i in meeting_list['meeting_id']])

    meeting_attendance = get_meeting_attendance(meeting_ids_csv)




main()