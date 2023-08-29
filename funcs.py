from graphqlclient import GraphQLClient
import pandas as p
import json as j
import headers as h
import time


# Define globals and constants
score_map = {
    1: 100,
    2: 50,
    3: 25,
    4: 12,
    5: 6,
    7: 3
}
player_map = {
    'South': 'YoanP',
    'KDQ | ICrazyJI': 'KDQ | CrazyJ'
}


# get event ID value
def get_event_id(game: str, slug: str) -> str:
    client = GraphQLClient('https://api.start.gg/gql/' + h.__APIversion__)
    client.inject_token('Bearer ' + h.__token__)
    h.__event_lookup_vars__['slug'] = slug
    event_list = client.execute(h.__event_lookup__, h.__event_lookup_vars__)
    #print(event_list)
    events = j.loads(event_list)['data']['tournament']['events']
    for event in events:
        #print(event)
        if event['videogame']['name'] == game:
            return event['id']


# total entrants
def get_total_entrants() -> int:
    client = GraphQLClient('https://api.start.gg/gql/' + h.__APIversion__)
    client.inject_token('Bearer ' + h.__token__)
    event_list = client.execute(h.__top8_query__, h.__top8_vars__)
    entrants = j.loads(event_list)['data']['tournament']['events'][0]['numEntrants']

    return entrants


# different find top 8
def get_top_8(the_list: p.DataFrame) -> p.DataFrame:
    client = GraphQLClient('https://api.start.gg/gql/' + h.__APIversion__)
    client.inject_token('Bearer ' + h.__token__)
    event_list = client.execute(h.__top8_query__, h.__top8_vars__)
    standings = j.loads(event_list)['data']['tournament']['events'][0]['standings']['nodes']

    cols = ["player", "standing", "autoqual"]
    top_df = p.DataFrame(columns=cols)
    for node in standings:
        if h.__top8_vars__['slug'] in h.__autoqual_slug__ and node['placement'] == 1:
            record = {"player": node['entrant']['name'], "standing": node['placement'], 'autoqual': 1}
            top_df = top_df.append(record, ignore_index=True)
        else:
            record = {"player": node['entrant']['name'], "standing": node['placement'], 'autoqual': 0}
            top_df = top_df.append(record, ignore_index=True)
    top_df = top_df.replace({'player': player_map})

    delta = 0
    for player in top_df['player']:
        if player in str(the_list[the_list['autoqual'] == 1]['player']):
            delta += 1
        else:
            break

    for x in range(delta+1):
        top_df.loc[x, 'autoqual'] = 1

    print('')
    print(top_df)

    return top_df


def get_dqs() -> p.DataFrame:
    client = GraphQLClient('https://api.start.gg/gql/' + h.__APIversion__)
    client.inject_token('Bearer ' + h.__token__)
    record_count = 1
    cols = ['player']
    dqw_df = p.DataFrame(columns=cols)
    dql_df = p.DataFrame(columns=cols)

    while record_count != 0:
        set_list = client.execute(h.__dq_query__, h.__dq_vars__)

        sets = j.loads(set_list)
        count = j.loads(set_list)

        record_count = count['data']['tournament']['events'][0]['sets']['pageInfo']['total']
        sets = sets['data']['tournament']['events'][0]['sets']

        h.__dq_vars__['page'] += 1

        for node in sets['nodes']:
            if node['slots'][0]['standing']['stats']['score']['value'] == -1 \
                    and node['slots'][0]['standing']['placement'] == 2:
                if node['round'] > 0:
                    record = {'player': node['slots'][0]['standing']['entrant']['name']}
                    dqw_df = dqw_df.append(record, ignore_index=True)
                elif node['round'] < 0:
                    record = {'player': node['slots'][0]['standing']['entrant']['name']}
                    dql_df = dql_df.append(record, ignore_index=True)

            if node['slots'][1]['standing']['stats']['score']['value'] == -1 \
                    and node['slots'][1]['standing']['placement'] == 2:
                if node['round'] > 0:
                    record = {'player': node['slots'][1]['standing']['entrant']['name']}
                    dqw_df = dqw_df.append(record, ignore_index=True)
                elif node['round'] < 0:
                    record = {'player': node['slots'][1]['standing']['entrant']['name']}
                    dql_df = dql_df.append(record, ignore_index=True)

    dqw_df = dqw_df.drop_duplicates().sort_values(by=['player'])
    dql_df = dql_df.drop_duplicates().sort_values(by=['player'])
    dq_df = dqw_df.merge(dql_df, left_on='player', right_on='player')

    return dq_df


