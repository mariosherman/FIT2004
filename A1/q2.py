import heapq

class Edge:
    def __init__(self, origin, destination, time):
        """
        Function description:
        Initializes an Edge object that represents a connection between two vertices in a graph.
        The edges are weighted as they require a given amount of time for traversal.
        
        :Input:
        - origin (int): Tree id of the which vertex it's going to travel from
        - destination (int): Tree id of the destination vertex
        - time (int): The time needed to traverse the edge
        
        :Output, return or postcondition:
        None
        
        :Time complexity: O(1)
        :Time complexity analysis:
        The initialization only requires us to assign input parameters to the instance variables which takes constant time
        
        :Space complexity: O(1)
        :Space complexity analysis:
        The space required is constant as it only needs to store input variables which are constant
        
        :Auxiliary space complexity: O(1)
        :Auxiliary space complexity analysis:
        Only requires to assign input variables to instance variables which are constant
        """

        self.origin = origin
        self.destination = destination
        self.time = time

class Vertex:
    """
    Function description:
    Initializes a Vertex object. The Vertex also maintains lists for its outgoing edges 
    (edges) and incoming edges (reversed_edges), which are useful for various graph algorithms. It also tracks 
    the predecessor vertex or vertices for path finding purposes in both forward and reverse graph explorations.

    :Input:
    - tree_id (int): The unique identifier for this vertex, used to distinguish it from other vertices in the graph.
    
    :Output, return or postcondition:
    None. 

    :Time complexity: O(1)
    :Time complexity analysis:
    The initialization of a Vertex object involves setting up empty lists and a None which are constant time operations

    :Space complexity: O(1)
    :Space complexity analysis:
    The space required is constant as it only needs to store the tree_id, declare empty lists and a None.

    :Auxiliary space complexity: O(1)
    :Auxiliary space complexity analysis:
    The constructor only needs to initialize a fixed number of data which are constant (2 lists, None)
    """
    def __init__(self, tree_id):
        self.tree_id = tree_id
        self.edges = []
        self.reversed_edges = [] # Used when needed to reverse the graph
        self.predecessor = None # (normal predecessor, predecessor from reverse)


