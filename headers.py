__token__ = ''
__tournament_url__ = 'colorado-mile-high-burst-monthly-july-2023'
__game__ = 'street-fighter-6'
__game_formal__ = 'Street Fighter 6'
__APIversion__ = 'alpha'
__tournament_slug__ = 'colorado-mile-high-burst-monthly-july-2023'
__autoqual_slug__ = ['colorado-mile-high-burst-monthly-july-2023']
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
    "slug": "colorado-mile-high-burst-monthly-july-2023",
    "eventID": "935958",
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
  "eventID": "935958",
  "phase": "Finals",
  "page": 1,
  "perPage": 50
}
