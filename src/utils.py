class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def display(self):
        elems = []
        current = self.head
        while current:
            elems.append(current.data)
            current = current.next
        return elems

    def remove(self, key):
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
        self.items.append(item)

    def dequeue(self):
        if self.is_empty():
            raise IndexError("Dequeue from empty queue")
        dequeued_item = self.items.head.data
        self.items.remove(dequeued_item)
        return dequeued_item

    def peek(self):
        if self.is_empty():
            raise IndexError("Peek from empty queue")
        return self.items.head.data

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
