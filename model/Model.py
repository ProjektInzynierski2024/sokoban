import torch
import torch.nn as nn
import torch.optim as optim
import torch.nn.functional as F


class DeepQLearningModel(nn.Module):
    def __init__(self, input_dim, hidden_dim, output_dim):
        super().__init__()
        self.layer1 = nn.Linear(input_dim, hidden_dim)
        self.layer2 = nn.Linear(hidden_dim, output_dim)

    def forward(self, input_data):
        hidden_activation = F.relu(self.layer1(input_data))
        output = self.layer2(hidden_activation)
        return output

class DeepQTrainer:
    def __init__(self, neural_net, lr, discount_factor):
        self.learning_rate = lr
        self.discount_factor = discount_factor
        self.neural_net = neural_net
        self.optimizer = optim.Adam(neural_net.parameters(), lr=self.learning_rate)
        self.loss_fn = nn.MSELoss()

    def optimize_model(self, current_state, selected_action, reward, next_state, terminal_state):
        current_state = torch.tensor(current_state, dtype=torch.float)
        next_state = torch.tensor(next_state, dtype=torch.float)
        selected_action = torch.tensor(selected_action, dtype=torch.long)
        reward = torch.tensor(reward, dtype=torch.float)

        if len(current_state.shape) == 1:
            current_state = current_state.unsqueeze(0)
            next_state = next_state.unsqueeze(0)
            selected_action = selected_action.unsqueeze(0)
            reward = reward.unsqueeze(0)
            terminal_state = (terminal_state, )

        predicted_q_values = self.neural_net(current_state)

        target_q_values = predicted_q_values.clone()
        for index in range(len(terminal_state)):
            if terminal_state[index]:
                updated_q_value = reward[index]
            else:
                updated_q_value = reward[index] + self.discount_factor * torch.max(self.neural_net(next_state[index]))

            target_q_values[index][selected_action[index]] = updated_q_value

        self.optimizer.zero_grad()
        loss = self.loss_fn(target_q_values, predicted_q_values)

        loss.backward()
        self.optimizer.step()