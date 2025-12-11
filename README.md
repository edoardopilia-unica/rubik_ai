# Rubik_ai V. 1.0
This program is designed to solve the rubik's cube using breadth-first search, depth-first search (which are uninformed) and A* search.
DFS is limited to 8 nodes of depth for testing purposes.
A* is designed using manhattan distance as heuristic.


All of these are fully working, however some considerations have to be done:
- It is recommended to solve configuration with a distance to the solution under six nodes, expecially for BFS and DFS. It can take a long time.
- A* is tested up to 8 nodes. Over 8 node it will find a solution but the time can be extremely high.

