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

        start_date = st.date_input('From what date do you want to analyze?', 
                                   min_value=min_date_value, max_value=max_date_value,
                                   value=min_date_value)

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

    # add a column for total evaluations based on the number of S
    attendance_matrix_df_sorted['Total Evaluations'] = attendance_matrix_df_sorted[unique_meeting_ids].apply(lambda row: row.eq('S').sum(), axis=1)


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

    # add a column for total speeches based on the number of S
    attendance_matrix_df_sorted['Total Speeches'] = attendance_matrix_df_sorted[unique_meeting_ids].apply(lambda row: row.eq('S').sum(), axis=1)


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

    # add a column for total table topics attempts based on the number of S
    attendance_matrix_df_sorted['Total Table Topics Attempts'] = attendance_matrix_df_sorted[unique_meeting_ids].apply(lambda row: row.eq('S').sum(), axis=1)


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

    attendance_matrix_df_sorted['Total Attendance'] = attendance_matrix_df_sorted[unique_meeting_ids].apply(lambda row: row.eq('P').sum(), axis=1)


    meeting_dates_dict = meeting_dates.set_index('meeting_id')['date'].to_dict()

    attendance_matrix_df_sorted = attendance_matrix_df_sorted.rename(columns=meeting_dates_dict)
    styled_attendance_matrix = attendance_matrix_df_sorted.style.map(highlight_none)


    styled_attendance_matrix.index.name = "Member"
    st.dataframe(styled_attendance_matrix, 
                 column_config={'Member': st.column_config.TextColumn("Member", width="medium")})



def display_awards(meeting_ids_csv):

    sql_query = f'''SELECT
    m.first_name  AS member_name,
    COUNT(CASE WHEN a.best_speaker_id = m.member_id THEN 1 ELSE NULL END) AS best_speaker,
    COUNT(CASE WHEN a.best_table_topics_speaker_id = m.member_id THEN 1 ELSE NULL END) AS best_table_topics,
    COUNT(CASE WHEN a.best_evaluator_id = m.member_id THEN 1 ELSE NULL END) AS best_evaluator,
	COUNT(CASE WHEN a.best_auxiliary_role_taker_id = m.member_id THEN 1 ELSE NULL END) AS best_auxiliary_role,
	COUNT(CASE WHEN a.best_role_taker_id= m.member_id THEN 1 ELSE NULL END) AS best_role_taker
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

    # sort the dataframe by total awards
    awards_df = awards_df.sort_values(by='Total Awards', ascending=False)

    # change the column names
    awards_df.columns = ['Member Name', 'Speaker', 'Table Topics', 'Evaluator', 'Auxiliary Role', 'Role Taker', 'Total Awards']


    # make member name the index
    awards_df.set_index('Member Name', inplace=True)

    # highlight the total awards column
    styled_awards = awards_df.style.applymap(lambda x: 'background-color: #5D3FD3' if x > 0 else 'background-color: #7393B3', subset=['Total Awards'])

    st.dataframe(styled_awards)



def display_summary_stats(meeting_ids_csv):

    sql_query = f'''-- Define the set of meeting IDs you want to restrict the results to
WITH restricted_meetings AS (
    SELECT meeting_id
    FROM meetings -- Assuming you have a meetings table or use a provided list of meeting IDs
    WHERE meeting_id IN ({meeting_ids_csv}) -- Replace with your desired meeting IDs
)

SELECT
    m.first_name AS Member_Name,
    COALESCE(attendance_counts.total_attendance, 0) AS total_attendance,
    COALESCE(speeches_counts.total_speeches, 0) AS total_speeches,
    COALESCE(evaluations_counts.total_evaluations, 0) AS total_evaluations,
    COALESCE(table_topics_counts.total_table_topics, 0) AS total_table_topics
FROM
    members m
LEFT JOIN
    (SELECT member_id, COUNT(*) AS total_attendance
     FROM attendance
     WHERE meeting_id IN (SELECT meeting_id FROM restricted_meetings)
     GROUP BY member_id) AS attendance_counts ON m.member_id = attendance_counts.member_id
LEFT JOIN
    (SELECT speaker_id AS member_id, COUNT(*) AS total_speeches
     FROM speeches
     WHERE meeting_id IN (SELECT meeting_id FROM restricted_meetings)
     GROUP BY speaker_id) AS speeches_counts ON m.member_id = speeches_counts.member_id
LEFT JOIN
    (SELECT evaluation_counterpart_id AS member_id, COUNT(*) AS total_evaluations
     FROM speeches
     WHERE meeting_id IN (SELECT meeting_id FROM restricted_meetings)
     GROUP BY evaluation_counterpart_id) AS evaluations_counts ON m.member_id = evaluations_counts.member_id
LEFT JOIN
    (SELECT speaker_id AS member_id, COUNT(*) AS total_table_topics
     FROM table_topics
     WHERE meeting_id IN (SELECT meeting_id FROM restricted_meetings)
     GROUP BY speaker_id) AS table_topics_counts ON m.member_id = table_topics_counts.member_id
