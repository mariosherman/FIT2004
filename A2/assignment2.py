class Node:
    def __init__(self):
        """
        Function description:
        Initialize a node with an array for its child nodes (one for each possible character 'A', 'B', 'C', 'D')
        and a list to store indexes where suffixes start from
        """
        self.children = [None] * 4  # Since the genome contains only 'A', 'B', 'C', 'D'
        self.indexes = [] # Keep traack of index

class SuffixTrie:
    def __init__(self, word):
        """
        Function description:
        Initialize the trie's root  and generate the suffix trie based off the given word

        :Input:
        word: A string representing the genome

        :Output, return or postcondition:
        Initializes a SuffixTrie object 

        :Time Complexity:
        O(N^2)

        :Time Complexity Analysis:
        The function iterates over the text to insert all suffixes and each insertion can take up to O(N) time

        :Space Complexity:
        O(N^2)

        :Space Complexity Analysis:
        Each suffix can create up to N new nodes => N * (N+1) / 2 nodes
        which is O(N^2) in space complexity

        :Auxiliary Space Complexity:
        O(N^2)

        :Auxiliary Space Complexity Analysis:
        The auxiliary space includes the nodes and their children which can be up to O(N^2) in the worst case
        """
        self.root = Node()
        self.generate_trie(word)

    def generate_trie(self, word):
        """
        Function description:
        Insert all suffixes of the given text into the suffix trie

        :Input:
        word: A string representing the genome

        :Output, return or postcondition:
        The suffix trie is built from the text

        :Time Complexity:
        O(N^2)

        :Time Complexity Analysis:
        Each time we insert it can take up to O(N) time and there are N suffixes to insert
        So we get O(N^2) time

        :Space Complexity:
        O(N^2)

        :Space Complexity Analysis:
        Each suffix can create up to N new nodes => leading to N * (N+1) / 2 nodes
        which is O(N^2)

        :Auxiliary Space Complexity:
        O(N^2)

        :Auxiliary Space Complexity Analysis:
        The auxiliary space includes the nodes and their children which can be up to O(N^2)
        """
        n = len(word)
        for i in range(n):
            self.insert_suffix(word, i)

    def insert_suffix(self, word, start_index):
        """
        Function description:
        Insert a suffix starting at the given index into the trie

        :Input:
        word: A string representing the genome
        start_index: The starting index of the suffix to be inserted

        :Output, return or postcondition:
        The suffix starting at start_index is inserted into the trie.

        :Time Complexity:
        O(N)

        :Time Complexity Analysis:
        Inserting a suffix needs us to go through and potentially add nodes for each character in the suffix
        which takes linear time in the length of the suffix

        :Space Complexity:
        O(N)

        :Space Complexity Analysis:
        Each suffix can add up to N new nodes in the trie

        :Auxiliary Space Complexity:
        O(1)

        :Auxiliary Space Complexity Analysis:
        Only stores root
        """
        current = self.root
        for i in range(start_index, len(word)):
            index = ord(word[i]) - ord('A')  # Convert character to index (i.e. 'A'-> 0, 'B'-> 1, and so on)
            if not current.children[index]:
                current.children[index] = Node()  # Create a new node if necessary.

            current = current.children[index]
            current.indexes.append(start_index)  # Keep track of the starting index of the suffix

    def search(self, pattern):
        """
        Function description:
        Search for all occurrences of the pattern within the trie

        :Input:
        pattern: A pattern string that we need to search for in the trie

        :Output, return or postcondition:
        A list of start indexes where the pattern is found in the text

        :Time Complexity:
        O(T)

        :Time Complexity Analysis:
        Searching for a pattern needs us to go through the trie for each character in the pattern
        which takes linear time in the length of the pattern

        :Space Complexity:
        O(1)

        :Space Complexity Analysis:
        Only need to traverse the trie

        :Auxiliary Space Complexity:
        O(1)

        :Auxiliary Space Complexity Analysis:
        Only need to traverse the trie
        """
        current = self.root
        for char in pattern:
            index = ord(char) - ord('A')  # Convert character to index

            if not current.children[index]:
                return []  # Pattern not found
            current = current.children[index]

        return current.indexes  

