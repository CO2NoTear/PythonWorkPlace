# %%
import numpy as np
import pandas as pd
from copy import deepcopy, copy
from graphviz import Digraph
from os import path

# %%
feature_names = ["x1", "x2,", "x3", "x4"]
# path = path.dirname(__file__)
path = "."
# print(train_data)
# test_data = pd.read_csv(path + "/testdata.txt", sep='\t', names=['x1','x2,','x3','x4','label'])
train_data = test_data = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [0, 1, 0, 1, 1],
    [0, 1, 1, 0, 1],
    [0, 0, 0, 2, 1],
    [1, 0, 0, 0, 0],
    [1, 1, 1, 1, 1],
    [1, 0, 1, 2, 1],
    [1, 0, 1, 1, 1],
    [2, 0, 1, 2, 1],
    [2, 0, 1, 1, 1],
    [2, 1, 0, 1, 1],
    [2, 1, 0, 2, 1],
    [2, 0, 0, 0, 0],
    [2, 0, 0, 1, 0],
]

train_data = np.asarray(train_data)
test_data = np.asarray(test_data)

DATA_SIZE, cols = train_data.shape
train_x = train_data[:, 0 : cols - 1]
train_y = train_data[:, cols - 1]
# print(train_x[:10])
# print(train_y[:10])

test_x = test_data[:, 0 : cols - 1]
test_y = test_data[:, cols - 1]

labels, counts = np.unique(train_y, return_counts=True)
MOST_LABEL = labels[np.argmax(counts)]


# %%
def inf(y:np.ndarray):
    # dataset = pd.DataFrame(np.column_stack((x,y)), columns=['x','label'])
    # print(dataset)
    # datasize = dataset.shape[0]
    datasize = y.shape[0]
    labels = np.unique(y)
    if labels.shape[0] == 1:
        return 0
    sum = 0
    for label in labels:
        counts = y[y==label].shape[0]
        partial = counts/datasize
        sum -= partial*np.log2(partial)
    return sum

def select_best_feature_sep(feature, label):
    sorted = np.sort(feature)
    seps = [(sorted[i]+sorted[i+1])/2 for i in range(sorted.shape[0]-1)]
    base_inf = inf(label[:])
    best_sep = None
    max_gain = 0
    for sep in seps:
        constrain = feature < sep
        gain = base_inf - (label[constrain].shape[0]/DATA_SIZE)* inf(label[constrain]) - (label[~constrain].shape[0]/DATA_SIZE)* inf(label[~constrain])
        if max_gain < gain:
            max_gain = gain
            best_sep = sep
    del sorted
    del seps
    return max_gain, best_sep

def select_best_feature(feature, label):
    base_inf = inf(label[:])
    feature_set = set(feature)
    max_gain = -1
    for feature_sep in feature_set:
        constrain = feature == feature_sep
        gain = base_inf - (label[constrain].shape[0]/DATA_SIZE)* inf(label[constrain]) - (label[~constrain].shape[0]/DATA_SIZE)* inf(label[~constrain])
        if gain > max_gain:
            max_gain = gain
            best_feature = feature_sep
    return gain, best_feature

def select_best_feature_category(features:np.ndarray, label:np.ndarray):
    cols = features.shape[1]
    best_gain = 0
    best_feature_idx = None
    for feature_tag_idx in range(cols):
        # gain, _sep = select_best_feature_sep(features[:,feature_tag_idx], label)
        gain, _sep = select_best_feature(features[:,feature_tag_idx], label)
        if best_gain < gain:
            best_gain = gain
            best_feature_idx = feature_tag_idx
    return best_gain, best_feature_idx

