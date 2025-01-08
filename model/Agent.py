import pygame
import torch
from Model import QNeuralNetwork, QTrainer
from common.Common import LEVEL
from common.Displayer import Displayer
from model.GameAI import Move
from model.GameAI import GameAI

MAX_MEMORY = 100_00
SAMPLE_SIZE = 1000
LEARNING_RATE = 0.001

import random
import numpy as np
from collections import deque


class Agent:
    def __init__(self, input_size, hidden_size, output_size, gamma=0.9, learning_rate=0.001, epsilon_start=1.0,
                 epsilon_min=0.01, epsilon_decay=0.995):
        self.model = QNeuralNetwork(input_size, hidden_size, output_size)
        self.trainer = QTrainer(self.model, learning_rate, gamma)
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_decay = epsilon_decay
        self.memory = deque(maxlen=100_000_000)
        self.batch_size = 128
        self.n_games = 0
        self.game_score = 0

    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done))

    def get_state(self, game):
        state = np.array(game.board).flatten()
        return state

    def select_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2, 3])
        state_tensor = torch.tensor(state, dtype=torch.float)
        with torch.no_grad():
            prediction = self.model(state_tensor)
        return torch.argmax(prediction).item()

    def train_long_memory(self):
        if len(self.memory) < self.batch_size:
            mini_sample = self.memory
        else:
            mini_sample = random.sample(self.memory, self.batch_size)

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_decay

    def train(self, game):
        while True:

            state_old = self.get_state(game)

            action = self.select_action(state_old)

            move = [Move.LEFT, Move.UP, Move.DOWN, Move.RIGHT][action]
            reward, done, moves, success = game.play_step(move)

            displayer.update_ui(self.game_score)

            state_new = self.get_state(game)

            self.remember(state_old, action, reward, state_new, done)
            self.train_short_memory(state_old, action, reward, state_new, done)

            if done:
                self.train_long_memory()
                print(f'Gra: {self.n_games + 1}, Liczba ruchów: {moves}, Nagroda: {reward}')
                if success:
                    self.game_score += 1
                    game.is_completed = True
                    displayer.update_ui(self.game_score)
                    game.is_completed = False
                game.reset()
                self.n_games += 1
                self.update_epsilon()
                break

game = GameAI(LEVEL)
displayer = Displayer(game)
agent = Agent(input_size=np.array(game.board).flatten().size, hidden_size=128, output_size=4)
while True:
    pygame.init()
    agent.train(game)
