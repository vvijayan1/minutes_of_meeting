import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime
import os

from st_pages import Page, show_pages, add_page_title

def print_formatted_sub_header(sub_header):
    html_temp = f"""
    <div>
    <h3 style="color:#A9B2B1;text-align:left;">{sub_header}</h3>
    </div>
    """
    st.markdown(html_temp,unsafe_allow_html=True)




def highlight_speech_cols(s, coldict):

    if s.name in coldict.keys():
        return ['background-color: {}'.format(coldict[s.name])] * len(s)
    
    return [''] * len(s)





def print_meeting_details(meeting_date):
    # need a function that connects to mysql database
    conn = st.connection('minutes', type='sql')

    meeting_details = conn.query(f'SELECT meeting_id, theme FROM meetings WHERE date = \'{meeting_date}\'')

    if meeting_details.empty:
        st.write(':red[Oh! There was no meeting on this day! What a pity! ] :hushed:')
        return 0

    meeting_id = meeting_details.loc[0].iloc[0]
    theme = meeting_details.loc[0].iloc[1]

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.markdown(f'''### :hash: :gray[{meeting_id}]''')
            
    with col2:
        simplified_date = meeting_date.strftime('%d %B, %Y')
        st.markdown(f'''### :calendar: :gray[{simplified_date}]''')
    
    with col3:
   
        st.markdown(f'''### :clipboard: :gray[{theme}]''')
   
    with col4:
        draw_meeting_progress_bar(meeting_date)

    return meeting_id


def draw_meeting_progress_bar(meeting_date):

    # based on the meeting date, determine if it is first half of the year or second half of the year

    if meeting_date.month <= 6:
        # first half of the year
        start_date = f'{meeting_date.year}-01-01'
        end_date = f'{meeting_date.year}-06-30'
    else:
        # second half of the year
        start_date = f'{meeting_date.year}-07-01'
        end_date = f'{meeting_date.year}-12-31'
    
    # find weeks elapsed between start and end 

    delta = pd.to_datetime(end_date) - pd.to_datetime(meeting_date)
    weeks_left = delta.days / 7

    percentage_weeks_over = 100 - (weeks_left / 26) * 100    

    data_df = pd.DataFrame(
        {
            "weeks": [percentage_weeks_over]
        }
    )



    st.dataframe(data_df, column_config={
        "weeks": st.column_config.ProgressColumn("Term progress",
                                                 help="Percentage of weeks elapsed in the term",
                                                  min_value=0, max_value=100, format="%d%%")
    }, hide_index=True)

    

def print_role_takers(meeting_number):


    role_taker_sql = f"select t1.first_name as President, t2.first_name as ToD, \
t3.first_name as SAA, t4.first_name as TTM, \
t8.first_name as 'GE', \
t5.first_name as Timer, t6.first_name as AhCounter,\
t7.first_name as Grammarian \
from role_takers rt \
left join members t1 on t1.member_id = rt.president_id \
left join members t2 on t2.member_id = rt.tod_id \
left join members t3 on t3.member_id = rt.saa_id \
left JOIN members t4 on t4.member_id = rt.ttm_id \
left JOIN members t5 on t5.member_id = rt.timer_id \
left JOIN members t6 on t6.member_id = rt.ah_counter_id \
left JOIN members t7 on t7.member_id = rt.grammarian_id \
left JOIN members t8 on t8.member_id = rt.ge_id \
where meeting_id = {meeting_number};"
    
    conn = st.connection('minutes', type='sql')

    role_takers = conn.query(role_taker_sql)

    st.markdown('''### :pushpin: :gray[The Pillars of the Meeting]''')    

    coldict = {'President':'#772432', 'ToD':'#6b202d', 'SAA':'#5f1c28', 'TTM':'#531923', 
               'GE':'#004165', 'Timer':'#003a5a', 'AhCounter':'#003450', 'Grammarian':'#002d46'}

    role_takers_stylised1 = role_takers.style.apply(highlight_speech_cols, coldict=coldict)



    st.dataframe(role_takers_stylised1, 
                 column_config ={ 
                     "GE": None, 
                    "Timer": None,
                    "AhCounter": None,
                    "Grammarian": None,
                    "President": st.column_config.TextColumn("President", width="Large"),
                    "SAA": st.column_config.TextColumn("Sergeant-At-Arms", width="Large"),
                    "ToD": st.column_config.TextColumn("Toastmaster of the Day", width="Large"),
                    "TTM": st.column_config.TextColumn("Table Topics Master", width="Large")
                     }, 
                hide_index=True)

    
    st.dataframe(role_takers_stylised1, 
                 column_config ={ 
                     "GE": st.column_config.TextColumn("General Evaluator", width="Large"), 
                    "Timer": st.column_config.TextColumn("Timer", width="Large"),
                    "AhCounter": st.column_config.TextColumn("Ah-Counter", width="Large"),
                    "Grammarian": st.column_config.TextColumn("Grammarian", width="Large"),
                    "President": None,
                    "SAA": None,
                    "ToD": None,
                    "TTM": None
                     }, 
                hide_index=True)





