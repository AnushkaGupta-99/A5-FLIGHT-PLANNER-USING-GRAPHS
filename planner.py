from flight import Flight

class Planner:
    def __init__(self, flights):
        """The Planner

        Args:
            flights (List[Flight]): A list of information of all the flights (objects of class Flight)
        """
        #O(m) where m is the number of flights, note that n is O(m) #build an adjacency list
        self.flights=flights
        self.m=len(flights)  #number of flights
        self.n = max(flight.end_city for flight in flights) + 1
        self.city_list = []
        for _ in range(self.m):
            self.city_list.append([])
        #city list is an adjacency list where each index is a list which contains all the flights that depart from city with that index
        for i in flights:
            self.city_list[i.start_city].append(i)       
        pass
    
    def least_flights_earliest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=), satisfying:
        The route has the least number of flights, and within routes with the same number of flights,
        arrives the earliest.
        """
        # Queue elements ka format (current_city, current_time, num_flights, last_flight)
        queue = Queue()
        queue.enqueue((start_city, t1, 0, None))  # initial city se start kar rahe hai 

        # To track the min flight ye create kiya hai 
        min_flights = [float('inf')] * len(self.city_list)
        earliest_arrival = [float('inf')] * len(self.city_list)
        min_flights[start_city] = 0
        last_flight_to_city = [None] * len(self.city_list)

        while queue.is_empty()==False:
            city, current_time, num_flights, last_flight = queue.dequeue()

            # Explore outgoing flights from the current city
            for flight in self.city_list[city]:
                if num_flights == 0:  # First flight
                    if flight.departure_time >= t1 and flight.arrival_time <= t2:
                        new_num_flights = 1
                        if (new_num_flights < min_flights[flight.end_city] or
                                (new_num_flights == min_flights[flight.end_city] and
                                flight.arrival_time < earliest_arrival[flight.end_city])):
                            min_flights[flight.end_city] = new_num_flights
                            earliest_arrival[flight.end_city] = flight.arrival_time
                            last_flight_to_city[flight.end_city] = flight
                            queue.enqueue((flight.end_city, flight.arrival_time, new_num_flights, flight))
                else:  # Connecting flight
                    if (flight.departure_time >= current_time + 20 and
                            flight.arrival_time <= t2):
                        new_num_flights = num_flights + 1
                        if (new_num_flights < min_flights[flight.end_city] or
                                (new_num_flights == min_flights[flight.end_city] and
                                flight.arrival_time < earliest_arrival[flight.end_city])):
                            min_flights[flight.end_city] = new_num_flights
                            earliest_arrival[flight.end_city] = flight.arrival_time
                            last_flight_to_city[flight.end_city] = flight
                            queue.enqueue((flight.end_city, flight.arrival_time, new_num_flights, flight))

        # Reconstruct the path if a valid route exists
        if min_flights[end_city] == float('inf'):
            return []
        best_path = []
        current_city = end_city
        while last_flight_to_city[current_city] is not None:
            best_path.append(last_flight_to_city[current_city])
            current_city = last_flight_to_city[current_city].start_city

        best_path.reverse()
        return best_path

    def cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        #O(mlogm)
        #BFS then Dijkstra’s Algorithm
        #Queue ke elements ka format hoga(city, num_flights, current_time, total_cost, path)#heap mei special comparator function use ho rha hai
        heap = MinHeap()
        best_flight_tuple = None
        visited_flights = [None]*(self.m+1)
        #Push the starting city with 0 flights and 0 cost
        heap.push((0, start_city, t1,None))  # (total_cost, city, curr_time, path)
        n = len(self.city_list)
        # To keep track of the minimum cost for (city, num_flights)
        # Initialize min_cost as a list with tuples (float('inf'), float('inf'))
        min_cost = []
        flag = 0
        for i in range(n):
            min_cost.append(float('inf'))

        min_cost[start_city] = 0 # Minimum cost to reach start_city with 0 flights is 0

        while not heap.is_empty():
            total_fare, city, curr_time, flight_tuple = heap.pop()
            #print(f"city is {city}, total_fare is {total_fare[0], total_fare[1]}")
            if city == end_city:
                if min_cost[end_city] == float('inf'):
                    #print(f" flight_no. {flight_tuple[0].flight_no}")
                    min_cost[end_city] = total_fare
                    best_flight_tuple = flight_tuple
                elif total_fare < min_cost[end_city]:
                    min_cost[end_city] = total_fare
                    best_flight_tuple = flight_tuple
                #elif total_fare[0] == min_cost[end_city][0] and total_fare[1] < min_cost[end_city][1]:
                #    min_cost[end_city] = total_fare
                #    best_flight_tuple = flight_tuple
                else:
                    pass
            
            for flight in self.city_list[city]:
                if flag == 0:#for the first flight
                    if flight.departure_time>=t1 and flight.arrival_time <= t2:
                        #new_flight_no=1
                        new_fare=total_fare+flight.fare  
                        new_cost=new_fare                     
                        flight_tuple=(flight,None)#flight_tuple stores current and previous flight
                        #visited_flights[flight.]=
                        #if visited_flights[flight.flight_no]
                        visited_flights[flight.flight_no] = flight_tuple
                        heap.push((new_cost, flight.end_city, flight.arrival_time, flight_tuple))
                        #print(f"pushed flight into heap {flight.flight_no}")

                else:#for the 20 min wait
                    last_arrival=flight_tuple[0].arrival_time #to check for next flight
                    if flight.departure_time>=last_arrival+20 and flight.arrival_time <= t2 and visited_flights[flight.flight_no] == None:
                        #new_flight_no=total_fare[0]+1
                        new_fare=total_fare+flight.fare
                        new_cost=new_fare
                        new_flight_tuple=(flight,flight_tuple[0])
                        visited_flights[flight.flight_no] = new_flight_tuple
                        heap.push((new_cost, flight.end_city, flight.arrival_time,new_flight_tuple))
                        #print(f"pushed flight into heap {flight.flight_no}")
                        '''if path!=None:
                                heap.push((new_cost, flight.end_city, flight.arrival_time, path.append(flight)))
                            else:
                                heap.push((new_cost, flight.end_city, flight.arrival_time, [flight]))'''
            flag = 1

        if best_flight_tuple == None:
            return []
        else:
            best_path = []
            flight_tuple = best_flight_tuple
            while True: #curr_city != flight_tuple[0].start_city:
                    best_path.append(flight_tuple[0])
                    if flight_tuple[1] == None:
                        break
                    flight_tuple = visited_flights[flight_tuple[1].flight_no]
            best_path.reverse() 
            return best_path
#NOTES:HERE THE KEY FOR COMPARISON IS 0TH INDEX OF ELEMENT ADDED IN HEAP
#YOU WILL HAVE TO CHANGE TO ACC TO YOUR '''
    
    
    
    
    def least_flights_cheapest_route(self, start_city, end_city, t1, t2):
        """
        Return List[Flight]: A route from start_city to end_city, which departs after t1 (>= t1) and
        arrives before t2 (<=) satisfying: 
        The route has the least number of flights, and within routes with same number of flights, 
        is the cheapest
        """
        #O(mlogm)
        #BFS then Dijkstra’s Algorithm
        #Queue ke elements ka format hoga(city, num_flights, current_time, total_cost, path)#heap mei special comparator function use ho rha hai
        heap = MinHeap(compare_noofflights_then_cost)
        best_flight_tuple = None
        visited_flights = [None]*(self.m+1)
        #Push the starting city with 0 flights and 0 cost
        heap.push(((0, 0), start_city, t1,None))  # ((num_flights, total_cost), city, curr_time, path)
        n = len(self.city_list)
        # To keep track of the minimum cost for (city, num_flights)
        # Initialize min_cost as a list with tuples (float('inf'), float('inf'))
        min_cost = []
        flag = 0
        for i in range(n):
            min_cost.append((float('inf'), float('inf')))

        min_cost[start_city] = (0,0)  # Minimum cost to reach start_city with 0 flights is 0

        while not heap.is_empty():
            total_fare, city, curr_time, flight_tuple = heap.pop()
            #print(f"city is {city}, total_fare is {total_fare[0], total_fare[1]}")
            if city == end_city:
                if min_cost[end_city] == (float('inf'), float('inf')):
                    #print(f" flight_no. {flight_tuple[0].flight_no}")
                    min_cost[end_city] = total_fare
                    best_flight_tuple = flight_tuple
                elif total_fare[0] < min_cost[end_city][0]:
                    min_cost[end_city] = total_fare
                    best_flight_tuple = flight_tuple
                elif total_fare[0] == min_cost[end_city][0] and total_fare[1] < min_cost[end_city][1]:
                    min_cost[end_city] = total_fare
                    best_flight_tuple = flight_tuple
                else:
                    pass
            
            for flight in self.city_list[city]:
                if flag == 0:#for the first flight
                    if flight.departure_time>=t1 and flight.arrival_time <= t2:
                        new_flight_no=1
                        new_fare=total_fare[1]+flight.fare  
                        new_cost=(new_flight_no,new_fare)                     
                        flight_tuple=(flight,None)#flight_tuple stores current and previous flight
                        #visited_flights[flight.]=
                        visited_flights[flight.flight_no] = flight_tuple
                        heap.push((new_cost, flight.end_city, flight.arrival_time, flight_tuple))
                        #print(f"pushed flight into heap {flight.flight_no}")

                else:#for the 20 min wait
                    last_arrival=flight_tuple[0].arrival_time #to check for next flight
                    if flight.departure_time>=last_arrival+20 and flight.arrival_time <= t2 and visited_flights[flight.flight_no] == None:
                        new_flight_no=total_fare[0]+1
                        new_fare=total_fare[1]+flight.fare
                        new_cost=(new_flight_no,new_fare)
                        new_flight_tuple=(flight,flight_tuple[0])
                        visited_flights[flight.flight_no] = new_flight_tuple
                        heap.push((new_cost, flight.end_city, flight.arrival_time,new_flight_tuple))
                        #print(f"pushed flight into heap {flight.flight_no}")
                        '''if path!=None:
                                heap.push((new_cost, flight.end_city, flight.arrival_time, path.append(flight)))
                            else:
                                heap.push((new_cost, flight.end_city, flight.arrival_time, [flight]))'''
            flag = 1

        if best_flight_tuple == None:
            return []
        else:
            best_path = []
            flight_tuple = best_flight_tuple
            while True: #curr_city != flight_tuple[0].start_city:
                    best_path.append(flight_tuple[0])
                    if flight_tuple[1] == None:
                        break
                    flight_tuple = visited_flights[flight_tuple[1].flight_no]
            best_path.reverse() 
            return best_path
#NOTES:HERE THE KEY FOR COMPARISON IS 0TH INDEX OF ELEMENT ADDED IN HEAP
#YOU WILL HAVE TO CHANGE TO ACC TO YOUR '''

def default_comparison(a,b):
    if a[0]<b[0]:
        return True
    else:
        return False

def compare_noofflights_then_cost(a,b):
    if a[0][0]<b[0][0]:
        return True
    elif a[0][0]==b[0][0]:
        if a[0][1]<b[0][1]:
            return True #when the number of flights used are the same, then the cost is compared
        else:
            return False
    else:
        return False


class MinHeap:
    def __init__(self,comparator_function=default_comparison):
        self.comparator_function=comparator_function
        self.heap=[]
        #list of elementss
    
    
    def push(self,item):
        self.heap.append(item)
        self._heapify_up(len(self.heap)-1)

    def pop(self):
        if not self.heap:
            return None
        if len(self.heap)==1:
            return self.heap.pop()
        root=self.heap[0]
        self.heap[0]=self.heap.pop()
        #you will move the last element to the root and heapify down
        self._heapify_down(0)
        return root
    
    def _heapify_up(self,index):
        parent=(index-1)//2
        if index>0 and self.comparator_function(self.heap[index],self.heap[parent]):
            self.heap[index],self.heap[parent]=self.heap[parent],self.heap[index]
            self._heapify_up(parent)
    
    def _heapify_down(self,index):
        smallest = index
        left = 2 * index + 1
        right = 2 * index + 2

        if left < len(self.heap) and self.comparator_function(self.heap[left],self.heap[smallest]):
            smallest = left
        if right < len(self.heap) and self.comparator_function(self.heap[right],self.heap[smallest]):
            smallest = right

        if smallest != index:
            self.heap[index], self.heap[smallest] = self.heap[smallest], self.heap[index]
            self._heapify_down(smallest)

    def is_empty(self):
        return len(self.heap) == 0

class Node:
    def __init__(self, value):
        self.value = value
        self.next = None
        self.prev = None

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None

    def enqueue(self, value):
        new_node = Node(value)
        if not self.tail:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node

    def dequeue(self):
        if not self.head:
            return None
        value = self.head.value
        self.head = self.head.next
        if self.head:
            self.head.prev = None
        else:
            self.tail = None
        return value

    def is_empty(self):
        return self.head is None





