import headers as h
from graphqlclient import GraphQLClient
import pandas as p
import json as j
from pprint import pprint

# config values
first = 100
second = 50
third = 25
fourth = 12
fifth = 6
seventh = 3

smash = h.init()


# find top 8
def get_top8():
    top_entrants = smash.tournament_show_entrants(h.__tournament_url__, h.__game__, 0)
    return top_entrants


# total entrants
def get_total_entrants():
    client = GraphQLClient('https://api.start.gg/gql/' + h.__APIversion__)
    client.inject_token('Bearer ' + h.__token__)
    event_list = client.execute(h.__top8_query__, h.__top8_vars__)
    entrants = j.loads(event_list)['data']['tournament']['events'][0]['numEntrants']

    #print(entrants)
    return entrants


# different find top 8
def get_top_8():
    client = GraphQLClient('https://api.start.gg/gql/' + h.__APIversion__)
    client.inject_token('Bearer ' + h.__token__)
    event_list = client.execute(h.__top8_query__, h.__top8_vars__)
    standings = j.loads(event_list)['data']['tournament']['events'][0]['standings']['nodes']

    cols = ["player", "standing"]
    top_df = p.DataFrame(columns=cols)
    for node in standings:
        record = {"player": node['entrant']['name'], "standing": node['placement']}
        top_df = top_df.append(record, ignore_index=True)

    #print(top_df)
    return top_df


def get_dqs():
    client = GraphQLClient('https://api.start.gg/gql/' + h.__APIversion__)
    client.inject_token('Bearer ' + h.__token__)
    record_count = 1
    cols = ['player']
    dq_df = p.DataFrame(columns=cols)
    while record_count != 0:
        set_list = client.execute(h.__dq_query__, h.__dq_vars__)
        sets = j.loads(set_list)
        count = j.loads(set_list)
        record_count = count['data']['tournament']['events'][0]['sets']['pageInfo']['total']
        h.__dq_vars__['page'] += 1
        sets = sets['data']['tournament']['events'][0]['sets']
        #print(sets)
        for node in sets['nodes']:
            if node['slots'][0]['standing']['stats']['score']['value'] == -1:
                record = {'player': node['slots'][0]['standing']['entrant']['name']}
                dq_df = dq_df.append(record, ignore_index=True)

            if node['slots'][1]['standing']['stats']['score']['value'] == -1:
                record = {'player': node['slots'][1]['standing']['entrant']['name']}
                dq_df = dq_df.append(record, ignore_index=True)

    #print(dq_df.drop_duplicates())
    return dq_df.drop_duplicates()['player']


def calculate_scores() -> p.DataFrame:
    cols = ['player', 'score']
    the_list = p.DataFrame(columns=cols)
    top8 = get_top_8()
    total = get_total_entrants()
    dq_count = get_dqs().count()
    entrants = total - dq_count

    print('total - dq: ', entrants)
    print('total: ', total)
    print('dq: ', dq_count)
    print('---')
    print(top8)

    for rank in top8:
        if rank == 1:
            record = {'player': rank['player'], 'standing': 100 + entrants}
            the_list = the_list.append(record, ignore_index=True)

    print(the_list)

# find total entrants
# def get_total_entrants():
#     total_entrants = 0
#     events = smash.tournament_show_events(h.__tournament_slug__)
#
#     for event in events:
#         if event['name'] == h.__game_formal__:
#             total_entrants = event['entrants']
#
#     # figure out unique DQ's, subtract from total_entrants
#     keep_searching = True
#     iterator = 0
#     all_dqs = []
#     while keep_searching:
#         print(iterator)
#         bracket_sets = smash.tournament_show_sets(h.__tournament_slug__, h.__game__, iterator)
#         for set in bracket_sets:
#             if set['entrant1Score'] == -1:
#                 all_dqs.append(set['entrant1Name'])
#             if set['entrant2Score'] == -1:
#                 all_dqs.append(set['entrant2Name'])
#         print(all_dqs)
#         iterator += 1
#         if bracket_sets == []:
#             keep_searching = False
#
#     unique_dqs = []
#
#     unique_dq_count = 0
#
#     # traversing the array
#     for item in all_dqs:
#         if item not in unique_dqs:
#             unique_dq_count += 1
#             unique_dqs.append(item)
#
#     total_entrants = total_entrants - unique_dq_count
#
#     return total_entrants

#
# # assign points
# def print_top_8():
#     top_entrants = get_top8()
#     total_entrants = get_total_entrants()
#     print('test')
#     for entrant in top_entrants:
#         if entrant['finalPlacement'] == 1:
#             entrant_name = entrant['tag']
#             entrant_points = first + total_entrants
#             print(f'{entrant_name} - {entrant_points}')
#         if entrant['finalPlacement'] == 2:
#             entrant_name = entrant['tag']
#             entrant_points = second + total_entrants
#             print(f'{entrant_name} - {entrant_points}')
#         if entrant['finalPlacement'] == 3:
#             entrant_name = entrant['tag']
#             entrant_points = third + total_entrants
#             print(f'{entrant_name} - {entrant_points}')
#         if entrant['finalPlacement'] == 4:
#             entrant_name = entrant['tag']
#             entrant_points = fourth + total_entrants
#             print(f'{entrant_name} - {entrant_points}')
#         if entrant['finalPlacement'] == 5:
#             entrant_name = entrant['tag']
#             entrant_points = fifth + total_entrants
#             print(f'{entrant_name} - {entrant_points}')
#         if entrant['finalPlacement'] == 7:
#             entrant_name = entrant['tag']
#             entrant_points = seventh + total_entrants
#             print(f'{entrant_name} - {entrant_points}')