from mesa.visualization.modules import  CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from mesa.visualization.UserParam import UserSettableParameter

from model import MoneyModel
from mesa.visualization.modules import CanvasGrid
from mesa.visualization.modules import ChartModule
import mesa
import pandas as pd
import matplotlib.pyplot as plt

params = {"number_of_agents": 250, "width": 25, "height": 25, "limpiadores": 25, "stepsMax": 500}

results = mesa.batch_run(
    MoneyModel,
    parameters=params,
    iterations=100,
    max_steps=params["stepsMax"],
    number_processes=1,
    data_collection_period=1,
    display_progress=True,
)

results_df = pd.DataFrame(results)
print(results_df.keys())


N_values = results_df.Movimientosrealizados.values
gini_values = results_df.limpieza.values
plt.scatter(N_values, gini_values)
plt.show()

NUMBER_OF_CELLS = 10

simulation_params  = {
    "number_of_agents":UserSettableParameter(
        "slider",
        "Sucio",
        50,
        10,
        99,
        1,
        description = "hola"
    ),
    "width": NUMBER_OF_CELLS,
    "height": NUMBER_OF_CELLS,
    "limpiadores":UserSettableParameter(
        "slider",
        "Limpiadores",
        5,
        1,
        10,
        1,
        description = "hola"
    ),
    "stepsMax":UserSettableParameter(
        "slider",
        "Steps Maximos",
        50,
        10,
        100,
        1,
        description = "hola"
    ),
}


def agent_portrayal(agent):
    portrayal = {"Shape":"circle", "Filled": "True", "r":0.5}

    if agent.wealth == 1:
        portrayal["Color"] = "green"
        portrayal["Layer"] = 0
    elif agent.wealth == 3:
        portrayal["Color"] = "blue"
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = "red"
        portrayal["Layer"] = 0
        

    return portrayal

grid = CanvasGrid(agent_portrayal,NUMBER_OF_CELLS,NUMBER_OF_CELLS,500,500)

movimientos = ChartModule(
    [
        {"Label": "Movimientosrealizados", "Color": "red"},
    ]
)
limpieza = ChartModule(
    [
        {"Label": "limpieza", "Color": "red"},
    ]
)

servidor = ModularServer(MoneyModel,[grid,movimientos,limpieza],"Limpiadora",simulation_params)
servidor.port = 8521
servidor.launch() 
