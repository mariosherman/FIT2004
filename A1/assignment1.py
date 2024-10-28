"""
QUESTION 1
"""

"""
Personal Notes:
A fitmon is a list containing elements:
    [affinity_left, cuteness_score, affinity_right]

affinity_left: - positive float in the range of 0.1...0.9 inclusive.
                - only the left-most fitmons[0] will have an affinity_left of 0 as there is 
                no fitmon on the left for it to fuse

Same goes for affinity_right but right-most.

When 2 fitmons fuse:
    - The affinity_left will be based on the affinity_left of the left fitmon,
    affinity_left = fitmons[i][0]
    - The cuteness_score is computed using: cuteness_score = fitmons[i][1] * fitmons[i][2] + fitmons[i+1][1] * fitmons[i+1][0]
    - The affinity_right will be based on the affinity_right of the right fitmon,
    affinity_right = fitmons[i+1][2]

"""

    
def fuse_fitmon_pair(fitmon1: list, fitmon2: list):
    """
    Fuses two fitmons to create a new fitmon with potentially higher cuteness score based on their attributes.
    The fusion formula calculates the new cuteness score using the product of specific attributes from both fitmons.

    :param fitmon1: List of [left affinity (float), cuteness score (int), right affinity (float)]
    :param fitmon2: List of [left affinity (float), cuteness score (int), right affinity (float)]
    :return: List representing the new fused fitmon with updated attributes.

    :Time complexity: O(1) - The calculations and operations done within this function take constant time
    :Space complexity: O(1) - No additional space is needed/used
    :Auxiliary space complexity: O(1) - Only needs to store a float when calculating new cuteness scoer
    """
    new_cuteness_score = fitmon1[1] * fitmon1[2] + fitmon2[1] * fitmon2[0]
    return [fitmon1[0], int(new_cuteness_score), fitmon2[2]]


def fuse(fitmons):
    """
    Finds the maximum cuteness score possible by chain fusing all possibilities of fitmon fusions.
    All fitmon fusions done are only possible when the fitmons in the given list are adjacent.
    This function calculates all possible combinations of fitmon fusions and stores the results in a 2d array to avoid redundant calculations/operations

    Approach Description:
    The function calculates and keeps track of the optimal cuteness scores for each depth of fusions. It keeps track by
    storing each result in a 2D array.

    Example:
    Given input list of length 4 (a, b, c, d):
    For every iteration, fuse all combinations of adjacent fitmons and take the maximum possible combination.
    1st iteration:  We try to get a fusion of length 2 (here it'd be ab, bc, cd)
                     a and b -> ab; b and c -> bc; c and d -> cd
                     we store these within the 2d array.
                    # |a|_|_|_|
                    # |-|b|_|_|
                    # |-|-|c|_|
                    # |-|-|-|d|

    2nd iteration: Now we try to get a higher depht of fusion by incrementing it (3) (here it'd be abc, bcd)
                    So we compare all combinations for example when trying to get ABC:
                    we get max between (AB)C and A(BC) as thats all the possible combinations to make ABC.
                    and we keep going for further combinations.
                    # |a|ab|x |_ |
                    # |-|b |bc|y |
                    # |-|- |c |cd|
                    # |-|- |- |d |

                    x = max((AB)C, A(BC)); y = max(A(BC)); (all combinations possible to make length 3 which are adjacent)

    :param fitmons: List of lists, where each inner list represents a fitmon: [float (left affinity), int (cuteness score), float (right affinity)].
    :return: int representing the maximum cuteness score possible through chain fusions.

    :Time complexity: O(N^3) - The function includes three nested loops that depend on the number of fitmons
    N: number of fitmons in the input list

    :Space complexity: O(N^2) - Uses a 2D array
    N: number of fitmons in the input list

    :Auxiliary space complexity: O(N^2) - Uses a 2D Array
    """
    arr_2d = []
    # Initialize 2D Array    
    # |a|_|_|_|
    # |-|b|_|_|
    # |-|-|c|_|
    # |-|-|-|d|

    for i in range(len(fitmons)):
        arr_2d.append([None for _ in range(len(fitmons))])
        arr_2d[i][i] = fitmons[i]

    # Go through the list in a diagonal way 
    for k in range(len(fitmons)-1):
        i = 0 # Reset starting row
        j = k # Shift starting column to the right
        for _ in range(k, len(fitmons) - 1):
            curr_max_cuteness = 0
            x = 1
            for y in range(i, (j+1)):
                new_cuteness_score = arr_2d[i][y][1] * arr_2d[i][y][2] + arr_2d[i+x][j+1][1] * arr_2d[i + x][j+1][0]
                if new_cuteness_score > curr_max_cuteness:
                    curr_max_cuteness = new_cuteness_score
                    arr_2d[i][j+1] = fuse_fitmon_pair(arr_2d[i][y], arr_2d[i + x][j+1])
                    # Row i, column j+1 represents the next coordinates we're going to fill.
                    # |a|i, j+1|_|_|
                    # |-|b     |_|_|
                    # |-|-     |c|_|
                    # |-|-     |-|d|
                    # Goes right-downwardsd diagonally after each iteration
                x += 1
            j += 1
            i += 1

    # Returns the maximum output which is in the top right of the 2D array
    return arr_2d[0][len(fitmons)-1][1]


