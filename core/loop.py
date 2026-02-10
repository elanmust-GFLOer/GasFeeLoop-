from core.entities import Node, Flow, Trace

def process_flow(flow):
    trace = Trace(flow)
    state = {"loops": 1, "total_cost": flow.cost}  # egyszerű példa
    return trace, state
