__token__ = ''
__tournament_url__ = 'colorado-mile-high-burst-monthly-july-2023'
__game__ = 'street-fighter-6'
__game_formal__ = 'Street Fighter 6'
__APIversion__ = 'alpha'
__tournament_slug__ = ['colorado-mile-high-burst-monthly-july-2023',
                        'colorado-mile-high-burst-monthly-august-2023',
                       'bowu-monthly-2']
__eventid__ = ['935958', # Aki July
                '953284', # Aki Aug
               '944803'] #Springs 2
__autoqual_slug__ = ['colorado-mile-high-burst-monthly-july-2023',
                     'colorado-mile-high-burst-monthly-august-2023',
                     'bowu-monthly-2']
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
    "eventID": '935958',
    "phase": "Finals",
    "page": 1,
    "perPage": 8,
    "slug": __tournament_slug__
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
  "slug": __tournament_slug__,
  "eventID": '935958',
  "phase": "Finals",
  "page": 1,
  "perPage": 50
}
