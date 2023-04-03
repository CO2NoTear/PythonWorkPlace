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
        if 0 <= dot[0] < self.table.shape[0] and 0 <= dot[1] < self.table.shape[1]:
            return True
        else:
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
        with np.printoptions(precision=2, suppress=True):
            # print("table:")
            # print(self.table.shape)
            # print(self.table)
            print("qtable:")
            fulltable = np.full((self.table.shape[0]*3, self.table.shape[1]*3), np.nan)
            for i in range(self.table.shape[0]*self.table.shape[1]):
                dot_center = (i//self.table.shape[1], i%self.table.shape[1])
                dot_center_np = np.array((dot_center[0]*3+1, dot_center[1]*3+1))
                fulltable[tuple(dot_center_np)] = 0
                for dire in range(4):
                    fulltable[tuple(dot_center_np + self.directions[dire])] = self.qtable[dot_center][dire]
            print(fulltable)
            print("vtable:")
            print(self.vtable.shape)
            print(self.vtable)

# %%
gamma = 1
alive = 0
MDP = BaseTable((3,4), gamma, alive)
MDP.set_table_val((0,3), 'diamond')
MDP.set_table_val((1,3), 'fire')
MDP.set_table_val((1,1), 'wall')
MDP.set_start_dot((2,0))

MDP.iterate(1)
print('the {}th iteration'.format(1))
MDP.print_table()
MDP.iterate(1)
print('the {}th iteration'.format(2))
MDP.print_table()
MDP.iterate(1)
print('the {}th iteration'.format(3))
MDP.print_table()
MDP.iterate(1)
print('the {}th iteration'.format(4))
MDP.print_table()
MDP.iterate(1)
print('the {}th iteration'.format(5))
MDP.print_table()