def print_speeches(meeting_number):

    speeches_sql = f"select t1.first_name as Speaker, t2.first_name as Evaluator, \
    title as Title, project as Project  \
from speeches \
left JOIN members t1 on t1.member_id = speaker_id \
left JOIN members t2 on t2.member_id = evaluation_counterpart_id \
where meeting_id = {meeting_number};"
    
    conn = st.connection('minutes', type='sql')

    speeches = conn.query(speeches_sql)

    st.markdown('''### :speaker: :gray[The Prepared Speeches...]''')


    coldict = {'Speaker':'#772432', 'Evaluator':'#004165', 'Title':'#2f0e14', 'Project':'#47151e'}

    stylised_speeches = speeches.style.apply(highlight_speech_cols, coldict=coldict)

    st.dataframe(stylised_speeches, hide_index=True)

    

def print_table_topic_speakers(meeting_number):

    table_topics_sql = f"select first_name as Speaker, topic as Topic \
from table_topics, members \
where speaker_id = member_id \
and meeting_id = {meeting_number};"
    
    conn = st.connection('minutes', type='sql')

    table_topics = conn.query(table_topics_sql)

    coldict = {'Speaker':'#004165', 'Topic':'#772432'}

    st.markdown('''### :placard: :gray[The Table Topics...]''')


    # split the dataframe table_topis into 2 dataframes
    table_topics1 = table_topics.iloc[::2]
    table_topics2 = table_topics.iloc[1::2]


    cola, colb = st.columns(2)

    with cola:
        st.dataframe(table_topics1.style.apply(highlight_speech_cols,coldict=coldict), hide_index=True)
    
    with colb:
         st.dataframe(table_topics2.style.apply(highlight_speech_cols,coldict=coldict), hide_index=True)






   
def highlight_regulars(member_name, meeting_number):


    if member_name is None:
        return 'background-color: black'
    

    # check if the member is regular in the last 4 meetings
    # if yes, then highlight it
    # if no, then don't highlight it

    # find the last 4 meetings
    last_4_meetings_sql = f"select meeting_id \
from meetings \
where meeting_id >= {meeting_number} - 3 \
and meeting_id <= {meeting_number} \
order by meeting_id asc;"
    

    conn = st.connection('minutes', type='sql')

    last_4_meetings = conn.query(last_4_meetings_sql)

    last_4_meetings = last_4_meetings.transpose()
    list = last_4_meetings.values.tolist()

    # convert the list into a string
    last_4_meetings = ','.join(str(e) for e in list[0])

    # find the member id of the member_name
    member_id_sql = f"select member_id \
from members \
where first_name = '{member_name}';"
    
    member_id = conn.query(member_id_sql)
    member_id = member_id.loc[0].iloc[0]

    # find the number of meetings attended by the member
    meetings_attended_sql = f"select count(*) \
from attendance \
where member_id = {member_id} \
and meeting_id in ({last_4_meetings});"
    

    meetings_attended = conn.query(meetings_attended_sql)
    meetings_attended = meetings_attended.loc[0].iloc[0]

    # if the member has attended all the last 4 meetings, then highlight it
    if meetings_attended == 4:
        return 'background-color: #3B0104'
    else:
        return 'background-color: black'




def print_attendees(meeting_number):

    attendees_sql = f"select first_name as Member \
    from attendance, members \
    where attendance.member_id = members.member_id \
    and meeting_id = {meeting_number};"

    conn = st.connection('minutes', type='sql')

    attendees = conn.query(attendees_sql)

    # make attendees list into another dataframe that has 5 elements per row
    attendees_list = attendees['Member'].tolist()
    attendees_list = np.array_split(attendees_list, 5)
    attendees_list = pd.DataFrame(attendees_list)


    st.markdown('''### :raised_hands: :gray[Who were present...]''')


    # if the member name starts with S or M or A, then highlight it
    attendees_list = attendees_list.style.map(highlight_regulars, meeting_number=meeting_number)
    st.dataframe(attendees_list, hide_index=True)
    
    st.caption(':brown[Names in brown background have been regular in the last 4 meetings]')