def mark_qualifiers(df: p.DataFrame) -> p.DataFrame:
    aq_df = df[df['autoqual'] == 1].copy()  # Get auto qualifiers
    sc_df = p.DataFrame()            # Get score qualifiers
    nq_df = p.DataFrame()            # Get everyone else

    if h.__current_game__ == 'Street Fighter 6':  # Get top 7 for SF6
        sc_df = df.loc[df['autoqual'] == 0].sort_values('score', ascending=False).head(7).copy()
        nq_df = df.loc[df['autoqual'] == 0].sort_values('score', ascending=False).tail(-7).copy()
    if h.__current_game__ == 'Guilty Gear: Strive':  # Get top 8 for GGS
        sc_df = df.loc[df['autoqual'] == 0].sort_values('score', ascending=False).head(8).copy()
        nq_df = df.loc[df['autoqual'] == 0].sort_values('score', ascending=False).tail(-8).copy()

    aq_df.loc[:, 'qualified'] = 1
    sc_df.loc[:, 'qualified'] = 1
    sc_df.loc[:, 'points_qual'] = 1

    df = p.concat([aq_df, sc_df, nq_df])

    return df.sort_values('rank', ascending=True)


def calculate_scores() -> p.DataFrame:
    cols = ['player', 'score', 'rank', 'autoqual', 'points_qual', 'qualified']
    for game in h.__games__:
        h.__current_game__ = game
        the_list = p.DataFrame(columns=cols)
        for slug in h.__tournament_slug__:
            print('')
            print('-----')
            print('GAME: ', game)
            print('TOURNAMENT ', slug)
            event_id = get_event_id(game, slug)

            h.__top8_vars__['eventID'] = event_id
            h.__dq_vars__['eventID'] = event_id
            h.__top8_vars__['slug'] = slug
            h.__dq_vars__['slug'] = slug
            h.__top8_vars__['page'] = 0
            h.__dq_vars__['page'] = 0

            top8 = get_top_8(the_list)
            total = get_total_entrants()
            dq_count = len(get_dqs().index)
            entrants = total - dq_count

            for i, r in top8.iterrows():
                if r['player'] in the_list['player'].values:
                    the_list.loc[the_list['player'] == r['player'], 'score'] = the_list.loc[the_list['player'] == r['player'], 'score'] + (score_map[r['standing']] + entrants)
                    if the_list['autoqual'][the_list['player'] == r['player']].values == 0 and r['autoqual'] == 1:
                        the_list.loc[the_list['player'] == r['player'], 'autoqual'] = 1
                else:
                    record = {'player': r['player'],
                              'score': score_map[r['standing']] + entrants,
                              'rank': 0,
                              'autoqual': r['autoqual'],
                              'points_qual': 0,
                              'qualified': 0}
                    the_list = the_list.append(record, ignore_index=True)
            the_list.loc[:, 'rank'] = the_list['score'].rank(method='average', ascending=False)
            time.sleep(10)  # The DQ thing made too many requests so you gotta do what you gotta do
            the_list.loc[:, 'qualified'] = 0

        the_list = mark_qualifiers(the_list)
        print('~*~*~*~*~*~*~*~*~~*~*~*~ The List ~*~*~*~*~*~*~*~*~*~*~*~*~*~')
        print(the_list)
        print('~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~*~')
        print('Exporting to csv...')
        file_name = game + '_Stats.csv'
        the_list.to_csv(file_name)
        print('Export complete.')

    return the_list
