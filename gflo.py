from typer import Typer
from scripts.emit_flow import Node, Flow
from core.loop import process_flow
from core.reward import reward_loop

app = Typer()

@app.command()
def emit(cost: int = 1, ethical: bool = True):
    flow = Flow()
    flow.cost = cost
    trace, state = process_flow(flow)
    regen_gain, state = reward_loop(cost, ethical)
    print("🌬️ FLOW EMITTED")
    print("TRACE:", trace.hash)
    print("STATE:", state)
    print("REGEN GAIN:", regen_gain)

if __name__ == "__main__":
    app()  # <--- EZ KÖTELEZŐ!