class TreeMap:
    def __init__(self, roads, solulus):
        """
        Function description:
        Initializes a TreeMap object to create a graph structure from a given list of roads and solulus. 
        The graph is initialized as a list of trees/vertices where each vertex can have multiple one-way edges outgoing to other trees/vertices

        :Input:
        - roads (list of tuples): Each tuple (u: int, v: int, w: int) 
            represents an edge from vertex u (start tree id) to vertex v (end tree id) with weight w (travel time).
        - solulus (list of tuples): Each tuple (x: int, y: int, z: int) 
            represents a path from vertex x (solulu tree id) to vertex z (teleport tree id) with a claw time of y (time needed to claw the solulu).

        :Output, return or postcondition:
        None

        :Time complexity: O(V + E) = O(|T| + |R|)
        :Time complexity analysis:
        The initialization iterates over each road once to initialize the edges for each tree/vertex.
        It also requires to iterate (number of vertex/tree) amount of times to set up the graph's vertices.

        V: number of vertices
        E: number of edges
        |T|: number of trees
        |R|: number of roads

        :Space complexity: O(V + E) = O(|T| + |R|)
        :Space complexity analysis:
        Space is needed to store all vertices and their edges. 
        Each vertex is stored once, and each edge is stored twice (once in the original direction and once as a reverse edge).

        :Auxiliary space complexity: O(V + E) = O(|T| + |R|)
        :Auxiliary space complexity analysis:
        Apart from the given input lists (roads and solulus), this function needs space for trees/vertices and two lists of edges per treevertex (edges and reversed_edges).
        The auxiliary space depends on the number of vertices and edges.
        """
        
        max_tree_id = max(max(u, v) for u, v, _ in roads) + 1
        self.vertices = [Vertex(i) for i in range(max_tree_id)]
        
        for u, v, w in roads:
            self.vertices[u].edges.append(Edge(u, v, w))
            self.vertices[v].reversed_edges.append(Edge(v, u, w))

        self.solulus = solulus

    def escape(self, start, exits):
        """
        Function description:
        Finds the shortest path from a specified starting tree/vertex to any of the given exits.
        Path requires atleast one occurrence of clawing a solulu before being able to exit through reaching one of the given exits.

        :Input:
        - start (int): The index of the vertex from which to begin the escape.
        - exits (list of int): A list of vertex indices considered as safe exits.

        :Output, return:
        - Returns a tuple (best_time, path) 
        best_time: is the minimum time required to reach any of the exits after breaking a solulu from the starting tree/vertex,
        path: is a list of tree ids representing the route taken for the minimum time

        :Approach description:
        This function operates in three major phases:
        1. Dijkstra from the start vertex to calculate shortest paths to all trees/vertices.
        2. Dijkstra again from the extra tree/vertex which is connected to all exits, mainly used to get distance from exits to all possible solulu teleportation targets
        3. Do a calculation for each solulu which optimal path can be taken.
            Calculation: time from path to solulu + solulu claw time + time from solulu to nearest exit

        Each step uses a minimum heap to efficiently get the next tree/vertex to do operations on based on the shortest currently known distance.

        :Time complexity: O((V + E) log V) = O(|R| log|T|) 
        - The method uses Dijkstra's algorithm twice, once from start to all other trees/vertices to determine shortest paths from the start vertex
          and another in reverse from a dummy vertex which combines all the exits.

        O(V + E) is also O(R) as we need to access each vertice and it's edges which is proportional to the amount of roads
        and log|T| is also log V as the vertices represent the trees
 
        :Time complexity analysis:
        Each edge and tree/vertex is processed in both usage of Dijkstra's algorithm.
        The heap operations (pop, push) take logarithmic time.

        :Space complexity: O(V + E)
        - Stores vertices and edges in the TreeMap's graph.
        Each vertex also keeps a list of edges and reverse edges, which depends on the number of edges.

        :Auxiliary space complexity: O(V)
        - The function uses additional ADTs such as the minimum heap,
          arrays for storing distances from start and from the extra vertex to all other trees/vertices,
          and to keep track of the paths taken in which they all depend on the number of trees/vertices.

        :Auxiliary space analysis:
        The minimum heap can contain up to V vertices.
        Arrays used for distances and paths depend on the number of vertices.
        """
        min_heap = []
        times = [float('inf') for _ in range(len(self.vertices))]
        times[start] = 0
        heapq.heappush(min_heap, (0, start))  # Include path in the heap element
        
        while min_heap:
            current_time, u = heapq.heappop(min_heap)
            
            if times[u] < current_time:
                continue
            
            for edge in self.vertices[u].edges:
                v = edge.destination
                total_time = current_time + edge.time

                if total_time < times[v]:
                    times[v] = total_time
                    heapq.heappush(min_heap, (total_time, v))
                    self.vertices[v].predecessor = (u, None)  # Update predecessor

        # Reverse Graph and Source all the Exits into a singular vertice using an Additional Vertice
        # Extra vertice to source all the exits into one

        # Add extra vertice
        dummy = Vertex(self.vertices[len(self.vertices)-1].tree_id + 1)
        self.vertices.append(dummy)

        # Add edges for the extra vertice
        for exit in exits:
            self.vertices[exit].edges.append(Edge(exit, dummy.tree_id, 0))
            dummy.reversed_edges.append(Edge(dummy.tree_id, exit, 0))

        # Dijkstra from dummy vertice to all
        min_heap = []
        times_reverse = [float('inf') for _ in range(len(self.vertices))]
        times_reverse[dummy.tree_id] = 0
        heapq.heappush(min_heap, (0, dummy.tree_id))  # Include path in the heap element

        while min_heap:
            current_time, u = heapq.heappop(min_heap)
            
            if times_reverse[u] < current_time:
                continue
            
            for edge in self.vertices[u].reversed_edges:
                v = edge.destination
                total_time = current_time + edge.time

                if total_time < times_reverse[v]:
                    times_reverse[v] = total_time
                    heapq.heappush(min_heap, (total_time, v))
                    if self.vertices[v].predecessor != None:
                        self.vertices[v].predecessor = (self.vertices[v].predecessor[0], u)  
                    else:
                        self.vertices[v].predecessor = (None, u)  

        # Check for each solulu and get the best time
        best_time = float('inf')
        used_solulu = None # Which best solulu we decide to traverse to from start
        for solulu in self.solulus:
            time_from_start = times[solulu[0]]
            time_from_end = times_reverse[solulu[2]]
            total_time = time_from_start + time_from_end + solulu[1]

            if total_time < best_time:
                best_time = total_time
                used_solulu = solulu

        if not used_solulu:
            return None

        # Get best path

        # Get path from start to solulu
        path = []
        pred = (used_solulu[0], None)
        # Track back from solulu to start using predecessors
        while (pred[0] != None):
            if self.vertices[pred[0]] != None:
                path.append(pred[0])
                pred = self.vertices[pred[0]].predecessor

        path = path[::-1]

        # From exit to solulu

        # Avoids redundant trees in the path if solulu teleports to the same tree
        if used_solulu[2] != used_solulu[0]:
            path.append(used_solulu[2])

        pred = self.vertices[used_solulu[2]].predecessor

        # Track back in the reverse graph from teleport vertex back to exit using predecessors
        while (pred != None):
            if pred[1] != dummy.tree_id:
                path.append(pred[1])
            if self.vertices[pred[1]] != None:
                pred = self.vertices[pred[1]].predecessor

        return best_time, path