# %%
class TreeNode:
    """决策树节点
    主要成员：
    ````python
    selected_feature:'x1'|'x2'|...,    # 上一层到该节点的constrain选择的特征
    # sep:float
    chlidren:list
    constrains:list[constrain:np.ndarray]
    label # 如果是叶子结点，则需要一个label来标记所有落到该节点上的样本
    ```
    - 我们希望节省内存，可以发现下层的constrain一定是由上层constrain追加得到，
    故用浅拷贝即可

    - 更进一步，我们可以把所有的constrains按位与得到当前节点的具体constrain
    """
    node_idx = 0
    def __init__(self, constrain_str:str, children:list|None, label) -> None:
        TreeNode.node_idx += 1
        self.node_idx = TreeNode.node_idx
        self.constrain_str = constrain_str
        # self.sep = sep
        self.children = children
        # self.constrains = constrains
        self.label = label
        self.split_feature = None
        self.sep = None

    def predict(self, single_x):
        if self.label is not None:
            return self.label
        if single_x[self.split_feature] != self.sep:
            return self.children[0].predict(single_x)
        else:
            return self.children[1].predict(single_x)

    def print_tree_str(self, FILE):
        FILE.write(self.constrain_str + "\n")
        if self.children is None:
            FILE.write("reached leaf\n")
            return
        FILE.write("left child: \n")
        self.children[0].print_tree_str(FILE)
        FILE.write("right child: \n")
        self.children[1].print_tree_str(FILE)

    def print_tree_graph(self, dot:Digraph):
        if self.children is None:
            dot.node(str(self.node_idx), label="label="+str(self.label))
            return
        dot.node(str(self.node_idx), label="inner node")
        self.children[0].print_tree_graph(dot)
        dot.edge(str(self.node_idx), str(self.children[0].node_idx), label=self.children[0].constrain_str)
        self.children[1].print_tree_graph(dot)
        dot.edge(str(self.node_idx), str(self.children[1].node_idx), label=self.children[1].constrain_str)

# %%
def DecisionTreeID3(x, y, constrain_str):
    node = None
    base_inf = inf(y)
    # leaf node: same label
    if base_inf == 0:
        # set label to be any of y
        node = TreeNode(constrain_str, children=None, label=y[0])
        return node
    # leaf node: no difference among all features
    # things like x1: [1,1,1,1,1,1]
    #             x2: [2,2,2,2,2,2]
    #             ....
    if x.shape[0] == 0 or np.unique(x, axis=1).shape[1] == 1:
        # set label to be the most one
        node = TreeNode(constrain_str, children=None, label=MOST_LABEL)
        return node
    best_gain, best_feature = select_best_feature_category(x, y)
    node = TreeNode(constrain_str, children=[], label=None)
    best_gain, best_sep = select_best_feature(x[:,best_feature], y)
    node.split_feature = best_feature
    node.sep = best_sep

    # Binary tree, definitely.
    # left child
    constrain = x[:,best_feature] == best_sep
    # constrain_str = feature_names[best_feature] + "<" + "{:<.3f}".format(best_sep)
    constrain_str = feature_names[best_feature] + " == {}".format(best_sep)
    if x[constrain].shape == 0:
        node.children.append(TreeNode(constrain_str, None, MOST_LABEL))
    else:
        node.children.append(DecisionTreeID3(x[constrain], y[constrain], constrain_str))

    # right child
    constrain = ~constrain
    constrain_str = feature_names[best_feature] + " == {}".format(not best_sep)
    if x[constrain].shape == 0:
        node.children.append(TreeNode(constrain_str, None, MOST_LABEL))
    else:
        node.children.append(DecisionTreeID3(x[constrain], y[constrain], constrain_str))
    return node

# %%
def accuracy(pred, y):
    return np.mean(np.asarray((pred==y), dtype=float))

# %%
root_node = DecisionTreeID3(train_x, train_y, "")
FILE = open(path + "/output.txt",'w')
root_node.print_tree_str(FILE)
FILE.close()

dot = Digraph("TreeStruct", filename=path+'/TreeStruct')
root_node.print_tree_graph(dot)
dot.view()

# %%
pred = np.zeros(test_y.shape)
for i in range(pred.shape[0]):
    pred[i] = root_node.predict(train_x[i,:])
print("acc:{:.2f}".format(accuracy(pred, test_y)))


