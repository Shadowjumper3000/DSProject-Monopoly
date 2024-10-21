"""
utils.py

This module contains utility classes and functions.

Classes
-------
Node
    A class used to represent a Node in a singly linked list.
LinkedList
    A simple implementation of a singly linked list.
"""


class Node:  # pylint: disable=too-few-public-methods
    """
    A class used to represent a Node in a singly linked list.

    Attributes
    ----------
    data : any
        The data stored in the node.
    next : Node or None
        The reference to the next node in the linked list.
    """

    def __init__(self, data=None):
        """
        Parameters
        ----------
        data : any, optional
            The data to be stored in the node (default is None).
        """
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
        """Initializes an empty linked list."""
        self.head = None

    def append(self, data):
        """
        Adds a new node with the specified data to the end of the list.

        Parameters
        ----------
        data : any
            The data to be stored in the new node.
        """
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self):
        """Prints the elements of the linked list in a list format."""
        current = self.head
        while current:
            print(current.data, end=" -> " if current.next else "\n")
            current = current.next
