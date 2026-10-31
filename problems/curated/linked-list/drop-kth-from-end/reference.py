def remove_kth_from_end(head, k):
    dummy = ListNode(0, head)
    lead = dummy
    for _ in range(k):
        lead = lead.next
    trail = dummy
    while lead.next:
        lead = lead.next
        trail = trail.next
    trail.next = trail.next.next
    return dummy.next