class OrfFinder:
    def __init__(self, genome):
        """
        Function description:
        Initialize the OrfFinder object with the given genome and then
        generate the trie based off the given genome

        :Input:
        genome: A string representing the genome

        :Output, return or postcondition:
        Initializes an OrfFinder object

        :Time Complexity:
        O(N^2)

        :Time Complexity Analysis:
        The constructor of the OrfFinder calls the suffix trie's generate function which is O(N^2) at worst

        :Space Complexity:
        O(N^2)

        :Space Complexity Analysis:
        The space complexity is O(N^2) because the suffix trie structure can have up to N^2 vertices

        :Auxiliary Space Complexity:
        O(N^2)

        :Auxiliary Space Complexity Analysis:
        The auxiliary space includes the nodes and their children in the trie which can be up to O(N^2)
        """
        self.genome = genome
        self.suffix_trie = SuffixTrie(genome)

    def find(self, start, end):
        """
        Function description:
        Find all substrings in the genome that start with the given start pattern and end with the given end pattern

        Approach:
        The function first finds all positions in the genome where the start pattern occurs using teh search function in the suffix trie
        Then it finds all positions where the end pattern occurs also by using the search function
        For each starting position it checks every ending position to see if the end pattern occurs after the start pattern
        If True then it makes a substring from the starting position to the end position of the word and appends it to the result list


        :Input:
        start: A string representing the start pattern (prefix)
        end: A string representing the end pattern (suffix)

        :Output, return or postcondition:
        A list of substrings that start with start and end with end

        :Time Complexity:
        O(T + U + V)

        :Time Complexity Analysis:
        Searching for start and end takes O(T) and O(U) (respectively)
        Constructing the substrings takes O(V) where V is the total length of all substrings that we foundd

        :Space Complexity:
        O(V)

        :Space Complexity Analysis:
        The space complexity depends on the total length of all found substrings which is O(V).

        :Auxiliary Space Complexity:
        O(V)

        :Auxiliary Space Complexity Analysis:
        O(V), which is the total length of all substrings found which are in vertices
        """
        result = []
        start_positions = self.suffix_trie.search(start)  # Find all positions where start/prefix appears
        end_positions = self.suffix_trie.search(end)  # Find all positions where end/suffix appears

        for start_index in start_positions:
            for end_index in end_positions:
                if end_index >= start_index + len(start):  # Ensure the end part occurs after start 
                    orf = self.genome[start_index:end_index + len(end)]
                    result.append(orf)  

        return result


from collections import deque

class Vertex:
    def __init__(self, id, demand=0):
        """
        Represents a vertex in a network flow

        :Input:
        id: identifier for the vertex
        demand: demand of the vertex
        """
        self.id = id
        self.edges = []
        self.demand = demand  
        self.discovered = False # for bfs
        self.visited = False # for bfs
        self.prev = None # for backtracking to find a path
        self.allocation_idx = None # for allocation

    def __str__(self) -> str:
        return str(self.id)
    
    def __repr__(self) -> str:
        return self.id

class Edge:
    def __init__(self, u, v, capacity, lower_bounds, flow=0, is_reverse = False):
        """
        Represents an edge in a network flow
        
        :Input:
        u: The start vertex of the edge
        v: The end vertex of the edge
        capacity: The capacity of the edge
        lower_bounds: The lower bounds of the edge
        flow: The current flow through the edge
        is_reverse: A flag indicating if the edge is a reverse edge (when augmenting)
        """
        self.u = u  
        self.v = v  
        self.capacity = capacity  
        self.flow = flow  
        self.lower_bounds = lower_bounds 
        self.is_reverse = is_reverse # used to help when augmenting path

    def remaining_capacity(self):
        return self.capacity - self.flow

    def __repr__(self) -> str:
        return f"{self.u} -> {self.v}"
    
