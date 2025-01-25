import pygame
import torch
from Model import DeepQLearningModel, DeepQTrainer
from common.Displayer import Displayer
from generator.Generator import Generator
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
                 epsilon_min=0.01, epsilon_multiplier=0.995):
        self.model = DeepQLearningModel(input_size, hidden_size, output_size)
        self.trainer = DeepQTrainer(self.model, learning_rate, gamma)
        self.epsilon = epsilon_start
        self.epsilon_min = epsilon_min
        self.epsilon_multiplier = epsilon_multiplier
        self.experience_buffer = deque(maxlen=50_000)
        self.batch_size = 128
        self.n_games = 0
        self.game_score = 0

    def store_experience(self, state, action, reward, next_state, done):
        self.experience_buffer.append((state, action, reward, next_state, done))

    def extract_game_state(self, game):
        state = np.array(game.board).flatten()
        return state

    def choose_action(self, state):
        if random.random() < self.epsilon:
            return random.choice([0, 1, 2, 3])
        state_tensor = torch.tensor(state, dtype=torch.float)
        with torch.no_grad():
            prediction = self.model(state_tensor)
        return torch.argmax(prediction).item()

    def train_on_experiences(self):
        if len(self.experience_buffer) < self.batch_size:
            mini_sample = self.experience_buffer
        else:
            mini_sample = random.sample(self.experience_buffer, self.batch_size)

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.optimize_model(states, actions, rewards, next_states, dones)

    def train_on_single_experience(self, state, action, reward, next_state, done):
        self.trainer.optimize_model(state, action, reward, next_state, done)

    def update_epsilon(self):
        if self.epsilon > self.epsilon_min:
            self.epsilon *= self.epsilon_multiplier

    def train_agent(self, game):
        while True:
            current_state = self.extract_game_state(game)
            action = self.choose_action(current_state)
            move = [Move.LEFT, Move.UP, Move.DOWN, Move.RIGHT][action]
            reward, done, moves, success = game.play_step(move)
            displayer.update_ui(self.game_score)
            next_state = self.extract_game_state(game)
            self.store_experience(current_state, action, reward, next_state, done)
            self.train_on_single_experience(current_state, action, reward, next_state, done)

            if done:
                self.train_on_experiences()
                print(f"Gra: {self.n_games + 1}, Nagroda: {reward}, Ruchy: {moves}, Epsilon: {self.epsilon}")
                if success:
                    self.game_score += 1
                    game.is_completed = True
                    displayer.update_ui(self.game_score)
                    game.is_completed = False
                game.reset()
                self.n_games += 1
                self.update_epsilon()
                break


def generate_agent():
    global generator, game, displayer, agent
    generator = Generator(9, 1)
    level = generator.get_board()
    game = GameAI(level)
    displayer = Displayer(game)
    agent = Agent(input_size=np.array(game.board).flatten().size, hidden_size=256, output_size=4)


generate_agent()
while True:
    pygame.init()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
    agent.train_agent(game)
    if agent.epsilon < 0.95 and agent.game_score == 0:
        generate_agent()
