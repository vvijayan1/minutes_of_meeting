# this is a streamlit page that provides analysis of several aspects of meetings 

import streamlit as st
from utilities import *
import numpy as np
import pandas as pd
from datetime import date


def accept_user_input():
    # create a streamlit form to accept user input
    with st.form(key='analysis_form'):
        # add a date input for the start date

        min_date_value = date.fromisoformat('2024-01-01')
        max_date_value = date.today()

        start_date = st.date_input('From what date do you want to analyze?', min_value=min_date_value, max_value=max_date_value)

        # add a date input for the end date
        end_date = st.date_input('Till what date do you want to analyze?',min_value=min_date_value, max_value=max_date_value)

        # add a submit button
        submit_button = st.form_submit_button(label='Submit')

    # return the start and end dates
    return start_date, end_date




def get_meeting_list(start_date, end_date):
    
    meeting_ids_sql = f"select meeting_id from meetings where date between '{start_date}' and '{end_date}'"
    
    conn = st.connection('minutes', type='sql')

    meeting_ids = conn.query(meeting_ids_sql)

    return meeting_ids





def highlight_none(val):
    if val is None or pd.isnull(val):
        return 'background-color: orange'
    elif val == 'P':
        return 'background-color: green'
    

def highlight_spoke(val):

    if val is None or pd.isnull(val):
        return 'background-color: grey'
    elif val == 'S':
        return 'background-color: blue'


def highlight_speakers(val):

    if val is None or pd.isnull(val):
        return 'background-color: #7393B3'
    elif val == 'S':
        return 'background-color: purple'


def highlight_evaluators(val):

    if val is None or pd.isnull(val):
        return 'background-color: #7393B3'
    elif val == 'S':
        return 'background-color: #5D3FD3'



def display_evaluators(meeting_ids_csv):

    meeting_attendance_sql = f"select meeting_id, evaluation_counterpart_id from speeches where meeting_id in ({meeting_ids_csv})"
    members_sql = f"select member_id, first_name from members"

    conn = st.connection('minutes', type='sql')

    meeting_attendance = conn.query(meeting_attendance_sql)
    all_members = conn.query(members_sql)


    unique_meeting_ids = meeting_attendance['meeting_id'].unique().tolist()
    unique_member_ids = all_members['member_id'].unique().tolist()


    # define a dictionary that has indexes
    attendance_matrix_df = pd.DataFrame(index = unique_member_ids, 
                      columns = unique_meeting_ids)
    


    for index, row in meeting_attendance.iterrows():
        meeting_id = row['meeting_id']
        member_id = row['evaluation_counterpart_id']
        attendance_matrix_df.loc[member_id][meeting_id] = 'S'


    member_dict = all_members.set_index('member_id')['first_name'].to_dict()

    for current_index in attendance_matrix_df.index:
        if current_index in member_dict:
            new_index_label = member_dict[current_index]
            attendance_matrix_df.rename(index={current_index: new_index_label}, inplace=True)


    attendance_matrix_df['Count_S'] = attendance_matrix_df[unique_meeting_ids].apply(lambda row: row.eq('S').sum(), axis=1)
    attendance_matrix_df_sorted = attendance_matrix_df.sort_values(by='Count_S', ascending=False).drop('Count_S', axis=1)

    # change column IDs to meeting dates 
    meeting_sql = f"select meeting_id, date from meetings where meeting_id in ({meeting_ids_csv})"
    meeting_dates = conn.query(meeting_sql)

    meeting_dates_dict = meeting_dates.set_index('meeting_id')['date'].to_dict()

    attendance_matrix_df_sorted = attendance_matrix_df_sorted.rename(columns=meeting_dates_dict)
    styled_attendance_matrix = attendance_matrix_df_sorted.style.map(highlight_evaluators)

    
    styled_attendance_matrix.index.name = "Member"
    st.dataframe(styled_attendance_matrix, 
                 column_config={'Member': st.column_config.TextColumn("Member", width="medium")})
    








