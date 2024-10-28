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
    def __init__(self, u, v, capacity, lower_bounds, flow=0, is_reverse=False):
        self.u = u  
        self.v = v  
        self.capacity = capacity  
        self.flow = flow  
        self.lower_bounds = lower_bounds 
        self.is_reverse = is_reverse

    def remaining_capacity(self):
        return self.capacity - self.flow

    def __repr__(self) -> str:
        return f"{self.u} -> {self.v} (cap: {self.capacity}, flow: {self.flow})"

class NetworkFlow:
    def __init__(self, preferences, officers_per_org, min_shifts, max_shifts, days=30):
        self.vertices = []
        self.source = Vertex("source")
        self.sink = Vertex("sink")
        self.vertices.append(self.source)
        
        self.officers = []
        for i in range(len(preferences)):
            officer_vertex = Vertex(f"officer_{i}", -(max_shifts - min_shifts))
            officer_vertex.allocation_idx = i
            self.officers.append(officer_vertex)
            self.vertices.append(officer_vertex)
            edge_to_officer = Edge(self.source, officer_vertex, max_shifts, min_shifts)
            self.source.edges.append(edge_to_officer)

        self.shifts = []
        for i in range(len(officers_per_org)):
            for shift_idx in range(len(officers_per_org[i])):
                officers_needed = officers_per_org[i][shift_idx] * days
                shift_vertex = Vertex(f"company_{i}_shift_{shift_idx}", officers_needed)
                shift_vertex.allocation_idx = shift_idx
                self.shifts.append(shift_vertex)
                self.vertices.append(shift_vertex)
                edge_to_sink = Edge(shift_vertex, self.sink, officers_needed, officers_needed)
                shift_vertex.edges.append(edge_to_sink)

        self.days = []
        for i in range(len(officers_per_org)):
            for j in range(len(preferences)):
                officer_vertex = self.officers[j]
                for day in range(days): 
                    day_vertex = Vertex(f"company_{i}_officer_{j}_day_{day}")
                    day_vertex.allocation_idx = day
                    self.vertices.append(day_vertex)
                    edge_to_day = Edge(officer_vertex, day_vertex, 1, 0)
                    officer_vertex.edges.append(edge_to_day)
                    self.days.append(day_vertex)
                    for shift_idx in range(len(officers_per_org[i])):
                        if preferences[j][shift_idx] == 1:
                            day_to_shift_edge = Edge(day_vertex, self.shifts[i*len(officers_per_org[i]) + shift_idx], 1, 0)
                            day_vertex.edges.append(day_to_shift_edge)

    def reduce_network(self, preferences, officers_per_org, min_shifts, max_shifts):
        temp_network = NetworkFlow(preferences, officers_per_org, min_shifts, max_shifts)
        temp_network.super_source = Vertex("super_source")
        temp_network.super_sink = Vertex("super_sink")

        for v in temp_network.vertices:
            for edge in v.edges:
                capacity = edge.capacity
                lower_bounds = edge.lower_bounds
                remaining = capacity - lower_bounds
                edge.capacity = remaining
                edge.lower_bounds = 0

        temp_network.vertices[0] = temp_network.super_source
        temp_network.vertices[-1] = temp_network.super_sink
    
        for v in temp_network.vertices:
            if v.demand < 0:
                temp_network.super_source.edges.append(Edge(temp_network.super_source, v, -(v.demand), 0))
            elif v.demand > 0:
                v.edges.append(Edge(v, temp_network.super_sink, v.demand, 0))
            v.demand = 0

        return temp_network
    
    def bfs(self, s):
        discovered = deque([s])
        s.visited = True

        while discovered:
            u = discovered.popleft()

            if u == self.sink:
                return True
            
            for edge in u.edges:
                v = edge.v
                if edge.remaining_capacity() > 0 and not v.visited:
                    discovered.append(v)
                    v.visited = True
                    v.prev = u

        return False

    def bfs_reset(self):
        for vertice in self.vertices:
            vertice.visited = False
            vertice.prev = None

    def find_path(self):
        path = []
        v = self.sink

        while v.prev is not None:
            path.append(v)
            v = v.prev
        path.append(self.source)
        
        if path[-1] != self.source:
            return None
        return path[::-1]

    def augment_path(self, path):
        min_flow = float('inf')
        for i in range(len(path) - 1):
            for edge in path[i].edges:
                if edge.v == path[i + 1]:
                    min_flow = min(min_flow, edge.remaining_capacity())

        for i in range(len(path) - 1):
            for edge in path[i].edges:
                if edge.v == path[i + 1]:
                    edge.flow += min_flow
            for edge in path[i + 1].edges:
                if edge.v == path[i]:
                    edge.flow -= min_flow
                    break
            else:
                path[i + 1].edges.append(Edge(path[i + 1], path[i], 0, 0, -min_flow, True))

        return min_flow

    def ford_fulkerson(self, preferences, officers_per_org, min_shifts, max_shifts):
        residual_network = self.reduce_network(preferences, officers_per_org, min_shifts, max_shifts)
        source = residual_network.super_source

        max_flow = 0
        while residual_network.bfs(source):
            path = residual_network.find_path()
            if path:
                flow = residual_network.augment_path(path)
                max_flow += flow
                residual_network.bfs_reset()
            else:
                break

        for v in self.vertices:
            for edge in v.edges:
                if edge.flow > 0:
                    for r_edge in residual_network.vertices:
                        if r_edge.id == edge.v.id:
                            for redge in r_edge.edges:
                                if redge.v.id == v.id and redge.is_reverse:
                                    edge.flow += redge.flow

