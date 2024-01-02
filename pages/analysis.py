# this is a streamlit page that provides analysis of several aspects of meetings 

import streamlit as st

# define a function that creates a streamlit form and accepts start and end dates
# the function returns a dataframe of meetings that fall within the date range

def get_meetings(start_date, end_date):
    # create a connection to the minutes database
    conn = st.connection('minutes', type='sql')

    # create a sql statement to query the meetings table
    meetings_sql = """
        SELECT
            meeting_id,
            meeting_date,
            meeting_type,
            meeting_location
        FROM
            meetings
        WHERE
            meeting_date >= %(start_date)s
        AND
            meeting_date <= %(end_date)s
        ORDER BY
            meeting_date
    """

    # create a dictionary of parameters to pass to the query
    params = {
        'start_date': start_date,
        'end_date': end_date
    }

    # query the meetings table and return a dataframe
    meetings = conn.query(meetings_sql, params)

    # return the dataframe
    return meetings



