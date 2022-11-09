from mesa import Agent

class MoneyAgent(Agent):

    def __init__(self, unique_id, model, type):
        super().__init__(unique_id, model)
        self.wealth = type
        self.movimientos = 0
        self.limpiados = 0
    def move(self):
        possible_steps = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_steps)
        self.model.grid.move_agent(self, new_position)

    
    
    def clean(self):
        cellmates = self.model.grid.get_cell_list_contents([self.pos])
        other_agent = self.random.choice(cellmates)
        if other_agent.wealth == 1:
            other_agent.wealth = 0
            self.limpiados += 1


    def step(self):
        if self.wealth == 3:
                self.clean()
                self.move()
                self.movimientos = self.movimientos  + 1
        """ if self.wealth == 1:
            self.give_money() """

