from core.loop import process_flow
from scripts.emit_flow import flow
from core.reward import reward_loop

# Teszt futtatás
flow.cost = 3
trace, state = process_flow(flow)
regen_gain, state = reward_loop(cost=flow.cost, ethical=True)

print("🌬️ FLOW EMITTED")
print("TRACE:", getattr(trace, 'hash', 'No hash'))
print("STATE:", state)
print("REGEN GAIN:", regen_gain)
