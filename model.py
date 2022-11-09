from mesa import Model
from mesa import DataCollector
from agent import MoneyAgent
from mesa.time import RandomActivationByType, RandomActivation
from mesa.space import MultiGrid


class MoneyModel(Model):

    verbose = False

    def __init__(self, number_of_agents, width,height,limpiadores,stepsMax):
        self.num_agents = number_of_agents
        self.agentes = limpiadores
        self.maxStep = stepsMax
        self.grid = MultiGrid(width, height, True)
        self.running = True

        #self.schedule = RandomActivationByType(self)
        self.schedule = RandomActivation(self)
        """self.datacollector = DataCollector(
            {
                "Wolves": lambda m: m.schedule.get_type_count(MoneyAgent.wealth == 1),
                "Sheep": lambda m: m.schedule.get_type_count(MoneyAgent.wealth == 3,lambda x: x.fully_grown),
                
            }
        )"""
            # Create agents
        for i in range(self.num_agents):
            a = MoneyAgent(i, self, 1)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            if self.grid.is_cell_empty((x,y)):
                self.grid.place_agent(a, (x, y))
            else:
                
                
                self.grid.place_agent(a, self.grid.find_empty())
                
        for i in range(self.agentes):
            a = MoneyAgent(i+self.num_agents, self,3)
            self.schedule.add(a)
            # Add the agent to a random grid cell
            x = 1
            y = 1
            self.grid.place_agent(a, (x, y))
        
        self.datacollector = DataCollector(
            {
                "Movimientosrealizados": MoneyModel.movimientos,
                "limpieza":MoneyModel.limpios,
            }
        )
        

    def step(self):
        if self.schedule.steps < self.maxStep-2:
            
            self.schedule.step()
            
            self.datacollector.collect(self)
            
        else:
            self.running = False

    @staticmethod
    def movimientos(model):
        acumulado = 0

        for i in model.schedule.agents:
            if i.wealth == 3:
                acumulado += i.movimientos

        return acumulado

    @staticmethod
    def limpios(model):

        
        # sucios = model.num_agents

        # sucios -= model.limpiados

        limpiados = 0
        for i in model.schedule.agents:
            if i.wealth == 3:
                limpiados += i.limpiados
                
        return limpiados

