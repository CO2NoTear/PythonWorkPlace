# %%
import numpy as np
from queue import PriorityQueue
from copy import deepcopy
import os

# %% [markdown]
# ### 1. 数据结构选择
# #### 数据结构要求
# - 3x3迷宫
# - 状态：3x3=9维，1,...,9
# - 9表示空腔
# - cost: 每走一步cost 1
# - 走下一步：9的上下左右某一格与它做交换
# - 上下左右：
#   - Up: -3
#   - Down: +3
#   - left: -1
#   - right +1
# #### 初始状态
# - 由目标解随机移动N步得到
# #### Heuristic 设计
# - version 1.  
#   各数码当前位置与正确位置曼哈顿距离 加和
#   - 一定小于等于实际步数
#   - 比较粗糙

# %%
# Up, Right, Down, Left
directions = [
    -3 , 1, +3, -1
]
SOLUTION_PATTERN = np.array(
    [1,2,3,
     8,9,4,
     7,6,5]
)
solution_index = {
    SOLUTION_PATTERN[i]:i for i in range(9)
}

def leagel_movement(src, op):
    # Up or Down
    if src + op < 0 or src + op > 8:
        return False
    # Left or Right
    if op%3:
        if src%3 + op < 0 or src%3 +op > 2:
            return False
    return True

def check_result(state):
    return np.all(state == SOLUTION_PATTERN)

# 计算给定状态的heuristic值：Version1:曼哈顿距离
def calc_heuristic(state):
    sum = 0
    # state can be 
    # 3, 2, 4
    # 1, 5,(7) <- i = 5, state[i] = 7
    #[6],x, 8                |---means----> wanna go to i+1 = 7
    #          got source = i = 5
    #              dest = state[i]-1 = 6
    #              L1dist = abs(source//3 - dest//3) +
    #                       abs(souce%3 - dest%3)
    for i in range(9):
        # 从第i个位置到第state[i]
        source = i
        dest = solution_index[state[i]]
        sum += abs(source//3 - dest//3) +\
               abs(source %3 - dest %3)
    return sum
# 生成初始迷宫
def generate_initial_puzzle(random_steps):
    init_node = node(SOLUTION_PATTERN, 4, 0, 0)
    for _ in range(random_steps):
        op = directions[np.random.randint(4)]
        while not leagel_movement(init_node.hole, op):
            op = directions[np.random.randint(4)]
        init_node.state[init_node.hole], init_node.state[init_node.hole+op] =\
        init_node.state[init_node.hole+op], init_node.state[init_node.hole]
        init_node.hole += op
    return init_node

class node:
    def __init__(self, state, hole, cost, heuristic, route:list=[]) -> None:
        self.state:np.ndarray = deepcopy(state)
        self.cost = cost
        self.heuristic = heuristic
        # # route can be useless,
        # for we can print whole state at every entry
        self.route = route
        
        # hole is where the num "9" is
        # a fast way to locate the "9" and move it
        self.hole = hole
    
    def __lt__(self, other):
        return self.cost+self.heuristic < other.cost+other.heuristic

    def get_state_str(self):
        return str(self.state.reshape(3,3)).replace('9',' ')

# %%
SHUFFLE_STEP = 100
initial_puzzle = generate_initial_puzzle(SHUFFLE_STEP)
# initial_puzzle = node(np.array([9,4,8,5,1,3,7,6,2]), 0, 0, 0)
initial_puzzle.heuristic = calc_heuristic(initial_puzzle.state)
print(initial_puzzle.state,'\n', initial_puzzle.hole)

# %%
queue = PriorityQueue()
MAXCOST = np.inf
Astar_File = open(os.path.dirname(__file__)+"/output.txt","w")
DEPTH_LIMIT = round(SHUFFLE_STEP*0.75)

def Astar(initial_puzzle):
    min_cost = MAXCOST
    queue.put(initial_puzzle)
    while not queue.empty():
        # 取出队头
        try:
            current_node:node = queue.get()
            # Astar_File.write("{: <30} Current cost: {}\n".format(current_node.get_state_str(), current_node.cost))
        except IndexError:
            print("[ERROR] 队空了！")
            return -1
        
        if current_node.cost > DEPTH_LIMIT: #or (current_node.cost!=0 and str(current_node.state.reshape(3,3)) in current_node.route):
            continue

        # 正解输出
        if check_result(current_node.state):
            min_cost = min(min_cost,current_node.cost)

            Astar_File.write("Initial puzzle\n")
            Astar_File.write(initial_puzzle.get_state_str())
            Astar_File.write('\n')
            Astar_File.write("Min cost is: {}\n".format(current_node.cost))
            for i in range(len(current_node.route)):
                Astar_File.write(f"step {i+1}:\n")
                Astar_File.write(current_node.route[i])
                Astar_File.write('\n')
            Astar_File.close()
            return min_cost

        # Astar迭代
        for dire in directions:
            if not leagel_movement(current_node.hole, dire):
                continue
            next_node = deepcopy(current_node)
            next_node.state[next_node.hole], next_node.state[next_node.hole+dire] =\
            next_node.state[next_node.hole+dire], next_node.state[next_node.hole] 
            next_node.route.append(next_node.get_state_str())
            next_node.hole += dire
            next_node.cost += 1
            next_node.heuristic = calc_heuristic(next_node.state)
            queue.put(next_node)
        del current_node
    return min_cost

# %%
print(Astar(initial_puzzle))


