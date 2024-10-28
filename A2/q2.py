from collections import deque

class Vertex:
    def __init__(self, id, demand=0):
        self.id = id
        self.edges = []
        self.demand = demand  
        self.discovered = False
        self.visited = False
        self.prev = None
        self.allocation_idx = None

    def __str__(self) -> str:
        return str(self.id)
    
    def __repr__(self) -> str:
        return self.id

class Edge:
    def __init__(self, u, v, capacity, lower_bounds, flow=0, is_reverse = False):
        self.u = u  
        self.v = v  
        self.capacity = capacity  
        self.flow = flow  
        self.lower_bounds = lower_bounds 
        self.is_reverse = is_reverse # used to help display when augmenting path

    def remaining_capacity(self):
        return self.capacity - self.flow

    def __repr__(self) -> str:
        return f"{self.u} -> {self.v}"
    
class NetworkFlow:
    """
    Structure:
    source -> officers -> days (to set constraint 1 shift per day per officer) -> shifts (3 per company) -> sink
    """
    def __init__(self, preferences, officers_per_org, min_shifts, max_shifts, days=30):
        self.vertices = []
        self.source = Vertex("source")
        self.sink = Vertex("sink")

        # Append Source
        self.vertices.append(self.source)        
        
        # Create vertices for officers
        self.officers = []
        for i in range(len(preferences)):
            officer_vertex = Vertex(f"officer_{i}")
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
                shift_vertex = Vertex(f"company_{i}_shift_{shift_idx}", officers_needed)
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
                    day_vertex = Vertex(f"company_{i}_officer_{j}_day_{day}")
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
        Reduces a network until it has no lower bounds and no demands
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

        # temp_network.super_source.edges.append(Edge(temp_network.super_source, temp_network.source, (temp_network.source.demand), 0))
    
        for v in temp_network.vertices:
            if v.demand < 0:
                temp_network.super_source.edges.append(Edge(temp_network.super_source, v, -(v.demand), 0))
            elif v.demand > 0:
                v.edges.append(Edge(v, temp_network.super_sink, v.demand, 0))

            v.demand = 0

        # Check if possible
        for edge in temp_network.source.edges:
            if edge.v == temp_network.super_sink:
                return None

        return temp_network
    
    def bfs(self, s):
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
        Resets all nodes to allow for another BFS.
        """
        for vertice in self.vertices:
            vertice.discovered = False
            vertice.visited = False
            vertice.prev = None


    def find_path(self):
        # Backtrack to keep track of vertices for the path
        path = []
        path.append(self.vertices[-1])

        # Backtrack until it reaches source vertice
        i = 0
        while path[i] is not self.source and path[i] is not self.super_source:
            path.append(path[i].prev)
            i += 1

        # If there's no path
        # print(path)
        # if path[0] != self.vertices[-1] or path[-1] != self.vertices[0]:
        #     return None
        
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

        for i in range(len(path) - 1): # -1 to stop when reaching source
            curr = path[n - i]
            next_vertex = path[n - (i+1)]
            for i in range(len(curr.edges)):
                edge = curr.edges[i]
                if edge.v == next_vertex:
                    edge.flow += max_flow 

        return max_flow
        
    def augment_path(self, path, max_flow, original = None):
        n = len(path)-1
        reverse_edge_list = []
        # Augment the path
        for i in range(len(path) - 1):
            curr = path[n - i]
            next_vertex = path[n - (i+1)]

            # Find edge that connects to the next vertex in the path
            for edge in curr.edges:
                if edge.v == next_vertex:
                    connected_edge = edge
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

            # Update
             
        return max_flow

    def ford_fulkerson(self, preferences, officers_per_org, min_shifts, max_shifts):
        reduced_network = self.reduce_network(preferences, officers_per_org, min_shifts, max_shifts)

        if reduced_network == None:
            return None

        source = reduced_network.super_source

        max_flow = 0
        # Augment residual
        while reduced_network.bfs(source):
            # Get path
            path = reduced_network.find_path()

            # Find max flow (min edge capacity) from the path
            flow = reduced_network.find_max_flow(path)

            # Augment the path
            reduced_network.augment_path(path, flow, self)
            max_flow += flow
            reduced_network.bfs_reset()

        # Add lower bounds
        for v in self.vertices:
            for edge in v.edges:
                edge.flow += edge.lower_bounds        

        return reduced_network


# Helper for display
def print_network(network):
    for vertex in network.vertices:
        print(f"Vertex {vertex.id} (demand: {vertex.demand}):")
        for edge in vertex.edges:
            if not edge.is_reverse:
                print(f"\t{edge.u.id} -> {edge.v.id} | Capacity: {edge.capacity} | LB: {edge.lower_bounds} | Flow: {edge.flow} | Remaining capacity: {edge.remaining_capacity()}")

def print_reverse(network):
    for vertex in network.vertices:
        print(f"Vertex {vertex.id} (demand: {vertex.demand}):")
        for edge in vertex.edges:
            if edge.is_reverse:
                print(f"\t{edge.u.id} -> {edge.v.id} | Capacity: {edge.capacity} | Flow: {edge.flow} | Remaining capacity: {edge.remaining_capacity()} | Reverse: {edge.is_reverse}")


def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    days = 30
    network_flow = NetworkFlow(preferences, officers_per_org, min_shifts, max_shifts, days)
    processed_network_flow = network_flow.ford_fulkerson(preferences, officers_per_org, max_shifts, min_shifts)    

    if processed_network_flow == None:
        return None
    
    # [i][j][d][k]
    # i = officer, j = company, d = day, k = shift
    shift_per_day = len(officers_per_org[0])
    allocation = [[[[0 for _ in range(shift_per_day)] for _ in range(days)] for _ in range(len(officers_per_org))] for _ in range(len(preferences))]

    for officer in processed_network_flow.officers:
        for edge in officer.edges:
            if edge.flow > 0:
                day_vertex = edge.v
                for shift_edge in day_vertex.edges:
                    if shift_edge.flow > 0:
                        company_idx = int(shift_edge.v.id.split('_')[1])
                        shift_idx = shift_edge.v.allocation_idx
                        allocation[officer.allocation_idx][company_idx][day_vertex.allocation_idx][shift_idx] = 1
        
    return allocation

    # for i in range(len(preferences)): # Officer
    #     for j in range(len(officers_per_org)): # Company
    #         for day in range(days):
    #             for k in range(shift_per_day):
    #                 pass
    
    return network_flow

if __name__ == "__main__":
    pass

    # Example usage
    preferences = [
        [0, 1, 1],
        [1, 1, 0],
        [1, 0, 0],
        [1, 1, 0],
    ]
    officers_per_org = [[1, 1, 1]]
    min_shifts = 0
    max_shifts = 30

    network = NetworkFlow(preferences, officers_per_org, min_shifts, max_shifts)

    # print(network.vertices[0].edges[0].remaining_capacity())
    reduced_network = network.reduce_network(preferences, officers_per_org, min_shifts, max_shifts)
    ret_network = network.ford_fulkerson(preferences, officers_per_org, min_shifts, max_shifts)
    
    # print_network(ret_network)

    # allocation = allocate(preferences, officers_per_org, min_shifts, max_shifts)
    # print_network(allocation)
    # print(allocation)
    

    # print_network(reduced_network)

    # for edge in network.shifts[2].edges:
    #     edge.capacity
    # print(network.shifts[2].edges)
    # print_network(reduced_network)

    # print_network(allocate(preferences, officers_per_org, min_shifts, max_shifts))