def print_meeting_metrics(meeting_number):

    total_members_present_sql = f"select count(*) \
from attendance \
where meeting_id = {meeting_number};"
    
    conn = st.connection('minutes', type='sql')

    total_members_present = conn.query(total_members_present_sql)

    #extract the number from the dataframe
    total_members_present = total_members_present.loc[0].iloc[0]


    prev_meeting_number = meeting_number - 1

    previous_meeting_sql = f"select count(*) \
from attendance \
where meeting_id = {prev_meeting_number};"

    previous_meeting_present = conn.query(previous_meeting_sql)


    if not previous_meeting_present.empty:
        previous_meeting_present = previous_meeting_present.loc[0].iloc[0]
    else:
        previous_meeting_present = 0

    diff = (total_members_present - previous_meeting_present)   

    last_4_meetings_sql = f"select count(*) as attendance \
from attendance \
where meeting_id >= {meeting_number} - 3 \
and meeting_id <= {meeting_number} \
group by meeting_id \
order by meeting_id asc;"

    last_4_meetings = conn.query(last_4_meetings_sql)


    total_speakers_sql = f"select count(*) \
from speeches \
where meeting_id = {meeting_number};"

    total_speakers = conn.query(total_speakers_sql)

    if not total_speakers.empty:
        total_speakers = total_speakers.loc[0].iloc[0]
    else:
        total_speakers = 0

    total_speakers_prev_sql = f"select count(*) \
from speeches \
where meeting_id = {prev_meeting_number};"

    total_speakers_prev = conn.query(total_speakers_prev_sql)

    if not total_speakers_prev.empty:
        total_speakers_prev = total_speakers_prev.loc[0].iloc[0]
    else:
        total_speakers_prev = 0 



    diff_speakers = (total_speakers - total_speakers_prev)


    total_table_topics_sql = f"select count(*) \
from table_topics \
where meeting_id = {meeting_number};"

    total_table_topics = conn.query(total_table_topics_sql)
    total_table_topics = total_table_topics.loc[0].iloc[0]

    total_table_topics_prev_sql = f"select count(*) \
from table_topics \
where meeting_id = {prev_meeting_number};"

    total_table_topics_prev = conn.query(total_table_topics_prev_sql)

    if not total_table_topics_prev.empty:
        total_table_topics_prev = total_table_topics_prev.loc[0].iloc[0]
    else:
        total_table_topics_prev = 0

    diff_table_topics = (total_table_topics - total_table_topics_prev)


    last_4_table_topics_sql = f"select count(*) as table_topics \
from table_topics \
where meeting_id >= {meeting_number} - 3 \
and meeting_id <= {meeting_number} \
group by meeting_id \
order by meeting_id asc;"
    
    last_4_table_topics = conn.query(last_4_table_topics_sql)
    
    guests_sql = f"select guests_num \
    from meetings \
    where meeting_id = {meeting_number};"

    guests = conn.query(guests_sql)
    guests = guests.loc[0].iloc[0]

    guests_prev_sql = f"select guests_num \
    from meetings \
    where meeting_id = {prev_meeting_number};"

    guests_prev = conn.query(guests_prev_sql)

    # extract only if the dataframe is not empty
    if not guests_prev.empty:
        guests_prev = guests_prev.loc[0].iloc[0]
    else:
        guests_prev = 0

    diff_guests = (guests - guests_prev)


    last_4_guests_sql = f"select guests_num as guests \
from meetings \
where meeting_id >= {meeting_number} - 3 \
and meeting_id <= {meeting_number} \
order by meeting_id asc;"
    
    last_4_guests = conn.query(last_4_guests_sql)
        

    col1, col2, col3, col4 = st.columns(4)

    with col1:

        st.metric(label="Members Present", value=total_members_present, delta=diff.item(), label_visibility="visible")


        last_4_meetings = last_4_meetings.transpose()
        list = last_4_meetings.values.tolist()

        new_df = pd.DataFrame({ "attendance": list})

        st.dataframe(new_df, column_config={
            "attendance": st.column_config.BarChartColumn("Last 4 attendance", y_min=0,y_max=120)
        }, hide_index=True)


    with col2:

        st.metric(label="Speeches", value=total_speakers, delta=diff_speakers.item(), label_visibility="visible")    


    with col3:

        st.metric(label="Table Topics", value=total_table_topics, delta=diff_table_topics.item(), label_visibility="visible")


        last_4_table_topics = last_4_table_topics.transpose()
        list = last_4_table_topics.values.tolist()

        new_df = pd.DataFrame({ "table_topics": list})

        st.dataframe(new_df, column_config={
            "table_topics": st.column_config.BarChartColumn("Last 4 table topics", y_min=0,y_max=30)
        }, hide_index=True)
    

    with col4:

        st.metric(label="Guests", value=guests, delta=diff_guests.item(), label_visibility="visible")

        last_4_guests = last_4_guests.transpose()
        list = last_4_guests.values.tolist()

        new_df = pd.DataFrame({ "guests": list})

        st.dataframe(new_df, column_config={
            "guests": st.column_config.BarChartColumn("Last 4 guest count", y_min=0,y_max=30)
        }, hide_index=True)

    return total_members_present, diff.item()






