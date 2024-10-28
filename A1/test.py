def dijkstra_example(self, source):
    """
    Example from Dr. Ian
    """
    discovered = [] # Is a Queue
    discovered.append(source)
    while len(discovered) > 0:
        u = discovered.pop(0)
        u.visited = True
        for edge in u.edges:
            v = edge.v
            if v.discovered == False: # means distance is still \inf
                discovered.append(v)
                v.discovered = True
                v.distance = u.distance + edge.w
                v.previous = u
            else: # v.visited = False
                if v.distance > u.distance + edge.w:
                    # Update distance
                    v.distance = u.distance + edge.w
                    # CONT ... 


##########

import heapq

class Edge:
    def __init__(self, destination, weight):
        self.destination = destination
        self.weight = weight

class Vertex:
    def __init__(self, tree_id):
        self.tree_id = tree_id
        self.edges = []
        self.solulu_time = None  # Time to destroy this as a Solulu tree
        self.teleport = None  # Destination if this is a Solulu tree
        self.is_exit = False

class TreeMap:
    def __init__(self, roads, solulus):
        # Initialize the maximum index for the list of vertices
        max_tree_id = max(max(u, v) for u, v, _ in roads)
        self.vertices = [Vertex(i) for i in range(max_tree_id + 1)]
        for u, v, w in roads:
            self.vertices[u].edges.append(Edge(v, w))
        for x, y, z in solulus:
            vertex = self.vertices[x]
            vertex.solulu_time = y
            vertex.teleport = z

    def escape(self, start, exits):
        min_heap = []
        costs = [(float('inf'), float('inf')) for _ in self.vertices]  # (cost without solulu, cost with solulu)
        costs[start] = (0, float('inf'))
        heapq.heappush(min_heap, (0, start, False, [start]))  # include start in path

        for exit in exits:
            self.vertices[exit].is_exit = True

        paths = []
        while min_heap:
            cost, idx, used_solulu, path = heapq.heappop(min_heap)
            current_vertex = self.vertices[idx]

            if current_vertex.is_exit and used_solulu:
                # print(f"Exiting through {idx} with path {path} and cost {cost}")
                # return cost, path
                paths.append((cost, path))

            for edge in current_vertex.edges:
                v = edge.destination
                new_cost = cost + edge.weight
                new_path = path + [v]
                if not used_solulu:
                    if new_cost < costs[v][1]:
                        costs[v] = (costs[v][0], new_cost)
                        heapq.heappush(min_heap, (new_cost, v, False, new_path))
                else:
                    if new_cost < costs[v][0]:
                        costs[v] = (new_cost, costs[v][1])
                        heapq.heappush(min_heap, (new_cost, v, True, new_path))
                        
            # When you find a solulu and haven't clawed a solulu
            if current_vertex.solulu_time is not None and not used_solulu:
                solulu_cost = cost + current_vertex.solulu_time
                teleport_idx = current_vertex.teleport 
                new_path = path + [teleport_idx] if teleport_idx != idx else path
                if solulu_cost < costs[teleport_idx][0]:
                    costs[teleport_idx] = (solulu_cost, costs[teleport_idx][1])
                    heapq.heappush(min_heap, (solulu_cost, teleport_idx, True, new_path))

        if len(paths) != 0:
            min_cost = paths[0][0]
            min_path = paths[0]
            for path in paths:
                if path[0] < min_cost:
                    min_path = path[1]

            return min_path

        return None

    def escape(self, start, exits):
        min_heap = []
        times = [float('inf')] * len(self.vertices)
        times[start] = 0
        paths = [[] for _ in range(len(self.vertices))]
        paths[start] = [start]

        heapq.heappush(min_heap, (0, start))
        
        while min_heap:
            current_time, u = heapq.heappop(min_heap)
            
            if current_time > times[u]:
                continue
            
            for edge in self.vertices[u].edges:
                v = edge.destination
                total_time = current_time + edge.time

                if total_time < times[v]:
                    times[v] = total_time
                    self.vertices[v].predecessor = u
                    heapq.heappush(min_heap, (total_time, v))
                    paths[v] = paths[u] + [v]
        

        return paths
        best_time = float('inf')
        best_path = []

        for exit in exits:            
            # print(f"Exit: {exit}")
            # Get predecessor of the exit
            pred = (exit, 0)
            # Note: pred = tuple (predecessor tree ID, time taken to travel between)

            time = 0
            path = []
            while pred != None:

                path.append(pred[0])
                # Get vertice of predecessor
                pred_vertex = self.vertices[pred[0]]

                print(f"{pred[0]}, {pred_vertex.predecessor}")


                time += pred[1]

                # print(pred[0])

                # if predecessor is a solulu
                if pred_vertex.teleport_origin_id != None:
                    time += self.vertices[pred_vertex.teleport_origin_id].solulu_time
                    time += times[pred_vertex.teleport_origin_id]

                    if time < best_time:
                        best_time = time

                        # Get start to solulu
                        if pred_vertex.teleport_origin_id != pred_vertex.tree_id:
                            path.append(pred_vertex.teleport_origin_id)

                        solulu_pred = self.vertices[pred_vertex.teleport_origin_id].predecessor
                        # if pred_vertex.teleport_origin_id != exit:
                        #     # Backtrack path to from solulu to start
                        #     while solulu_pred != None:
                        #         path.append(solulu_pred[0])
                        #         solulu_pred = self.vertices[solulu_pred[0]].predecessor
                        #         print(f"Solulu pred: {solulu_pred}")

                        best_path = path

                if time > best_time:
                    break
                
                # Update predecessor
                pred = pred_vertex.predecessor


        return best_time, best_path[::-1]       
                                   




if __name__ == "__main__":
    roads = [(0,1,4), (1,2,2), (2,3,3), (3,4,1), (1,5,2),
    (5,6,5), (6,3,2), (6,4,3), (1,7,4), (7,8,2),
    (8,7,2), (7,3,2), (8,0,11), (4,3,1), (4,8,10)]
    # The solulus represented as a list of tuples
    solulus = [(5,10,0), (6,1,6), (7,5,7), (0,5,2), (8,4,8)]
    # Creating a TreeMap object based on the given roads
    myforest = TreeMap(roads, solulus)

    start = 3
    exits = [4]
    got = myforest.escape(start, exits)
    expected = (20, [3, 4, 8, 7, 3, 4])
    
    print(got)


