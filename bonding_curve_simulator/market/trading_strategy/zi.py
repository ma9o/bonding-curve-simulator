# Zero intelligence

# https://github.com/abides-sim/abides/blob/master/agent/ZeroIntelligenceAgent.py

from bonding_curve_simulator.mesa.agent.trader import TraderAgent


def strategy(agent: TraderAgent) -> None:

    r = agent.random.randint(0, 100)

    if r >= 25 and r <= 75:
        pass
    elif r < 25:
        sale_amount = agent.model.random.uniform(0.0, agent.supply)
        agent.model.exchange.sell(agent, sale_amount)
    elif r > 75:
        reserve_amount = agent.model.random.uniform(0.0, agent.reserve)
        agent.model.exchange.buy(agent, reserve_amount)