if __name__ == "__main__":
    # Example 1
    # The roads represented as a list of tuples
    roads = [(0,1,4), (1,2,2), (2,3,3), (3,4,1), (1,5,2),
    (5,6,5), (6,3,2), (6,4,3), (1,7,4), (7,8,2),
    (8,7,2), (7,3,2), (8,0,11), (4,3,1), (4,8,10)]
    # The solulus represented as a list of tuples
    solulus = [(5,10,0), (6,1,6), (7,5,7), (0,5,2), (8,4,8)]
    # Creating a TreeMap object based on the given roads
    myforest = TreeMap(roads, solulus)

    # Example 1.1
    # start = 1
    # exits = [7, 2, 4]

    # got = myforest.escape(start, exits)
    # expected = (9, [1, 7])
    # print(expected, got)

    # start = 7
    # exits = [8]

    # got = myforest.escape(start, exits)
    # expected = (6, [7, 8])
    # print((expected, got))

    # # Example 1.3
    # start = 1
    # exits = [3, 4]
    # got = myforest.escape(start, exits)
    # expected = (10, [1, 5, 6, 3])
    # print(expected, got)

    # # Example 1.4
    # start = 1
    # exits = [0, 4]
    # got = myforest.escape(start, exits)
    # expected = (11, [1, 5, 6, 4])
    # print(expected, got)

    # # Example 1.5
    # start = 3
    # exits = [4]
    # got = myforest.escape(start, exits)
    # expected = (20, [3, 4, 8, 7, 3, 4])
    # print(expected, got)

    # # Example 1.6
    # start = 8
    # exits = [2]
    # got = myforest.escape(start, exits)
    # expected = (16, [8, 0, 2])
    # print(expected, got)

    roads = [ 
        (0,1,1),
        (1,2,1),
        (2,3,1),
        (2,5,100),
        (3,4,1),
        (3,5,1),
        (4,2,1),
        (4,3,1),
    ]

    # The solulus represented as a list of tuples
    solulus = [(3, 1, 4)]

    # Creating a TreeMap object based on the given roads
    myforest = TreeMap(roads, solulus)

    print((myforest.escape(1, [5]), (5, [1, 2, 3, 4, 3, 5])))