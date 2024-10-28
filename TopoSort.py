#  File: TopoSort.py

#  Description: Cycle and topological sort was done in this program.

#  Student Name: Vaishnavi Sathiyamoorthy

#  Student UT EID: vs25229

#  Course Name: CS 313E

#  Unique Number: 52530

#  Date Created: 11/26/2022

#  Date Last Modified: 11/27/2022

import sys


class Stack(object):
    def __init__(self):
        self.stack = []

    # add an item to the top of the stack
    def push(self, item):
        self.stack.append(item)

    # remove an item from the top of the stack
    def pop(self):
        return self.stack.pop()

    # check the item on the top of the stack
    def peek(self):
        return self.stack[-1]

    # check if the stack if empty
    def is_empty(self):
        return (len(self.stack) == 0)

    # return the number of elements in the stack
    def size(self):
        return (len(self.stack))

    def stack_list(self):
        lst = []
        while self.is_empty() == False:
            lst.append(self.pop())

        for i in reversed(range(len(lst))):
            self.push(lst[i])
        return lst

class Queue(object):
    def __init__(self):
        self.queue = []

    # add an item to the end of the queue
    def enqueue(self, item):
        self.queue.append(item)

    # remove an item from the beginning of the queue
    def dequeue(self):
        return (self.queue.pop(0))

    # check if the queue is empty
    def is_empty(self):
        return (len(self.queue) == 0)

    # return the size of the queue
    def size(self):
        return (len(self.queue))

    def peek_first(self):
        return self.queue[0]

class Vertex(object):
    def __init__(self, label):
        self.label = label
        self.visited = False
        self.in_degree = 0

    # determine if a vertex was visited
    def was_visited(self):
        return self.visited

    # determine the label of the vertex
    def get_label(self):
        return self.label

    # string representation of the vertex
    def __str__(self):
        return str(self.label)