def display_prepared_speakers(meeting_ids_csv):

    meeting_attendance_sql = f"select meeting_id, speaker_id from speeches where meeting_id in ({meeting_ids_csv})"
    members_sql = f"select member_id, first_name from members"

    conn = st.connection('minutes', type='sql')

    meeting_attendance = conn.query(meeting_attendance_sql)
    all_members = conn.query(members_sql)


    unique_meeting_ids = meeting_attendance['meeting_id'].unique().tolist()
    unique_member_ids = all_members['member_id'].unique().tolist()


    # define a dictionary that has indexes
    attendance_matrix_df = pd.DataFrame(index = unique_member_ids, 
                      columns = unique_meeting_ids)
    


    for index, row in meeting_attendance.iterrows():
        meeting_id = row['meeting_id']
        member_id = row['speaker_id']
        attendance_matrix_df.loc[member_id][meeting_id] = 'S'


    member_dict = all_members.set_index('member_id')['first_name'].to_dict()

    for current_index in attendance_matrix_df.index:
        if current_index in member_dict:
            new_index_label = member_dict[current_index]
            attendance_matrix_df.rename(index={current_index: new_index_label}, inplace=True)


    attendance_matrix_df['Count_S'] = attendance_matrix_df[unique_meeting_ids].apply(lambda row: row.eq('S').sum(), axis=1)
    attendance_matrix_df_sorted = attendance_matrix_df.sort_values(by='Count_S', ascending=False).drop('Count_S', axis=1)

    # change column IDs to meeting dates 
    meeting_sql = f"select meeting_id, date from meetings where meeting_id in ({meeting_ids_csv})"
    meeting_dates = conn.query(meeting_sql)

    meeting_dates_dict = meeting_dates.set_index('meeting_id')['date'].to_dict()

    attendance_matrix_df_sorted = attendance_matrix_df_sorted.rename(columns=meeting_dates_dict)
    styled_attendance_matrix = attendance_matrix_df_sorted.style.map(highlight_speakers)


    styled_attendance_matrix.index.name = "Member"
    st.dataframe(styled_attendance_matrix, 
                 column_config={'Member': st.column_config.TextColumn("Member", width="medium")})


def display_table_topics_speakers(meeting_ids_csv):

    meeting_attendance_sql = f"select meeting_id, speaker_id from table_topics where meeting_id in ({meeting_ids_csv})"
    members_sql = f"select member_id, first_name from members"

    conn = st.connection('minutes', type='sql')

    meeting_attendance = conn.query(meeting_attendance_sql)
    all_members = conn.query(members_sql)


    unique_meeting_ids = meeting_attendance['meeting_id'].unique().tolist()
    unique_member_ids = all_members['member_id'].unique().tolist()


    # define a dictionary that has indexes
    attendance_matrix_df = pd.DataFrame(index = unique_member_ids, 
                      columns = unique_meeting_ids)
    


    for index, row in meeting_attendance.iterrows():
        meeting_id = row['meeting_id']
        member_id = row['speaker_id']
        attendance_matrix_df.loc[member_id][meeting_id] = 'S'


    member_dict = all_members.set_index('member_id')['first_name'].to_dict()

    for current_index in attendance_matrix_df.index:
        if current_index in member_dict:
            new_index_label = member_dict[current_index]
            attendance_matrix_df.rename(index={current_index: new_index_label}, inplace=True)


    attendance_matrix_df['Count_S'] = attendance_matrix_df[unique_meeting_ids].apply(lambda row: row.eq('S').sum(), axis=1)
    attendance_matrix_df_sorted = attendance_matrix_df.sort_values(by='Count_S', ascending=False).drop('Count_S', axis=1)

    # change column IDs to meeting dates 
    meeting_sql = f"select meeting_id, date from meetings where meeting_id in ({meeting_ids_csv})"
    meeting_dates = conn.query(meeting_sql)

    meeting_dates_dict = meeting_dates.set_index('meeting_id')['date'].to_dict()

    attendance_matrix_df_sorted = attendance_matrix_df_sorted.rename(columns=meeting_dates_dict)
    styled_attendance_matrix = attendance_matrix_df_sorted.style.map(highlight_spoke)


    styled_attendance_matrix.index.name = "Member"
    st.dataframe(styled_attendance_matrix, 
                 column_config={'Member': st.column_config.TextColumn("Member", width="medium")})


