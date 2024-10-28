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
        x = 1
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

if __name__ == "__main__":
    pass
    preferences = [[0, 0, 1],
                            [1, 1, 0], [1, 1, 1],
                            [1, 0, 0],
                            [1, 1, 1],
                            [1, 0, 0], [0, 1, 0], [1, 0, 1], [0, 1, 0], [0, 1, 1], [0, 1, 1], [0, 1, 1], [1, 1, 0], [0, 1, 0], [1, 0, 0], [1, 1, 1], [1, 1, 0], [0, 1, 0]]
    officers_per_org = [[5, 3, 4], [2, 1, 1]]
    min_shifts = 25
    max_shifts = 28
    

    network = NetworkFlow(preferences, officers_per_org, min_shifts, max_shifts)
    network = network.ford_fulkerson(preferences, officers_per_org, min_shifts, max_shifts)

    # for edge in network.officers[9].edges:
    #     for day_edge in edge.v.edges:
    #         if day_edge.flow > 0:
    #             print(day_edge)
    # print_network(network)    

    # allocation = allocate(preferences, officers_per_org, min_shifts, max_shifts)
    # print(allocation)
     
    

    # print_network(reduced_network)

    # for edge in network.shifts[2].edges:
    #     edge.capacity
    # print(network.shifts[2].edges)
    # print_network(reduced_network)

    # print_network(allocate(preferences, officers_per_org, min_shifts, max_shifts))
