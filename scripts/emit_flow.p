from core.entities import Node, Flow

# Node + Flow objektumok globális szinten
node = Node("local-node")
flow = Flow(node.id, cost=1)
