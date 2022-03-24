from dis import Instruction
from errno import EBADE
from filecmp import dircmp
from sqlite3 import ProgrammingError
from TuringMachine import *

def src_generetor():
    '''
    用于生成单行操作的两个数字
    '''
    # 生成0~11 一共12个数字
    for num1 in range(12):
        for num2 in range(12):
            return [num1,num2]
    

def decoder(src):
    '''
    解码所给数字代表的操作
    '''
    return '{0}{1}{2}'.format()

def program_generator(nState):
    instructions = [[]]
    for state in range(nState):
        src = src_generetor()
        instructions.append(state+1)
        instructions[state].append(decoder(src[0]))


def machine_generator(nState):
    '''
    :param nState: 图灵机的状态数
    :return TuringMachine: 一款图灵机
    对于nState的图灵机，其操作表上一共2n个0Ln类型的操作，用数字进制表示它们即可。
    原理：单操作最多有(k+1)*2*2种可能 例如：2状态的图灵机，一个空最多有3*2*2 = 12种操作，
    利用进制解码出源操作，则只需要写一个生成4个数字的4层循环，而不是12层循环。
    '''
    new_machine = TuringMachine(program_generator(nState))
    return 



def busyBeaver(nState):
    '''
    :param nState: 图灵机的状态数
    :return: Busy Beaver的数值
    提示：一般性计算busyBeaver是个非常复杂的问题，对于简单的情形，如BB(1), BB(2)我们可以使用穷举法得到结果
    其中，BB(1)需要考虑64种情况，而BB(2)需要考虑20736种情况
    '''
    busyMachine = machine_generator(nState)
    return 0

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    tm_add = TuringMachine('add.tr')
    tm_add.run('111011111')
    result = len(tm_add.getTuringResult())
    print('TM: 3+5={0}'.format(result))

    tm_multiply_two = TuringMachine('multiply_two.tr')
    tm_multiply_two.run('11111')
    result = len(tm_multiply_two.getTuringResult())
    print('TM: 5x2={0}'.format(result))

    tm_plus_three = TuringMachine('plus_three.tr')
    tm_plus_three.run('11111')
    result = len(tm_plus_three.getTuringResult())
    print('TM: 5+3={0}'.format(result))

    tm_multiply_two_plus_three= TuringMachine('multiply_two_plus_three.tr')
    tm_multiply_two_plus_three.run('11111')
    result = len(tm_multiply_two_plus_three.getTuringResult())
    print('TM: 2x5+3={0}'.format(result))

    bb1Number = busyBeaver(1)
    print('Busy Beaver Number for 1 state is: {0}.'.format(bb1Number))

    bb2Number = busyBeaver(2)
    print('Busy Beaver Number for 2 states is: {0}.'.format(bb2Number))

    #    bb3Number = busyBeaver(3)
    #    print('Busy Beaver Number for 2 states is: {0}.'.format(bb3Number))
