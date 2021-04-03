from os import PathLike, path

from bonding_curve_simulator.mesa.simulation_model import SimulationModel


def with_outdir(outdir: PathLike):
    def _with_outdir(model: SimulationModel):
        model.datacollector.get_model_vars_dataframe().to_csv(
            path.join(outdir, "/model.csv")
        )
        model.datacollector.get_agent_vars_dataframe().to_csv(
            path.join(outdir, "/agent.csv")
        )

        return model

    return _with_outdir
