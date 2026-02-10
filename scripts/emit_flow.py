from core.entities import Node, Flow

# Példányosítás (globális változók a CLI-hez)
node = Node("local-node")
flow = Flow(node.id, cost=1)

