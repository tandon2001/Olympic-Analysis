import numpy as np
def medal_tally(df):
    medal_tally = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    medal_tally = medal_tally.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold', ascending=False).reset_index()
    medal_tally['total'] = medal_tally['Gold'] + medal_tally['Silver'] + medal_tally['Bronze']
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Gold'] = medal_tally['Gold'].astype('int')
    medal_tally['Silver'] = medal_tally['Silver'].astype('int')
    medal_tally['Bronze'] = medal_tally['Bronze'].astype('int')
    medal_tally['total'] = medal_tally['total'].astype('int')
    return medal_tally
def country_year_list(df):
    years = df['Year'].unique().tolist()
    years.sort()
    years.insert(0,'overall')
    country = np.unique(df['region'].dropna().values).tolist()
    country.sort()
    country.insert(0,'Overall')

    return years,country


def fetch_medal_tally(df, years, country):
    medal_df = df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'Year', 'City', 'Sport', 'Event', 'Medal'])
    flag = 0
    if years == 'overall' and country == 'Overall':
        temp_df = medal_df
    if years == 'overall' and country != 'Overall':
        flag = 1
        temp_df = medal_df[medal_df['region'] == country]
    if years != 'overall' and country == 'Overall':
        temp_df = medal_df[medal_df['Year'] == int(years)]
    if years != 'overall' and country != 'Overall':
        temp_df = medal_df[(medal_df['Year'] == int(years)) & (medal_df['region'] == country)]
    if flag == 1:

        x = temp_df.groupby('Year').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                    ascending=True).reset_index()
    else:
        x = temp_df.groupby('region').sum()[['Gold', 'Silver', 'Bronze']].sort_values('Gold',
                                                                                      ascending=False).reset_index()

    x['total'] = x['Gold'] + x['Silver'] + x['Bronze']
    x['Gold'] = x['Gold'].astype('int')
    x['Silver'] = x['Silver'].astype('int')
    x['Bronze'] = x['Bronze'].astype('int')
    x['total'] = x['total'].astype('int')

    print(x)
    return (x)

def data_over_time(df,col):
    nations_over_time = df.drop_duplicates(['Year', col])['Year'].value_counts().reset_index()
    nations_over_time.columns = ['Year', col]
    nations_over_time = nations_over_time.sort_values('Year')
    return nations_over_time


# def most_successful(df, sport):
#     temp_df = df.dropna(subset=['Medal'])
#
#     if sport != 'Overall':
#         temp_df = temp_df[temp_df['Sport'] == sport]
#
#     x = temp_df['Name'].value_counts().reset_index()
#     x.rename(columns={'index': 'Name', 'Name': 'Medals'}, inplace=True)
#
#     # Merge based on the correct column (e.g., 'Name')
#     x = x.merge(df, left_on='Name', right_on='Name', how='left')[
#         ['Name', 'Medals', 'Sport', 'region']].drop_duplicates('Name')
#
#     return x


def most_successful(df, sport):
    temp_df = df.dropna(subset=['Medal'])

    if sport != 'Overall':
        temp_df = temp_df[temp_df['Sport'] == sport]

    x = temp_df.groupby('Name').agg(Medals=('Medal', 'size'),
                                    Sport=('Sport', 'first'),
                                    region=('region', 'first')).reset_index()

    return x


def yearwise_medal_tally(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]
    final_df = new_df.groupby('Year').count()['Medal'].reset_index()

    return final_df

def country_event_heatmap(df,country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df.drop_duplicates(subset=['Team', 'NOC', 'Games', 'City', 'Sport', 'Event', 'Medal'], inplace=True)

    new_df = temp_df[temp_df['region'] == country]

    pt =  new_df.pivot_table(index='Sport', columns='Year', values='Medal', aggfunc='count').fillna(0)

    return pt


def most_successful_countrywise(df, country):
    temp_df = df.dropna(subset=['Medal'])
    temp_df = temp_df[temp_df['region'] == country]

    # Get the top 10 most successful athletes
    top_athletes = temp_df['Name'].value_counts().head(10).index

    # Filter the original DataFrame to include only the top athletes
    x = df[df['Name'].isin(top_athletes)][['Name', 'Sport']].drop_duplicates()

    return x



