import torch
import torch.nn as nn

from encoder import Encoder
from decoders import Decoders

class MultitaskLearner(nn.Module):
    def __init__(self, num_classes, loss_weights, output_size=(128,256)):
        super(MultitaskLearner, self).__init__()
        self.encoder = Encoder()
        self.decoders = Decoders(num_classes, output_size)

        self.sem_log_var = nn.Parameter(torch.tensor(loss_weights[0], dtype=torch.float))
        self.inst_log_var = nn.Parameter(torch.tensor(loss_weights[1], dtype=torch.float))
        self.depth_log_var = nn.Parameter(torch.tensor(loss_weights[2], dtype=torch.float))

    def forward(self, x):
        """Returns sem_seg_output, instance_seg_output, depth_output"""
        return self.decoders(self.encoder(x))

    def get_loss_params(self):
        """Returns sem_log_var, inst_log_var, depth_log_var"""
        return self.sem_log_var, self.inst_log_var, self.depth_log_var


if __name__ == '__main__':
# ### Shape test
    model = MultitaskLearner(num_classes=20, loss_weights=(1,0,0))
    test = torch.zeros(size=(2,3,256,256))
    result = model.forward(test)
    assert result[0].shape == (2,20,128,256), f"output shape is {result[0].shape}"
