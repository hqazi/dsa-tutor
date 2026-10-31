def reverse_list(head):
    prev = None
    node = head
    while node:
        nxt = node.next
        node.next = prev
        prev = node
        node = nxt
    return prev