"""
QUESTION 2
"""

import heapq

class Edge:
    def __init__(self, origin, destination, time):
        """
        Function description:
        Initializes an Edge object that represents a connection between two vertices in a graph.
        The edges are weighted (time) as they require a certain amount of time for traversal which is given as input
        
        :Input:
        - origin (int): Tree id of the which vertex it's going to travel from
        - destination (int): Tree id of the destination vertex
        - time (int): The time needed to traverse the edge
        
        :Output, return or postcondition:
        None
        
        :Time complexity: O(1)
        :Time complexity analysis:
        The initialization only requires us to assign input variables to instance variables, 
        which takes constant time
        
        :Space complexity: O(1)
        :Space complexity analysis:
        The space required is constant as it only needs to store three attributes: origin, destination, and time, 
        
        :Auxiliary space complexity: O(1)
        :Auxiliary space complexity analysis:
        Only requires to assign fixed numbers of datas which doesn't require any additional space/memory
        """

        self.origin = origin
        self.destination = destination
        self.time = time

class Vertex:
    """
    Function description:
    Initializes a Vertex object. The Vertex also has lists for its outgoing edges (edges for normal edges and reversed_edges for convenience when we need to reverse the graphh)
    It also tracks the predecessor vertices to track paths taken in both normal and reverse graph traversal.

    :Input:
    - tree_id (int): The unique identifier for this vertex, used to distinguish it from other vertices in the graph.
    
    :Output, return or postcondition:
    None. 

    :Time complexity: O(1)
    :Time complexity analysis:
    The initialization of a Vertex object only needs us to set up empty lists and a None which take constant time

    :Space complexity: O(1)
    :Space complexity analysis:
    The space required is constant as it only needs to assign input variable to instance variable and initialize empty lists and a None which doesn't take additional space

    :Auxiliary space complexity: O(1)
    :Auxiliary space complexity analysis:
    The constructor only initializes a fixed number of data which are constant (2 lists, None), so it meanas that no additional space needed
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
        Finds the shortest path which requires the least amount of time from a given starting tree/vertex to any of the given exits.
        This function also takes into account that the path requires atleast one occurrence of clawing a solulu before being able to exit through reaching one of the given exits.

        :Input:
        - start (int): The tree id which represents the tree from where we need to begin our escape from.
        - exits (list of int): A list of tree ids which are the exits.

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

        Each step uses a minimum heap to get the next tree/vertex to do operations on based on the shortest currently known distance. 

        :Time complexity: O((V + E) log V) = O(|R| log|T|) 
        - The method uses Dijkstra's algorithm twice, once from start to all other trees/vertices to determine shortest paths from the start vertex
          and another in reverse from a dummy vertex which combines all the exits. Also take into account usage of min heaps which helps with the time complexity because
          it's operations are in logarithmic time

        O(V + E) is also O(R) as we need to access each vertice and it's edges which dependend on the amount of roads
        and log|T| is also log V as the vertices represent the trees
 
        :Time complexity analysis:
        Each edge and tree/vertex is processed in both usage of Dijkstra's algorithm.
        The heap operations (pop, push) take logarithmic time.

        :Space complexity: O(V + E) = O(|R| + |T|)
        - Stores vertices and edges in the main graph structure.
        Each vertex also keeps a list of edges and reverse edges, which depends on the number of edges.

        :Auxiliary space complexity: O(V) = O|T|
        - The function uses additional ADTs such as the minimum heap,
          arrays for storing distances from start and from the dummy vertex to all other vertices,
          and the predecessors to track the paths taken in which all depend on the number of trees/vertices.

        :Auxiliary space analysis:
        The minimum heap used in Dijkstra's algorithm can contain up to V vertices at any time.
        Arrays for distances and predecessors, each with a length equal to the number of vertices
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

        # Reverse Graph and Source all the Exits using an Additional Vertice
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
                        self.vertices[v].predecessor = (self.vertices[v].predecessor[0], u)  # Update predecessor
                    else:
                        self.vertices[v].predecessor = (None, u)  # Update predecessor

        # Check for each solulu
        best_time = float('inf')
        used_solulu = None # Which solulu we decide to traverse to from start
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
        # Track back from the solulu we used to start using predecessors
        while (pred[0] != None):
            if self.vertices[pred[0]] != None:
                path.append(pred[0])
                pred = self.vertices[pred[0]].predecessor
        path = path[::-1]

        # From exit to solulu
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
