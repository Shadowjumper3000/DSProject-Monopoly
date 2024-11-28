"""
Utils module containing utility functions and classes.
"""


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # Adds a new node with the given data to the end of the linked list
    def append(self, data):
        """
        Adds a new node with the given data to the end of the linked list.

        Time Complexity:
            O(n): where n is the number of nodes in the linked list
        """
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    # Returns a list of all data elements in the linked list
    def display(self):
        """
        Returns a list of all data elements in the linked list.

        Time Complexity:
            O(n): where n is the number of nodes in the linked list
        """
        elems = []
        current = self.head
        while current:
            elems.append(current.data)
            current = current.next
        return elems

    # Removes the first node with the specified data (key) from the list
    def remove(self, key):
        """
        Removes the first node with the specified data (key) from the list.

        Time Complexity:
            O(n): where n is the number of nodes in the linked list
        """
        current = self.head
        if current and current.data == key:
            self.head = current.next
            current = None
            return
        prev = None
        while current and current.data != key:
            prev = current
            current = current.next
        if current is None:
            return
        prev.next = current.next
        current = None


class Queue:
    def __init__(self):
        self.items = LinkedList()

    def is_empty(self):
        return self.items.head is None

    def enqueue(self, item):
        """
        Adds an item to the end of the queue.

        Time Complexity:
            O(1)
        """
        self.items.append(item)

    def dequeue(self):
        """
        Removes and returns the item at the front of the queue.
        Raises an IndexError if the queue is empty.

        Time Complexity:
            O(1)
        """
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        dequeued_item = self.items.head.data
        self.items.remove(dequeued_item)
        return dequeued_item

    # Returns the item at the front of the queue without removing it
    def peek(self):
        """
        Returns the item at the front of the queue without removing it.
        Raises an IndexError if the queue is empty.

        Time Complexity:
            O(1)
        """
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.items.head.data

    # Displays the current elements of the queue
    def display(self):
        return self.items.display()


def wrap_text(text, font, max_width):
    """
    Wrap text to fit within a certain width

    Args:
        text (str): Text to wrap
        font (int): Font to use
        max_width (int): Maximum width of the text

    Returns:
        str: Wrapped text

    Time Complexity:
        O(n): where n is the number of words in the text
    """
    words = text.split(" ")
    lines = []
    current_line = []

    for word in words:
        current_line.append(word)
        width, _ = font.size(" ".join(current_line))
        if width > max_width:
            current_line.pop()
            lines.append(" ".join(current_line))
            current_line = [word]

    lines.append(" ".join(current_line))
    return lines


def quick_sorts(arr, key=lambda x: x, reverse=False):
    """
    Sorts an array using the quick sort algorithm.

    Args:
        arr (list): The array to be sorted.
        key (function): A function that serves as a key for the sort comparison.
        reverse (bool): If True, the list elements are sorted as if each comparison were reversed.

    Returns:
        list: The sorted array.
    Time Complexity:
        Average case: O(n log n)
        Worst case: O(n^2)
    """
    if len(arr) <= 1:
        return arr
    pivot = key(arr[len(arr) // 2])
    left = [x for x in arr if key(x) < pivot]
    middle = [x for x in arr if key(x) == pivot]
    right = [x for x in arr if key(x) > pivot]
    if reverse:
        return (
            quick_sorts(right, key, reverse) + middle + quick_sorts(left, key, reverse)
        )
    else:
        return (
            quick_sorts(left, key, reverse) + middle + quick_sorts(right, key, reverse)
        )