def allocate(preferences, officers_per_org, min_shifts, max_shifts):
    days = 30
    network_flow = NetworkFlow(preferences, officers_per_org, min_shifts, max_shifts)
    network_flow.ford_fulkerson(preferences, officers_per_org, max_shifts, min_shifts)    

    shift_per_day = len(officers_per_org[0])
    allocation = [[[[0 for _ in range(shift_per_day)] for _ in range(days)] for _ in range(len(officers_per_org))] for _ in range(len(preferences))]
    c = 0
    for i in range(len(preferences)):
        officer = network_flow.officers[i]
        for edge in officer.edges:
            if edge.flow > 0:
                day = edge.v
                for shift_edge in day.edges:
                    if shift_edge.flow > 0:
                        allocation[i][c][day.allocation_idx][shift_edge.v.allocation_idx] = 1

    return network_flow
def print_network(network):
    for vertex in network.vertices:
        print(f"Vertex {vertex.id} (demand: {vertex.demand}):")
        for edge in vertex.edges:
            if edge.flow > 0:
                print(f"\t{edge.u.id} -> {edge.v.id} | Capacity: {edge.capacity} | LB: {edge.lower_bounds} | Flow: {edge.flow} | Remaining capacity: {edge.remaining_capacity()}")
if __name__ == "__main__":
    preferences = [
        [0, 1, 1],
        [1, 0, 0],
        [1, 1, 0],
        [1, 1, 0],
    ]
    officers_per_org = [[1, 1, 1]]
    min_shifts = 0
    max_shifts = 30

    allocation = allocate(preferences, officers_per_org, min_shifts, max_shifts)
    print_network(allocation)
    # for officer_idx, officer_allocation in enumerate(allocation):
    #     print(f"Officer {officer_idx}:")
    #     for company_idx, company_allocation in enumerate(officer_allocation):
    #         for day_idx, day_allocation in enumerate(company_allocation):
    #             for shift_idx, shift_allocation in enumerate(day_allocation):
    #                 if shift_allocation == 1:
    #                     print(f"\tDay {day_idx}, Company {company_idx}, Shift {shift_idx}")