class NetworkFlow:
    def __init__(self, preferences, officers_per_org, min_shifts, max_shifts, days=30):
        """
        Function description:
        Initialize a NetworkFlow object creating vertices and edges to represent officers, days, and shifts.
        
        Approach:
        Structure I decided on: 
            Source -> Officers -> Days (act as intermediary to set capacity that each officer can only work once a day)
            -> Shifts (3 Shift Vertices per company)

        There will be 30 days nodes acting as intermediary between each officer and shift vertex where each edge has a capacity of 1
        to ensure that each officer can only work once a day



        :Input:
        preferences: A list of lists where preferences[i][k] is 1 if officer i prefers shift k, 0 otherwise
        officers_per_org: A list of lists where officers_per_org[j][k] is the number of officers needed by company j for shift k
        min_shifts: Minimum number of shifts an officer can work in a month
        max_shifts: Maximum number of shifts an officer can work in a month
        days: Number of days in the month (default is 30).

        :Output, return or postcondition:
        None, Initializes a NetworkFlow object with vertices and edges based on the given information regarding allocation needs

        :Time complexity:
        O(m * n * d)

        :Time complexity analysis:
        Creating the vertices and edges involves iterating over officers, companies, and days.

        :Space complexity:
        O(m * n * d)

        :Auxiliary space complexity:
        O(m * n * d)

        :Space complexity analysis:
        The overall space complexity depends on the vertices and edges created 
        There are m amount of companies, n amount of officers, and d amount of days
        So O(m * n * d)
        """
        self.vertices = []
        self.source = Vertex("source")
        self.sink = Vertex("sink")

        # Append Source
        self.vertices.append(self.source)        
        
        # Create vertices for officers
        self.officers = []
        for i in range(len(preferences)):
            officer_vertex = Vertex(f"Officer {i}")
            officer_vertex.allocation_idx = i # i'th officer
            
            self.officers.append(officer_vertex)
            self.vertices.append(officer_vertex)
            
            # Connect source to officer vertices
            # edge_to_officer = Edge(self.source, officer_vertex, max_shifts, min_shifts, 0)
            edge_to_officer = Edge(self.source, officer_vertex, max_shifts, min_shifts, 0)
            self.source.edges.append(edge_to_officer)

        # Create shift vertices
        total_officers_needed = 0
        self.shifts = []
        for i in range(len(officers_per_org)):
            company_shifts = []
            # 3 possible shifts per company
            for shift_idx in range(len(officers_per_org[i])):
                officers_needed = officers_per_org[i][shift_idx] * days # officers demanded per shift total for a month
                shift_vertex = Vertex(f"Company{i} Shift{shift_idx}", officers_needed)
                shift_vertex.allocation_idx = shift_idx # shift_idx'th shift

                total_officers_needed += officers_needed
                company_shifts.append(shift_vertex)
                self.vertices.append(shift_vertex)
                # Connect shift vertices to sink
                edge_to_sink = Edge(shift_vertex, self.sink, officers_needed, officers_needed, 0)
                # shift_vertex.edges.append(edge_to_sink)
            self.shifts.append(company_shifts)

            self.days = []
            # Connect officers to day vertices per company
            for j in range(len(preferences)):
                officer_vertex = self.officers[j]
                for day in range(days): 
                    # Create day vertices
                    day_vertex = Vertex(f"Company {i}/Officer {j}/Day {day}")
                    day_vertex.allocation_idx = day # day'th day
                    self.vertices.append(day_vertex)
                    
                    edge_to_day = Edge(officer_vertex, day_vertex, 1, 0, 0)
                    officer_vertex.edges.append(edge_to_day)

                    self.days.append(day_vertex)
                    # Connect day vertices to shift vertices
                    for shift_idx in range(len(officers_per_org[i])):
                        if preferences[j][shift_idx] == 1:
                            day_to_shift_edge = Edge(day_vertex, self.shifts[i][shift_idx], 1, 0, 0)
                            day_vertex.edges.append(day_to_shift_edge)
        
        self.source.demand = -(total_officers_needed)

    def reduce_network(self, preferences, officers_per_org, min_shifts, max_shifts, days=30):
        """
        Function description:
        Reduces a network until it has no lower bounds and no demands.

        :Input:
        preferences: A list of lists where preferences[i][k] is 1 if officer i prefers shift k, 0 otherwise
        officers_per_org: A list of lists where officers_per_org[j][k] is the number of officers needed by company j for shift k
        min_shifts: Minimum number of shifts an officer can work in a month
        max_shifts: Maximum number of shifts an officer can work in a month
        days: Number of days in the month (default is 30)

        :Output, return or postcondition:
        Returns a new NetworkFlow object representing the reduced network.

        :Time complexity:
        O(m * n * d)

        :Time complexity analysis:
        The reduction process involves iterating over vertices and edges to adjust capacities and demands.

        :Space complexity:
        O(m * n * d)

        :Auxiliary space complexity:
        O(m * n * d)

        :Space complexity analysis:
        The overall space complexity depends on the vertices and edges created 
        There are m companies, n officers, and d days
        So O(m * n * d) 
        """

        # Now we need to reduce until no lower bounds
        temp_network = NetworkFlow(preferences, officers_per_org, min_shifts, max_shifts)
        temp_network.super_source = Vertex("super_source")
        temp_network.super_sink = Vertex("super_sink")
        
        for v in temp_network.vertices:
            for edge in v.edges:
                capacity = edge.capacity
                lower_bounds = edge.lower_bounds
                remaining = capacity - lower_bounds
                
                # Update demand depending on outgoing/incoming lower bounds
                v.demand += lower_bounds
                edge.v.demand -= lower_bounds

                edge.capacity = remaining
                edge.lower_bounds = 0

        temp_network.vertices.insert(0, temp_network.super_source)
        temp_network.vertices.append(temp_network.super_sink)

        # Reduce to no demand    
        for v in temp_network.vertices:
            if v.demand < 0:
                temp_network.super_source.edges.append(Edge(temp_network.super_source, v, -(v.demand), 0))
            elif v.demand > 0:
                v.edges.append(Edge(v, temp_network.super_sink, v.demand, 0))
        
            v.demand = 0

        return temp_network
    
    def bfs(self, s):
        """
        Function description:
        Perform a BFS in order to augment a path from source to sink

        Approach:
        From the source (current vertex) vertex go through it's edges until you find an edge not discovered and has a remaining
        capacity of > 0 (means that flow can still go through)

        Replace current vertex with the edge's target vertex and repeat until you find the sink which means that there's a valid
        path from source to destination

        If it goes through everything and finds no way to reach the sink then that means there's no valid path from source to destination

        :Input:
        s: The source vertex

        :Output, return or postcondition:
        Returns True if an augmenting path is found or False otherwise

        :Time complexity:
        O(V + E)

        :Time complexity analysis:
        BFS traverses each vertex and edge once which means linear time complexity

        :Space complexity:
        O(V)

        :Auxiliary space complexity:
        O(V)

        :Space complexity analysis:
        The overall space complexity O(V) as the space is mainly used for the queue which at worst holds up to all vertices so O(V)
        """
        discovered = deque([s])
        s.visited = True
        while discovered:
            u = discovered.popleft()

            # When reach sink
            if u == self.vertices[-1]:
                return True
            
            for edge in u.edges:
                v = edge.v
                if edge.remaining_capacity() > 0 and not v.visited:
                    discovered.append(v)
                    v.visited = True
                    v.prev = u

        return False
        

    def bfs_reset(self):
        """
        Function description:
        Resets all nodes to allow for another BFS

        :Output, return or postcondition:
        None, resets the visited and previous properties of all vertices

        :Time complexity:
        O(V)

        :Time complexity analysis:
        Resetting the properties of each vertex takes linear time in the number of vertices

        :Space complexity:
        O(1)

        :Auxiliary space complexity:
        O(1)

        :Space complexity analysis:
        Constant as we're only resetting vertices
        """
        for vertice in self.vertices:
            vertice.discovered = False
            vertice.visited = False
            vertice.prev = None


    def find_path(self):
        """
        Function description:
        Backtrack to keep track of vertices for the path from sink to source

        Approach:
        Backtrack from the sink vertice until you reach the source, for each vertex in the path append it to the
        path list to keep track of the path taken

        :Output, return or postcondition:
        Returns a list of vertices representing the path found through BFS

        :Time complexity:
        O(V)

        :Time complexity analysis:
        Backtracking through the vertices needs us to visit each vertex in the path once

        :Space complexity:
        O(V)

        :Auxiliary space complexity:
        O(1)

        :Space complexity analysis:
        The space complexity is O(V) for storing the path, 
        Auxiliary space complexity is O(1) as no additional space is used
        """
        # Backtrack to keep track of vertices for the path
        path = []
        path.append(self.vertices[-1])

        # Backtrack until it reaches source vertice
        i = 0
        while path[i] is not self.source and path[i] is not self.super_source:
            path.append(path[i].prev)
            i += 1
        
        return path

    def find_max_flow(self, path):
        max_flow = float('inf')
        n = len(path)-1
        for i in range(len(path) - 1): # -1 to stop when reaching source
            curr = path[n - i]
            next_vertex = path[n - (i+1)]
            for i in range(len(curr.edges)):
                edge = curr.edges[i]
                if edge.v == next_vertex:
                    if edge.capacity < max_flow:
                        max_flow = edge.capacity  

        # Add flow throughout the path
        for i in range(len(path) - 1): # -1 to stop when reaching source
            curr = path[n - i]
            next_vertex = path[n - (i+1)]
            for i in range(len(curr.edges)):
                edge = curr.edges[i]
                if edge.v == next_vertex:
                    edge.flow += max_flow
                    edge.capacity += max_flow 

        return max_flow
        
    def augment_path(self, path, max_flow):
        """
        Function description:
        Augment the given path in the network

        Approach:
        Go through the path found and for every forward edge, negate it's capacity by the max-flow (or min capacity) found
        through path_max_flow function given in the parameter (already done in ford-fulkerson function)
        
        Then create a backwards edge with a capacity of the max-flow found earlier
        This backwards edge allows for reallocation if a shift isn't fully satisfied
        If already has a backward edge then increase the edge's capacity by the max-flow

        :Input:
        path: A list of vertices representing the path taken from BFS
        max_flow: The maximum flow to augment along the path

        :Output, return or postcondition:
        None, augments the path taken in the network

        :Time complexity:
        O(V)

        :Time complexity analysis:
        Augmenting the flow involves visiting each edge in the path once

        :Space complexity:
        O(1)

        :Auxiliary space complexity:
        O(1)

        :Space complexity analysis:
        Only stores a few variables (int, bool, ..) so its constant
        """
        n = len(path)-1

        # Augment the path
        for i in range(len(path) - 1):
            curr = path[n - i]
            next_vertex = path[n - (i+1)]

            # Find edge that connects to the next vertex in the path
            for edge in curr.edges:
                if edge.v == next_vertex:
                    flag = False

                    # Check for existing reverse edge from next vertex
                    for j in range(len(next_vertex.edges)):
                        next_edge = next_vertex.edges[j]
                        if next_edge.v.id == curr.id:
                            next_vertex.edges[j].capacity += max_flow
                            next_vertex.edges[j].is_reverse = True
                            flag = True
                            reverse_edge = next_vertex.edges[j]

                    if flag == False:
                        reverse_edge = Edge(next_vertex, curr, max_flow, 0, 0, True)
                        next_vertex.edges.append(reverse_edge)

                    edge.capacity = edge.capacity - max_flow

    def ford_fulkerson(self, preferences, officers_per_org, min_shifts, max_shifts):
        """
        Function description:
        ford-fulkerson algorithm to find the maximum flow in the network

        Approach:
        While a BFS can still be performed:
        - Get max-flow from path found through BFS then increment max_flow (for valid check later on)
        - Augment the path found through the BFS

        After doing so, for each edge in the vertice increase its flow by its lower bounds then network should be processed
        Check if  its valid by going through officers_per_org and finding the total amount of officers needed for shifts
        If max-flow is equal to the total then its valid, invalid if max-flow is less

        :Input:
        preferences: A list of lists where preferences[i][k] is 1 if officer i prefers shift k, 0 otherwise
        officers_per_org: A list of lists where officers_per_org[j][k] is the number of officers needed by company j for shift k
        min_shifts: Minimum number of shifts an officer can work in a month
        max_shifts: Maximum number of shifts an officer can work in a month

        :Output, return or postcondition:
        Returns the reduced network after applying ford-fulkerson on the network
        None if it doesn't pass the check as max-flow should equal to the amount of officers needed in total

        :Time complexity:
        O(E * F)

        :Time complexity analysis:
        The while loop runs until there is no augmenting path
        in the worst case the number of augmenting paths can be the maximum flow value F
        Each BFS takes O(E) time

        :Space complexity:
        O(V + E)

        :Auxiliary space complexity:
        O(V)

        :Space complexity analysis:
        The space complexity depends on the vertices and edges so O(V + E)
        The auxiliary space complexity is O(V) for the BFS queue
        """
        reduced_network = self.reduce_network(preferences, officers_per_org, min_shifts, max_shifts)
        source = reduced_network.super_source

        max_flow = 0
        # Augment residual
        while reduced_network.bfs(source):
            # Get path
            path = reduced_network.find_path()

            # Find max flow (min edge capacity) from the path
            flow = reduced_network.find_max_flow(path)

            # Augment the path
            reduced_network.augment_path(path, flow)
            max_flow += flow
            reduced_network.bfs_reset()

        # Add lower bounds
        for v in self.vertices:
            for edge in v.edges:
                edge.flow += edge.lower_bounds        

        officers_needed = 0
        for i in range(len(officers_per_org)):
            for j in range(len(officers_per_org[i])):
                officers_needed += officers_per_org[i][j] * 30

        if officers_needed > max_flow:
            return None
        
        return reduced_network


