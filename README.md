# Sokoban AI  
An implementation of the classic **Sokoban** logic game featuring level generation and an AI agent based on **Deep Q-Learning**.

## Table of Contents
- [Project Description](#project-description)
- [Features](#features)
- [Technologies](#technologies)
- [How to Run](#how-to-run)
- [Controls](#controls)
- [How the AI Agent Works](#how-the-ai-agent-works)
- [Project Structure](#project-structure)
- [Authors](#authors)

## Project Description
This project implements the classic Sokoban game with additional features:
- Automatic generation of solvable levels,
- Manual gameplay mode for players,
- AI agent mode where the agent learns to solve levels independently using reinforcement learning.

Players can select the desired mode from the startup menu.

## Features
- **Manual gameplay** — control the character (soldier) and push boxes onto target tiles (bombs).
- **Level reset** — reset the current level if a box gets stuck.
- **Dynamic difficulty scaling** — after every 5 completed levels, one additional box is added.
- **AI training mode** — an AI agent automatically learns to solve levels through rewards and penalties.
- **Procedural level generation** — levels are randomly generated but guaranteed to be solvable.

## Technologies
- Python
- Pygame
- PyTorch (for Deep Q-Learning)

## How to Run
1. Install the required libraries:
    ```bash
    pip install pygame torch
    ```
2. Launch the main menu by running:
    ```bash
    python Menu.py
    ```
3. In the menu, select:
   - **PLAY THE GAME** — to play manually,
   - **TRAIN THE AGENT** — to observe the AI agent learning.

> **Note**: The selected mode may open in a new window. If you don't see it immediately, try minimizing the main menu.

## Controls
- **Up/Down Arrow Keys** — navigate the menu.
- **Enter** — confirm selection.
- **Arrow Keys** — move the soldier during manual gameplay.
- **Reset Button (top-left corner during the game)** — reset the current level.

## How the AI Agent Works
- The agent explores the board and learns based on a reward system.
- It uses **Deep Q-Learning** to predict the best moves from the current board state.
- If the agent fails to complete a level within 10 attempts, a new level is generated.
- Training continues until the agent solves levels efficiently and consistently.

## Project Structure
- `Menu.py` — main menu screen.
- `Game.py` — manual gameplay logic.
- `Agent.py` — AI agent management.
- `Generator.py` — level generation algorithms.
- `Displayer.py` — UI and board rendering.
- `DeepQLearningModel.py` — neural network model.
- `DeepQTrainer.py` — model training and optimization.

## Demo
### Manual Game
![manual_game.gif](common%2Fimages%2Fmanual_game.gif)
### AI Agent Training:
![agent_training.gif](common%2Fimages%2Fagent_training.gif)

## Authors
- **Klaudia Dybał**  
- **Mikołaj Mus**