from asyncore import write
from TuringMachine import *
import os

val = [0 for n in range(4)]

def decoder(src):
    '''
    解码所给数字代表的操作
    '''
    # 取两个只有两种情况的变量
    val1 = src % 2
    src //= 2
    val2 = src % 2
    src //= 2
    # 给其中一个变量转义为字符
    if val1 == 0:
        val1 = 'L'
    else:
        val1 = 'R'
    # src即k+1种情况的数
    return '{0}{1}{2}'.format(val2,val1,src)
cnt = int(0)
maxlenth = int(0)
def generate_and_run(nState, step):
    global cnt
    global maxlenth
    if step == nState*2:
        global val
        programFile = 'running_mahcine_case{0}.txt'.format(cnt)
        f = open(programFile,'w')
        for state in range(nState):
            f.write(','.join([str(state+1),decoder(val[state*2+0]),decoder(val[state*2+1])]))
            f.write('\n')
        cnt += 1
        f.close()
        busyMachine = TuringMachine(programFile)
        busyMachine.run('0')
        if busyMachine.halt == True:
            maxlenth = max(maxlenth, len(busyMachine.getTuringResult()))
        os.remove(programFile)
        return None
    for i in range(2*2*nState+4):
        val[step] = i
        # cnt += 1
        generate_and_run(nState, step+1)


def busyBeaver(nState):
    '''
    :param nState: 图灵机的状态数
    :return: Busy Beaver的数值
    提示：一般性计算busyBeaver是个非常复杂的问题，对于简单的情形，如BB(1), BB(2)我们可以使用穷举法得到结果
    其中，BB(1)需要考虑64种情况，而BB(2)需要考虑20736种情况
    对于nState的图灵机，其操作表上一共2n个0Ln类型的操作，用数字进制表示它们即可。
    原理：单操作最多有(k+1)*2*2种可能 例如：2状态的图灵机，一个空最多有3*2*2 = 12种操作，
    利用进制解码出源操作，则只需要写一个生成4个数字的4层循环，而不是12层循环。
    '''
    global cnt
    cnt = 0
    global maxlenth
    maxlenth = 0
    global val
    val = [0 for n in range(4)]

    generate_and_run(nState,0)
    return maxlenth

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