class Graph(object):
    def __init__(self):
        self.Vertices = []
        self.adjMat = []

    # check if a vertex is already in the graph
    def has_vertex(self, label):
        nVert = len(self.Vertices)
        for i in range(nVert):
            if (label == (self.Vertices[i]).get_label()):
                return True
        return False

    # given the label get the index of a vertex
    def get_index(self, label):
        nVert = len(self.Vertices)
        for i in range(nVert):
            if (label == (self.Vertices[i]).get_label()):
                return i
        return -1

    # add a Vertex with a given label to the graph
    def add_vertex(self, label):
        if (self.has_vertex(label)):
            return

        # add vertex to the list of vertices
        self.Vertices.append(Vertex(label))

        # add a new column in the adjacency matrix
        nVert = len(self.Vertices)
        for i in range(nVert - 1):
            (self.adjMat[i]).append(0)

        # add a new row for the new vertex
        new_row = []
        for i in range(nVert):
            new_row.append(0)
        self.adjMat.append(new_row)

    # add weighted directed edge to graph
    def add_directed_edge(self, start, finish, weight=1):
        self.adjMat[start][finish] = weight
        self.Vertices[finish].in_degree += 1

    # add weighted undirected edge to graph
    def add_undirected_edge(self, start, finish, weight=1):
        self.adjMat[start][finish] = weight
        self.adjMat[finish][start] = weight

    # return an unvisited vertex adjacent to vertex v (index)
    def get_adj_unvisited_vertex(self, v):
        nVert = len(self.Vertices)
        for i in range(nVert):
            if (self.adjMat[v][i] == 1) and self.Vertices[i].visited == False:
                return i
        return -1

    # do a depth first search in a graph
    def dfs(self, v):
        # create the Stack
        theStack = Stack()

        # mark the vertex v as visited and push it on the Stack
        (self.Vertices[v]).visited = True
        print(self.Vertices[v])
        theStack.push(v)

        # visit all the other vertices according to depth
        while (not theStack.is_empty()):
            # get an adjacent unvisited vertex
            u = self.get_adj_unvisited_vertex(theStack.peek())
            if (u == -1):
                u = theStack.pop()
            else:
                (self.Vertices[u]).visited = True
                print(self.Vertices[u])
                theStack.push(u)

        # the stack is empty, let us rest the flags
        nVert = len(self.Vertices)
        for i in range(nVert):
            (self.Vertices[i]).visited = False

    # do the breadth first search in a graph
    def bfs(self, v):
        theQueue = Queue()
        self.Vertices[v].visited = True
        print(self.Vertices[v])
        theQueue.enqueue(v)

        while theQueue.is_empty() == False:
            u = self.get_adj_unvisited_vertex(theQueue.peek_first())
            if u == -1:
                theQueue.dequeue()
            if u != -1:
                (self.Vertices[u]).visited = True
                print(self.Vertices[u])
                theQueue.enqueue(u)

        nVert = len(self.Vertices)
        for i in range(nVert):
            (self.Vertices[i]).visited = False

    # determine if a directed graph has a cycle
    # this function should return a boolean and not print the result
    def has_cycle(self):
        # starts with each vertex of the graph
        for i in range(len(self.Vertices)):
            st = Stack()
            st.push(self.Vertices[i])
            (self.Vertices[i]).visited = True

            # checks whether a cycle is present by adding and removing from stack
            while st.is_empty() == False:
                idx = self.get_index(st.peek().get_label())
                found = False
                for j in range(len(self.Vertices)):
                    if self.adjMat[idx][j] == 1 and self.Vertices[j].visited == True:
                        lst = st.stack_list()
                        if self.Vertices[j] in lst:
                            for j in range(len(self.Vertices)):
                                self.Vertices[j].visited = False
                            return True
                    elif self.adjMat[idx][j] == 1 and self.Vertices[j].visited == False:
                        self.Vertices[j].visited = True
                        st.push(self.Vertices[j])
                        found = True
                        break
                if found == False:
                    st.pop()

            for j in range(len(self.Vertices)):
                self.Vertices[j].visited = False

        return False

    # delete an edge from the adjacency matrix
    # delete a single edge since the graph is directed
    # updates in_degree
    def delete_edge(self, fromVertexLabel, toVertexLabel):
        self.adjMat[self.get_index(fromVertexLabel)][self.get_index(toVertexLabel)] = 0
        self.Vertices[self.get_index(toVertexLabel)].in_degree -= 1

    # delete a vertex from the vertex list and all edges from and
    # to it in the adjacency matrix
    def delete_vertex(self, vertexLabel):
        del self.adjMat[self.get_index(vertexLabel)]
        for i in range(len(self.adjMat)):
            del self.adjMat[i][self.get_index(vertexLabel)]
        del self.Vertices[self.get_index(vertexLabel)]

    def toposort(self):
        qu = Queue()
        # empty list is created for each round of the loop
        while len(self.Vertices) > 0:
            lst = []
            # checks which vertices have an in_degree of 0
            for i in self.Vertices:
                if i.in_degree == 0:
                    lst.append(i)
            # Queues the vertices that have an in_degree of 0
            for i in lst:
                qu.enqueue(i)
            # The edges and vertices with in_degree 0 are removed. The in_degree is updates for the other vertices
            for i in lst:
                idx = self.get_index(i.get_label())
                for j in range(len(self.adjMat[idx])):
                    if self.adjMat[idx][j] == 1:
                        self.delete_edge(i.get_label(), self.Vertices[j].label)
                self.delete_vertex(i.get_label())
        # the final list is returned
        final_lst = []
        while qu.is_empty() == False:
            final_lst.append(qu.dequeue().get_label())
        return final_lst





def main():
    # create the Graph object
    theGraph = Graph()

    # read the number of vertices
    line = sys.stdin.readline()
    line = line.strip()
    num_vertices = int(line)

    # read the vertices to the list of Vertices
    for i in range(num_vertices):
        line = sys.stdin.readline()
        letter = line.strip()
        theGraph.add_vertex(letter)

    # read the number of edges
    line = sys.stdin.readline()
    line = line.strip()
    num_edges = int(line)

    # read each edge and place it in the adjacency matrix
    for i in range(num_edges):
        line = sys.stdin.readline()
        edge = line.strip()
        edge = edge.split()
        start = theGraph.get_index(edge[0])
        finish = theGraph.get_index(edge[1])

        theGraph.add_directed_edge(start, finish)

    # test if a directed graph has a cycle
    if (theGraph.has_cycle()):
        print("The Graph has a cycle.")
    else:
        print("The Graph does not have a cycle.")

    # test topological sort
    if (not theGraph.has_cycle()):
        vertex_list = theGraph.toposort()
        print("\nList of vertices after toposort")
        print(vertex_list)


if __name__ == "__main__":
    main()