def display_meeting_attendance(meeting_ids_csv):

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
    


    for index, row in meeting_attendance.iterrows():
        meeting_id = row['meeting_id']
        member_id = row['member_id']
        attendance_matrix_df.loc[member_id][meeting_id] = 'P'


    member_dict = all_members.set_index('member_id')['first_name'].to_dict()

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

    attendance_matrix_df_sorted = attendance_matrix_df_sorted.rename(columns=meeting_dates_dict)
    styled_attendance_matrix = attendance_matrix_df_sorted.style.map(highlight_none)

    styled_attendance_matrix.index.name = "Member"
    st.dataframe(styled_attendance_matrix, 
                 column_config={'Member': st.column_config.TextColumn("Member", width="medium")})



def display_awards(meeting_ids_csv):

    sql_query = f'''SELECT
    m.first_name  AS member_name,
    COUNT(CASE WHEN a.best_speaker_id = m.member_id THEN 1 ELSE NULL END) AS best_speaker_awards,
    COUNT(CASE WHEN a.best_table_topics_speaker_id = m.member_id THEN 1 ELSE NULL END) AS best_table_topics_awards,
    COUNT(CASE WHEN a.best_evaluator_id = m.member_id THEN 1 ELSE NULL END) AS best_evaluator_awards,
	COUNT(CASE WHEN a.best_auxiliary_role_taker_id = m.member_id THEN 1 ELSE NULL END) AS best_auxiliary_role_awards,
	COUNT(CASE WHEN a.best_role_taker_id= m.member_id THEN 1 ELSE NULL END) AS best_role_taker_awards
FROM
    members m
LEFT JOIN
    awards a ON m.member_id IN (a.best_speaker_id, a.best_table_topics_speaker_id, a.best_evaluator_id,a.best_auxiliary_role_taker_id ,a.best_role_taker_id)
where a.meeting_id  in ({meeting_ids_csv})
GROUP BY
 m.first_name
ORDER BY
    member_name;
'''

    conn = st.connection('minutes', type='sql')
    awards_df = conn.query(sql_query)

    # add a column for total awards
    awards_df['Total Awards'] = awards_df.iloc[:, 1:].sum(axis=1)


    st.write(awards_df)

    
def main(): 
    

    html_temp = """
<div style="background-color:#772432;padding:1px">
<h3 style="color:#A9B2B1;text-align:center;">Insights: know what happened over a time period</h3>
</div>
"""
    st.markdown(html_temp,unsafe_allow_html=True)
    
    start_date, end_date = accept_user_input()
    
    st.write('From Date:', start_date)
    st.write('To Date:', end_date)

    meeting_list = get_meeting_list(start_date, end_date)

    # convert elements of the df into a csv
    meeting_ids_csv = ','.join([str(i) for i in meeting_list['meeting_id']])


    st.subheader("Attendance Matrix")
    st.write("In decreseasing order of total attendance; :green[in green means present]")
    display_meeting_attendance(meeting_ids_csv)

    st.subheader("Table Topics Attempts over time")
    st.write("In descreasing order of total table topics attempts; :blue[in blue means attempted]")
    display_table_topics_speakers(meeting_ids_csv)


    st.subheader("Prepared Speeches over time")
    st.write("In descreasing order of speeches; :violet[in purple means delivered a prepared speech]")
    display_prepared_speakers(meeting_ids_csv)



    st.subheader("Evaluations over time")
    st.write("In descreasing order of evaluations; :violet[in violet means evaluated a speech]")
    display_evaluators(meeting_ids_csv)

    st.subheader("Medal Tally")
    display_awards(meeting_ids_csv)


    st.divider()
    st.write(":arrow_forward: The author welcomes suggestions/ideas.")
    st.write(":arrow_forward: Info is incorrect? Apologies! Please let the author know.")

main()