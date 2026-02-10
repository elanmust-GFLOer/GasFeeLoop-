from core.state import load_state

def observe():
    state = load_state()
    loops = state.get("loops", 0)
    total_cost = state.get("total_cost", 0)
    avg_cost = total_cost / loops if loops > 0 else 0

    print("🌬️ GFLO OBSERVER")
    print(f"Loops: {loops}")
    print(f"Total cost: {total_cost}")
    print(f"Average cost per loop: {avg_cost:.2f}")

    if avg_cost > 5:
        print("⚠️ Status: HIGH GAS USAGE")
    else:
        print("✅ Status: STABLE")