ORDER BY
    member_name;
'''

    conn = st.connection('minutes', type='sql')
    summary_stats_df = conn.query(sql_query)

    # sort by total attendance
    summary_stats_df = summary_stats_df.sort_values(by='total_attendance', ascending=False)

    # make member name the index
    summary_stats_df.set_index('Member_Name', inplace=True)

    # change the column names
    summary_stats_df.columns = ['Total Attendance', 'Total Speeches', 'Total Evaluations', 'Total Table Topics']

    # make each column in different shades of blue
    styled_summary_stats_df = summary_stats_df.style.applymap(lambda x: 'background-color: #7393B3', subset=['Total Attendance'])
    styled_summary_stats_df = styled_summary_stats_df.applymap(lambda x: 'background-color: #5D3FD3', subset=['Total Speeches'])
    styled_summary_stats_df = styled_summary_stats_df.applymap(lambda x: 'background-color: #5D3FD3', subset=['Total Evaluations'])
    styled_summary_stats_df = styled_summary_stats_df.applymap(lambda x: 'background-color: #5D3FD3', subset=['Total Table Topics'])


    st.dataframe(styled_summary_stats_df)



def draw_attendance_stats(meeting_ids_csv):

    sql_query = f'''
    SELECT
    mt.date AS meeting_date,
    COUNT(DISTINCT a.member_id) AS number_of_members_present,
    mt.guests_num AS number_of_guests
FROM
    meetings mt
LEFT JOIN
    attendance a ON mt.meeting_id = a.meeting_id
where mt.meeting_id in ({meeting_ids_csv})
GROUP BY
    mt.meeting_id, mt.date, mt.guests_num
ORDER BY
    mt.date;
'''
    

    conn = st.connection('minutes', type='sql')

    attendance_stats_df = conn.query(sql_query)

    # change the column names to readable ones
    attendance_stats_df.columns = ['Date', 'Num of Members ', 'Num of Guests']    


    # use streamlit's line_chart to plot the attendance stats
    st.line_chart(attendance_stats_df.set_index('Date'))



def get_random_table_topic(meeting_ids_csv):

    sql_query = f'''
    SELECT
    tt.topic
    FROM
    table_topics tt
    WHERE tt.meeting_id in ({meeting_ids_csv})
    ORDER BY RANDOM()
    LIMIT 1;
    '''

    conn = st.connection('minutes', type='sql')
    random_table_topic = conn.query(sql_query)

    st.write("Table topic of the moment: :orange["+random_table_topic['topic'].values[0]+"]")



def get_summary_insights(meeting_ids_csv):

    sql_query = f'''
    SELECT
    (SELECT COUNT(DISTINCT speaker_id) FROM speeches where meeting_id in  ({meeting_ids_csv}) ) AS unique_prepared_speakers,
    (SELECT COUNT(DISTINCT evaluation_counterpart_id) FROM speeches where meeting_id in  ({meeting_ids_csv})) AS unique_evaluators,
    (SELECT COUNT(DISTINCT speaker_id) FROM table_topics where meeting_id in  ({meeting_ids_csv})) AS unique_table_topics_speakers;
    '''

    conn = st.connection('minutes', type='sql')

    summary_insights = conn.query(sql_query)
    # change the column names to readable ones
    summary_insights.columns = ['Unique Prepared Speakers', 'Unique Evaluators', 'Unique Table Topics Speakers']

    # apply color in shares of violet to the dataframe
    summary_insights = summary_insights.style.applymap(lambda x: 'background-color: #5D3FD3', subset=['Unique Prepared Speakers'])
    summary_insights = summary_insights.applymap(lambda x: 'background-color: #6851C4', subset=['Unique Evaluators'])
    summary_insights = summary_insights.applymap(lambda x: 'background-color: #8879C7', subset=['Unique Table Topics Speakers'])




    st.dataframe(summary_insights)










def main(): 
    

    html_temp = """
<div style="background-color:#772432;padding:1px">
<h3 style="color:#A9B2B1;text-align:center;">Insights: know what happened over a time period</h3>
</div>
"""
    st.markdown(html_temp,unsafe_allow_html=True)
    
    start_date, end_date = accept_user_input()
    

    meeting_list = get_meeting_list(start_date, end_date)

    # convert elements of the df into a csv
    meeting_ids_csv = ','.join([str(i) for i in meeting_list['meeting_id']])


    get_summary_insights(meeting_ids_csv)


    st.subheader("Attendance Stats :chart_with_upwards_trend:")
    draw_attendance_stats(meeting_ids_csv)

    st.subheader("Medal Tally :medal:")
    display_awards(meeting_ids_csv)

    st.subheader("How many times did you speak? :speaking_head_in_silhouette:")
    display_summary_stats(meeting_ids_csv)





    st.subheader("Attendance Matrix :chair:")
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



    st.divider()
    st.write(":arrow_forward: The author welcomes suggestions/ideas.")
    st.write(":arrow_forward: Info is incorrect? Apologies! Please let the author know.")

main()