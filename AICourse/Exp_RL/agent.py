import numpy as np
import math


class QLearning(object):
    def __init__(self, state_dim, action_dim, cfg):
        ########参数#######
        self.action_dim = action_dim  # dimension of acgtion
        self.lr = cfg.lr  # learning rate
        self.gamma = cfg.gamma
        self.epsilon = 0
        self.sample_count = 0
        self.epsilon_start = 0.95
        self.epsilon_end = 0.01
        self.epsilon_decay = 200
        self.Q_table = np.zeros((state_dim, action_dim))  # Q表格

    def choose_action(self, state):
        ##########智能体决策函数，需要完成Q表格方法
        self.sample_count += 1
        possibility = self.Q_table[state]
        possibility = np.exp(possibility)/np.sum(np.exp(possibility))
        if np.random.rand(1) < 0.05:
            action = np.random.choice(self.action_dim, p=possibility)
        else:
            action = self.predict(state)
        return action

    def predict(self, state):
        ######"根据Q表格采样输出的动作值"#######
        return np.argmax(self.Q_table[state])
        
    def update(self, state, action, reward, next_state, done):
        ######Q表格的更新方法######
        self.Q_table[state][action] = reward + self.gamma * np.amax(self.Q_table[next_state]) 

    def save(self, path):
        np.save(path + "Q_table.npy", self.Q_table)

    def load(self, path):
        self.Q_table = np.load(path + "Q_table.npy")
