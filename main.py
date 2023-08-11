import funcs as f


print('Begin Test')
print('---')

f.calculate_scores()

print('---')
print('End Test')

#
# query
# TournamentQuery($slug: String, $eventID: ID, $phase) {
#     tournament(slug: $slug){
#     name,
#     events(filter: {
#     id:$eventID
# # slug:$eventName
# })
# {
#     name,
#     id,
#     phases {
#     name,
#     id,
#     phaseGroups(query: {
#     filter: {
#
#     }
# }) {
#     nodes
# {
#     wave
# {
#     id,
#     identifier,
#     startAt
# }
# standings(query: {
#     page: 1,
#     perPage: 500
# }) {
#     nodes
# {
#     entrant
# {
#     name
# }
# }
# }
# }
# },
# waves
# {
#     id,
#     identifier,
#     startAt
# }
# }
# }
# }
# }