def print_awardees(meeting_number):

    # find the best speaker, evaluator and table topics speaker
    # find the best speaker
    awardees_sql = f"select t1.first_name as aux_role_taker, \
t2.first_name as evaluator, \
t3.first_name as role_taker, \
t4.first_name as speaker, \
t5.first_name as tt_speaker \
from awards \
left join members t1 on t1.member_id = awards.best_auxiliary_role_taker_id \
left join members t2 on t2.member_id = awards.best_evaluator_id \
left join members t3 on t3.member_id = awards.best_role_taker_id \
left join members t4 on t4.member_id = awards.best_speaker_id \
left join members t5 on t5.member_id = awards.best_table_topics_speaker_id \
where meeting_id = {meeting_number};"
    
    conn = st.connection('minutes', type='sql')
    awardees = conn.query(awardees_sql)


    st.markdown('''### :trophy: :gray[**And** the award goes to...]''')


    coldict = {'aux_role_taker':'#004165', 'evaluator':'#003a5a', 'role_taker':'#003450', 'speaker':'#002d46', 'tt_speaker':'#00273c'}

    st.dataframe(awardees.style.apply(highlight_speech_cols, coldict=coldict),
                 hide_index=True,
                 column_config ={
                     "aux_role_taker": "Best Auxillary Role Taker",
                     "evaluator": "Best Evaluator",
                    "role_taker": "Best Role Taker",
                    "speaker": "Best Speaker",
                    "tt_speaker": "Best Table Topics Speaker"
                })





def print_footer():

    html_temp = """
<div style="background-color:#772432;padding:0.1px">
<h5 style="color:#A9B2B1;text-align:center;">Better Speaking, Better Thinking, Better Listening</h5>
</div>
"""
    st.markdown(html_temp,unsafe_allow_html=True)




if 'MEETINGS_IN_DEV' not in os.environ:
    
    show_pages(
        [
            Page("minutes.py", "Home", "🏠"),
            Page("pages/insights.py", "Insights", ":bulb:"),
        ]
    )


#st.set_page_config(layout="wide")


# prepare html code that is used as title of the page that is centered and all
# that
html_temp = """
<div style="background-color:#772432;padding:1px">
<h3 style="color:#A9B2B1;text-align:center;">Meeting in a page!</h3>
</div>
"""
st.markdown(html_temp,unsafe_allow_html=True)

# take as input date of meeting on streamlit 
meeting_date = st.date_input('Choose Meeting Date')

meeting_id = print_meeting_details(meeting_date)


if meeting_id == 0:
    st.page_link("pages/insights.py", label="Want to look at Insights instead?", icon="🧐")
    st.stop()


st.markdown("""---""")
print_meeting_metrics(meeting_id)
st.markdown("""---""")
print_role_takers(meeting_id)
st.markdown("""---""")
print_speeches(meeting_id)
st.markdown("""---""")
print_table_topic_speakers(meeting_id)
st.markdown("""---""")
print_attendees(meeting_id)
st.markdown("""---""")
print_awardees(meeting_id)
st.markdown("""---""")
st.page_link("pages/insights.py", label="Want to look at Insights as well?", icon="🧐")
print_footer()

