import streamlit as st
import pandas as pd
import preprocessor,helper
import plotly.express as px
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import scipy.stats as stats

df = pd.read_csv('athlete_events.csv')
region_df = pd.read_csv('noc_regions.csv')



df = preprocessor.preprocess(df,region_df)
st.sidebar.title('Olympics Analysis')

user_menu = st.sidebar.radio(
    'Select an Option',
    ('Medal tally','overall analysis','countrywise analysis','Athletewise analysis')

)





if user_menu == 'Medal tally':

    st.sidebar.header("Medal Tally")
    years,country = helper.country_year_list(df)
    selected_year = st.sidebar.selectbox("Select Year",years)
    selected_country = st.sidebar.selectbox("Select Country", country)

    medal_tally = helper.fetch_medal_tally(df,selected_year,selected_country)
    if selected_year == 'overall' and selected_country == 'Overall':
        st.title('Overall Tally')
    if selected_year != 'overall' and selected_country == 'Overall':
        st.title("Medal Tally in " + " " +  str(selected_year) +" " + 'Olympics')
    if selected_year == 'overall' and selected_country != 'Overall':
        st.title(selected_country +" " + "Overall Performance")
    if selected_year != 'overall' and selected_country != 'Overall':
        st.title(selected_country + " " + "Performance in " + " " + str(selected_year) +" " +  'Olympics')
    st.table(medal_tally)
if user_menu ==  'overall analysis' :
        editions = df['Year'].unique().shape[0]-1
        cities = df['City'].unique().shape[0]
        sports =  df['Sport'].unique().shape[0]
        events =  df['Event'].unique().shape[0]
        athletes =  df['Name'].unique().shape[0]
        nations =  df['region'].unique().shape[0]
        st.title(" Top Statistics ")
        col1,col2,col3 = st.columns(3)
        with col1:
            st.header('Events')
            st.title(editions)
        with col2:
            st.header('Hosts')
            st.title(cities)
        with col3:
            st.header('Sports')
            st.title(sports)

        col1, col2, col3 = st.columns(3)
        with col1:
            st.header('Events')
            st.title(events)
        with col2:
            st.header('Nations')
            st.title(nations)
        with col3:
            st.header('Athletes')
            st.title(athletes)

        nations_over_time = helper.data_over_time(df,'region')
        fig = px.line(nations_over_time, x="Year", y="region")#x="Edition", y="No of Countries")
        st.title("Participating Nations over the years")
        st.plotly_chart(fig)

        events_over_time = helper.data_over_time(df, 'Event')
        fig_events = px.line(events_over_time, x="Year", y="Event")  # x="Edition", y="No of Countries")
        st.title("Events over the years")
        st.plotly_chart(fig_events)

        athletes_over_time = helper.data_over_time(df, 'Name')
        fig1_events = px.line(athletes_over_time, x="Year", y="Name")  # x="Edition", y="No of Countries")
        st.title("Athletes over the years")
        st.plotly_chart(fig1_events)

        st.title("No of Events over Time(Every Sport)")
        fig,ax = plt.subplots(figsize=(20,20))
        x = df.drop_duplicates(['Year', 'Sport', 'Event'])
        ax = sns.heatmap(x.pivot_table(index='Sport', columns='Year', values='Event', aggfunc='count').fillna(0).astype('int'),
            annot=True)
        st.pyplot(fig)

        st.title("Most Succesful Athletes")
        sport_list = df['Sport'].unique().tolist()
        sport_list.sort()
        sport_list.insert(0,'Overall')

        selected_sport = st.selectbox('Select a sport',sport_list)
        x = helper.most_successful(df,selected_sport)
        st.table(x)

if user_menu == 'countrywise analysis':

    st.sidebar.title('Countrywise Analysis')

    country_list = df['region'].dropna().unique().tolist()
    country_list.sort()

    selected_country = st.sidebar.selectbox('Select a country',country_list)

    country_df = helper.yearwise_medal_tally(df, selected_country)
    fig4 = px.line(country_df, x='Year', y='Medal')
    st.title(selected_country + "Medal Tally over the Years")
    st.plotly_chart(fig4)

    st.title(selected_country , 'Excels in the following sports')
    pt = helper.country_event_heatmap(df, selected_country)
    fig,ax = plt.subplots(figsize=(20,20))
    ax = sns.heatmap(pt,annot = True,ax=ax)
    st.pyplot(fig)

    st.title("Top 10 athletes of" + selected_country)
    top10_df = helper.most_successful_countrywise(df,selected_country)
    st.table(top10_df)

if user_menu == 'Athletewise analysis':
    athlete_df = df.drop_duplicates(subset=['Name', 'region'])
    x1 = athlete_df['Age'].dropna()
    x2 = athlete_df[athlete_df['Medal'] == 'Gold']['Age'].dropna()
    x3 = athlete_df[athlete_df['Medal'] == 'Silver']['Age'].dropna()
    x4 = athlete_df[athlete_df['Medal'] == 'Bronze']['Age'].dropna()

    fig = ff.create_distplot([x1, x2, x3, x4], ['Overall Age', 'Gold Medalist', 'Silver Medalist', 'Bronze Medalist'], show_hist=False, show_rug=False)
    fig.show()
    fig.update_layout(autosize=False,width=1000,height=600)
    st.title('Distribution of Age')
    st.plotly_chart(fig)


    x = []
    name = []
    famous_sports = ['Basketball', 'Judo', 'Football', 'Tug-Of-War', 'Athletics',
                     'Swimming', 'Badminton', 'Sailing', 'Gymnastics',
                     'Art Competitions', 'Handball', 'Weightlifting', 'Wrestling',
                     'Water Polo', 'Hockey', 'Rowing', 'Fencing',
                     'Shooting', 'Boxing', 'Taekwondo', 'Cycling', 'Diving', 'Canoeing',
                     'Tennis', 'Golf', 'Softball', 'Archery',
                     'Volleyball', 'Synchronized Swimming', 'Table Tennis', 'Baseball',
                     'Rhythmic Gymnastics', 'Rugby Sevens',
                     'Beach Volleyball', 'Triathlon', 'Rugby', 'Polo', 'Ice Hockey']
    for sport in famous_sports:
        temp_df = athlete_df[athlete_df['Sport'] == sport]
        x.append(temp_df[temp_df['Medal'] == 'Gold']['Age'].dropna())
        name.append(sport)

    fig = ff.create_distplot(x, name, show_hist=False, show_rug=False)
    fig.update_layout(autosize=False, width=1000, height=600)
    st.title("Distribution of Age wrt Sports(Gold Medalist)")
    st.plotly_chart(fig)

    sport_list = df['Sport'].unique().tolist()
    sport_list.sort()
    sport_list.insert(0, 'Overall')





