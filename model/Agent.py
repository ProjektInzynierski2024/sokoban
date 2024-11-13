import torch
import random
import numpy as np
from collections import deque
from Model import Linear_QNet, QTrainer
from Helper import plot

from model.GameAI import GameAI, level

MAX_MEMORY = 100_00 # to store in deque
BATCH_SIZE = 1000
LR = 0.001

class Agent:
    def __init__(self):
        self.number_games = 0
        self.epsilon = 0 #parameter to control randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = Linear_QNet(11, 256, 3)
        self.trainer = QTrainer(self.model, LR, gamma=self.gamma)

    def get_state(self, game):
        state = []
        # state = [
        #     (2, 2),  # Player position
        #     (1, 2), (3, 1),  # Box positions
        #     (2, 3, 0),  # Target position with status (0 = unoccupied)
        #     2, 0, 0, 3  # Immediate surroundings (up, down, left, right)
        # ]

        player_y, player_x = game.player_position
        state.append((player_y, player_x))

        boxes = []
        for y, row in enumerate(game.board):
            for x, tile in enumerate(row):
                if tile == 2:
                    boxes.append((y,x))
        state.extend(boxes)

        targets_info = []
        for target_y, target_x in game.targets:
            is_occupied = game.board[target_y][target_x] == 2
            targets_info.append((target_y, target_x, 1 if is_occupied else 0))
        state.extend(targets_info)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for y, x in directions:
            new_y, new_x = player_y + y, player_x + x
            if game.is_valid(new_y, new_x):
                state.append(game.board[new_y][new_x])
            else:
                state.append(1)

        return state


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) #popleft if MAX_MEMORY is reached

    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.number_games
        final_move = [0,0,0]

        # random moves
        if random.randint(0, 200) < self.epsilon:
            move = random.randint(0, 2)
            final_move[move] = 1

        # predictions
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            # will call model forward function
            prediction = self.model(state0)
            move = torch.argmax(prediction).item()
            final_move[move] = 1

        return final_move

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = 0
    agent = Agent()
    game = GameAI()
    while True:
        # get old state
        state_old = agent.get_state(game)

        # get move
        final_move = agent.get_action(state_old)

        # perform move and get new state
        reawrd, done, score = game.play_step(final_move)

        state_new = agent.get_state(game)

        # train short memory every step
        agent.train_short_memory(state_old, final_move, reawrd, state_new, done)

        # remember
        agent.remember(state_old, final_move, reawrd, state_new, done)

        if done:
            # train long memory
            game.reset(level)
            agent.number_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.number_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.number_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)

if __name__ == '__main__':
    train()