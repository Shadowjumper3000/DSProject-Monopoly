class Node:
    def __init__(self, data=None):
        self.data = data
        self.next = None

class LinkedList:
    """
    A simple implementation of a singly linked list.
    Methods
    -------
    __init__():
        Initializes an empty linked list.
    append(data):
        Adds a new node with the specified data to the end of the list.
    display():
        Prints the elements of the linked list in a list format.
    """
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self):
        current = self.head
        while current:
            print(current.data, end=" -> " if current.next else "\n")
            current = current.next
