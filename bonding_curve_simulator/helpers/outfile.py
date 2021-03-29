from bonding_curve_simulator.mesa.simulation_model import SimulationModel


def with_outfile(model: SimulationModel) -> SimulationModel:

    model.datacollector.get_model_vars_dataframe().to_csv("datacollector/model.csv")
    model.datacollector.get_agent_vars_dataframe().to_csv("datacollector/agent.csv")

    return model
