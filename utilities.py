import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime


def get_current_members():
    # create a connection to the minutes database
    conn = st.connection('minutes', type='sql')

    # create a sql statement to query the members table
    members_sql = """
        SELECT
            member_id,
            first_name
        FROM
            members
        WHERE current_member = 1
        ORDER BY
            first_name
    """

    # query the members table and return a dataframe
    members = conn.query(members_sql)

    # return the dataframe
    return members


def get_last_meeting_ids():
    # create a connection to the minutes database
    conn = st.connection('minutes', type='sql')

    # create a sql statement to query the meetings table
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

    # create a list of the last 3 meeting IDs
    meeting_ids = meetings['meeting_id'].tolist()

    # return the list
    return meeting_ids  

