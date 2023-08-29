__token__ = ''
__APIversion__ = 'alpha'
__games__ = ['Street Fighter 6',
             'Guilty Gear: Strive'
             ]
__current_game__ = ''
__tournament_slug__ = ['colorado-mile-high-burst-monthly-july-2023',
                       'colorado-mile-high-burst-monthly-august-2023',
                       'bowu-monthly-2',
                       'noco-clash-august-2023',
                       'bowu-monthly-3'
                       ]
__autoqual_slug__ = [
                     'colorado-mile-high-burst-monthly-july-2023',
                     'colorado-mile-high-burst-monthly-august-2023',
                     'bowu-monthly-2',
                     'noco-clash-august-2023',
                     'bowu-monthly-3'
                     ]
__top8_query__ = """
    query TournamentQuery($slug: String, $eventID: ID, $page: Int!, $perPage: Int!) {
      tournament(slug: $slug) {
        name
        events(filter: {id: $eventID}) {
          name,
          numEntrants
          standings(query: {perPage: $perPage, page: $page}) {
            nodes {
              placement
              entrant {
                id
                name
              }
            }
          }
        }
      }
    }
"""
__top8_vars__ = {
    "slug": '',
    "eventID": '',
    "page": 1,
    "perPage": 8
}
__dq_query__ = """
    query TournamentQuery($slug: String, $eventID: ID, $page: Int!) {
  tournament(slug: $slug) {
    name
    events(filter: {id: $eventID}) {
      name,
      sets(
        page: $page
        #perPage: $perPage
        sortType: STANDARD
      ) {
        pageInfo {
          total
        }
        nodes {
          id
          round
          slots {
            standing {
              id
              placement
              entrant {
                name
              }
              stats {
                score {
                  value
                }
              }
            }
          }
        }
      }
    }
  }
}

"""
__dq_vars__ = {
    "slug": '',
    "eventID": '',
    "page": 1,
    "perPage": 50
}

__event_lookup__ = """
    query TournamentQuery($slug: String) {
        tournament(slug: $slug) {
            name,
            events(filter: {
            #id: $eventID
            }) {
                name,
                id,
                videogame {
                    name
                }
            }
        }
  }
    """

__event_lookup_vars__ = {
    "slug": ''
}
