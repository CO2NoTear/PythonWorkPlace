# %%
import numpy as np

# %%
class BaseTable:
    constants = {
        "diamond" : 1,
        "fire" : -1,
        "wall" : np.nan
    }
    # up, right, down, left
    # 0,  1,     2,    3
    directions = [
        (-1,0),
        (0,1),
        (1,0),
        (0,-1)
    ]
    action_dire_ratio = [
        0.1,
        0.8,
        0.1
    ]
    
    def __init__(self, shape, gamma, alive) -> None:
        self.table = np.zeros(shape)
        self.qtable = np.zeros([shape[0], shape[1], 4])
        self.vtable = np.zeros(shape)
        self.gamma = gamma
        self.alive = alive

    def set_table_val(self, dot:tuple, val:str):
        self.table[dot] = self.constants[val]

    def set_start_dot(self, dot):
        self.start_dot = dot
    
    def in_boundary(self, dot):
        try:
            self.table[dot]
            return True
        except IndexError:
            return False
    
    def iterate(self, step):
        for _ in range(step):
            self.__single_itreate()
            
    def __single_itreate(self):
        total_nodes = self.table.shape[0]*self.table.shape[1]
        new_qtable = np.zeros(self.qtable.shape)
        for j in range(total_nodes):
            dot = (j//self.table.shape[1], j%self.table.shape[1])
            # if is wall, continue
            if not self.in_boundary(dot) or np.isnan(self.table[dot]):
                continue
            new_qtable[dot] = self.__calc_q_nodewise(dot)
        del self.qtable
        self.qtable = new_qtable
        for j in range(total_nodes):
            dot = (j//self.table.shape[1], j%self.table.shape[1])
            self.vtable[dot] = np.max(new_qtable[dot])
    
    def __calc_q_nodewise(self, dot:tuple):
        new_qvalue = []
        for qdire in range(4):
            sum = 0
            for action_dire in range(3):
                next_dot = tuple(np.array(dot) + self.directions[(qdire+action_dire-1)%4])
                # hit a wall
                if not self.in_boundary(next_dot) or np.isnan(self.table[next_dot]):
                    next_dot = dot
                sum += self.action_dire_ratio[action_dire] * (
                    self.vtable[next_dot] * self.gamma +\
                    self.alive + self.table[dot]
                )
            new_qvalue.append(sum)
        return np.array(new_qvalue)
    
    def print_table(self):
        print("table:")
        print(self.table.shape)
        print(self.table)
        print("qtable:")
        print(self.qtable.shape)
        print(self.qtable)
        print("vtable:")
        print(self.vtable.shape)
        print(self.vtable)


# %%
MDP = BaseTable((3,4), 0.5, 0)
MDP.set_table_val((0,3), 'diamond')
MDP.set_table_val((1,3), 'fire')
MDP.set_table_val((1,1), 'wall')
MDP.set_start_dot((2,0))

MDP.iterate(2)
MDP.print_table()


