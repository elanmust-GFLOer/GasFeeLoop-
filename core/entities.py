class Node:
    def __init__(self, id):
        self.id = id

class Flow:
    def __init__(self, node_id, cost=1):
        self.node_id = node_id
        self.cost = cost
        self.hash = hash((node_id, cost))

class Trace:
    def __init__(self, flow):
        # Egyszerű hash, de lehet bővíteni
        self.hash = hash((flow.node_id, flow.cost))
