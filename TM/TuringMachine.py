from re import I
from shutil import move
import numpy as np
tapeLength = 1000
maxIter = 9999

class TuringMachine:
    '''
    初始化图灵机，读入程序和输入
    '''
    def __init__(self, programFile):
        # tap 是一个长度为tapeLength的数组
        self.tape = list(np.zeros(tapeLength))
        self.state = 1
        # head初始化在tape中间的位置
        self.head = tapeLength // 2
        self.program_name = []
        self.leftmost = self.rightmost = self.head
        self.halt = True
        # 如果在小于maxIter停止，halt = True；如果在maxIter未停止或有其他方法判定为非停时，halt = False
        self.program = self.buildProgram(programFile)
    def buildProgram(self, programFile):
        '''
        :param programFile: 一个N行程序，具体格式参照Great Ideas in Computer Science P164 M_add
        :return: 自行设计合适的数据结构，存储每一条instruction，方便调用；example：Nx2数组，每个数组包含(i,R,j)或者(i,L,j)
        '''
        index = 0
        self.program_name = programFile
        f = open(self.program_name, 'r')
        instrcutions = [[]]
        while True:
            instrcutions.append([])
            rawinput = f.readline()
            if not rawinput:
                break
            instrcutions[index] = rawinput.split(',')[1:3]
            # print(instrcutions[index])
            index += 1
        return instrcutions

    def step(self):
        '''
        执行一条指令，更新head, tape, state
        '''
        tempval = int(self.tape[self.head])        # 暂存探头值
        inst = self.program[self.state-1][tempval]   # 暂存指令
        if inst[1] == 'L':                         # 格式化移动指令
            movement = -1
        else: movement = 1

        self.tape[self.head] = int(inst[0])        # Modify tape val.
        self.head += movement                      # Update Head
        self.leftmost  = min(self.head,self.leftmost)  # Update leftmost
        self.rightmost = max(self.head,self.rightmost) # Update rightmost
        self.state= int(inst[2])                   # Update state
        print(self.getCurrentStateString())

    def run(self, input):
        '''
        执行整个程序，得到运算结果
        '''
        # 输入input
        ini_index = 0
        while ini_index < len(input):
            self.tape[ini_index+self.head] = int(input[ini_index])
            ini_index += 1
        self.rightmost += ini_index -1     # 更新最右端
        steps = 0
        print('\n\nStart running program {0}\n now :'.format(self.program_name),self.getCurrentStateString())
        while self.state != 0:
            self.step()
            steps += 1
            if steps >100:
                self.halt = False
                break
        # print(self.tape[self.head:self.head+10])
        print('--------------End Running {0}--------------\n\n'.format(self.program_name))
    def getTuringResult(self):
        '''
        :return: 从非零元素开始的tape序列，
        例如整体序列为......000111110000.....，则返回'11111'
        '''
        cnt = self.tape.count(1)
        ans = []
        for item in range(0,cnt):
            ans.append('1')
        return ans

    def getCurrentStateString(self):
        '''
        设计字符串格式输出当前状态、位置、tape状态
        '''
        return "state:{0},head:{1},tape:\n{2}".format(self.state,self.head,self.tape[self.leftmost:self.rightmost+1])
    def visualize(self):
        '''
        （选做）使用matplotlib动态展示图灵机的更新过程
        '''