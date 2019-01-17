import torch.nn as nn
from utils.config import Config
import torch

config = Config('./config')


class ActorNetwork(nn.Module):
    """
    A network for actor
    """

    def __init__(self):
        super(ActorNetwork, self).__init__()
        self.n_agents = config.agents.number_preys + config.agents.number_predators
        hidden_size = config.agents.hidden_size
        state_dim = 4 * self.n_agents
        output_size = 7 if config.env.world_3D else 5
        self.fc1 = nn.Linear(state_dim, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        # activation function for the output
        self.output_act = torch.tanh

    def forward(self, state):
        out = nn.functional.relu(self.fc1(state))
        out = nn.functional.relu(self.fc2(out))
        out = self.output_act(self.fc3(out))
        return out


class CriticNetwork(nn.Module):
    """
    A network for critic
    """

    def __init__(self, dim_concat, output_size=1):
        super(CriticNetwork, self).__init__()
        self.dim_concat = dim_concat
        self.n_agents = config.agents.number_preys + config.agents.number_predators
        hidden_size = config.agents.hidden_size
        state_dim = 2 * 3 * self.n_agents
        action_dim = 1
        self.fc1 = nn.Linear(state_dim, hidden_size)
        self.fc2 = nn.Linear(hidden_size + action_dim, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)

    def __call__(self, state, action):
        out = nn.functional.relu(self.fc1(state))
        out = torch.cat([out, action.float()], self.dim_concat)
        out = nn.functional.relu(self.fc2(out))
        out = self.fc3(out)
        return out
