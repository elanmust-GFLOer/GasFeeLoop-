from core.state import load_state, save_state

def reward_loop(cost, ethical=True):
    state = load_state()
    
    loops = state.get("loops", 0)
    regen = state.get("regen", 0)
    
    # alap REGEN: minden loop 1 pont
    regen_gain = 1
    
    # ha cost túl magas → csökkentjük
    if cost > 5:
        regen_gain = 0.5
    
    # etikai boost
    if ethical:
        regen_gain *= 2
    
    state["loops"] = loops
    state["regen"] = regen + regen_gain
    
    save_state(state)
    return regen_gain, state