def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    """
    Function description:
    Allocate officers to company shifts on a said day based off their preferences and the company's requirements
    
    Approach:
    Initialize a network then perform ford fulkerson on it. After getting appropriate flow distribution (or None if invalid allocation checked in ford-fulkerson function)
    we go through each officer check which edge has a flow towards the day vertices, if it has flow go through each shift the edge is connected to
    then check whether theres flow. If theres flow then the officer is working at that shift at that particular day.

    :Input:
    preferences: A list of lists where preferences[i][k] is 1 if officer i prefers shift k, 0 otherwise
    officers_per_org: A list of lists where officers_per_org[j][k] is the number of officers needed by company j for shift k
    min_shifts: Minimum number of shifts an officer can work in a month
    max_shifts: Maximum number of shifts an officer can work in a month

    :Output, return or postcondition:
    Returns a 4d list representing the allocation of officers to a company's shifts on certain days or None if no valid allocation exists

    :Time complexity:
    O(n * m * d)

    :Time complexity analysis:
    The worst case time complexity of the allocation is O(n * m * d) because we'll need to go through each officer (n),
    each day (d) and then each shift. The amount of shifts  and day vertices depends on the amount of companies (m).

    :Space complexity:
        O(m * n * d)

    :Auxiliary space complexity:
        O(m * n * d)

    :Space complexity analysis:
    The total space complexity is determined by the vertices and edges created
    There are m companies, n officers, and d days, so O(m * n * d) vertices and edges
    """
    days = 30
    network_flow = NetworkFlow(preferences, officers_per_org, min_shifts, max_shifts, days)
    processed_network_flow = network_flow.ford_fulkerson(preferences, officers_per_org, max_shifts, min_shifts)    
    
    if processed_network_flow == None: # The check for valid allocation / max-flow occurs in the ford-fulkerson function
        return None

    # [i][j][d][k]
    # i = officer, j = company, d = day, k = shift
    shift_per_day = len(officers_per_org[0])
    allocation = [[[[0 for _ in range(shift_per_day)] for _ in range(days)] for _ in range(len(officers_per_org))] for _ in range(len(preferences))]

    for officer in processed_network_flow.officers:
        i = 0
        c = 0
        officer_idx =  officer.allocation_idx
        for edge in officer.edges:
            if edge.flow > 0:
                day = edge.v
                day_idx = day.allocation_idx
                for day_edge in day.edges:
                    if day_edge.flow > 0 and day_edge.is_reverse == False:
                        shift = day_edge.v
                        shift_idx = shift.allocation_idx
                        allocation[officer_idx][c][day_idx][shift_idx] = 1
            
            i += 1
            if i % days == 0:
                # Increment company number every 30 days
                c += 1

    return allocation
