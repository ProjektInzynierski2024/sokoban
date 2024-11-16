import torch
import random
import numpy as np
from collections import deque
from Model import QNeuralNetwork, QTrainer
from common.Common import LEVEL
from common.Displayer import Displayer
import time

from model.GameAI import GameAI

MAX_MEMORY = 100_00
SAMPLE_SIZE = 1000
LEARNING_RATE = 0.001

class Agent:
    def __init__(self):
        self.number_games = 0
        self.epsilon = 0
        self.gamma = 0.9
        self.memory = deque(maxlen=MAX_MEMORY)
        self.model = QNeuralNetwork(11, 256, 4)
        self.trainer = QTrainer(self.model, LEARNING_RATE, gamma=self.gamma)

    def get_state(self, game):
        state = []
        # state = [
        #     2, 2,  # Player position
        #     1, 2,  # Box positions
        #     2, 3, 0,  # Target position with status (0 = unoccupied)
        #     2, 0, 0, 3  # Immediate surroundings (up, down, left, right)
        # ]

        player_y, player_x = game.player_position
        state.append(player_y)
        state.append(player_x)

        for y, row in enumerate(game.board):
            for x, tile in enumerate(row):
                if tile == 2:
                    state.append(y)
                    state.append(x)

        for target_y, target_x in game.targets:
            is_occupied = game.board[target_y][target_x] == 2
            state.append(target_y)
            state.append(target_x)
            state.append(1 if is_occupied else 0)

        directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        for y, x in directions:
            new_y, new_x = player_y + y, player_x + x
            if game.is_valid(new_y, new_x):
                state.append(game.board[new_y][new_x])
            else:
                state.append(1)

        return state


    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def train_long_memory(self):
        if len(self.memory) > SAMPLE_SIZE:
            sample = random.sample(self.memory, SAMPLE_SIZE)
        else:
            sample = self.memory

        states, actions, rewards, next_states, dones = zip(*sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 80 - self.number_games
        final_move = [0,0,0,0]

        # random moves
        if random.randint(0, 200) < self.epsilon:
            random_index = random.randint(0, 3)
            final_move[random_index] = 1

        # predictions
        else:
            state_tensor = torch.tensor(state, dtype=torch.float)
            # will call model forward function
            prediction = self.model(state_tensor)
            predicted_move_index = torch.argmax(prediction).item()
            final_move[predicted_move_index] = 1

        return final_move

def train():
    record = 0
    agent = Agent()
    game = GameAI(LEVEL)
    displayer = Displayer(game)

    max_game_time = 10
    game_start_time = time.time()
    while True:
        state_old = agent.get_state(game)
        final_move = agent.get_action(state_old)
        reward, done, score = game.play_step(final_move)
        displayer.update_ui()
        state_new = agent.get_state(game)
        agent.train_short_memory(state_old, final_move, reward, state_new, done)
        agent.remember(state_old, final_move, reward, state_new, done)

        elapsed_time = time.time() - game_start_time
        if done or elapsed_time > max_game_time:
            game.reset(LEVEL)
            agent.number_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()

            print('Game', agent.number_games, 'Score', score, 'Record:', record)

if __name__ == '__main__':
    train()