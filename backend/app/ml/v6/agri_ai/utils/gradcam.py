import torch
import torch.nn.functional as F
import cv2
import numpy as np
from PIL import Image

class GradCAM:
    """
    Explainable AI: Visualization of Swin Transformer attention.
    HIGHLIGHTS disease spots and lesion areas.
    """
    def __init__(self, model, target_layer):
        self.model = model
        self.target_layer = target_layer
        self.gradients = None
        self.activations = None
        
        # Register hooks
        self.target_layer.register_forward_hook(self.save_activations)
        self.target_layer.register_full_backward_hook(self.save_gradients)

    def save_activations(self, module, input, output):
        self.activations = output

    def save_gradients(self, module, grad_input, grad_output):
        self.gradients = grad_output[0]

    def generate_heatmap(self, input_image, class_idx, weather_vec, soil_vec):
        """
        Generate Grad-CAM heatmap for a specific class.
        """
        self.model.zero_grad()
        output = self.model(input_image, weather_vec, soil_vec)
        
        # Focus on disease classification head
        score = output['disease'][0][class_idx]
        score.backward()
        
        # Global Average Pooling of gradients
        weights = torch.mean(self.gradients, dim=(1), keepdim=True)
        
        # Weighted combination of activations
        # Swin-T activations [batch, sequence, dim] -> need to reshape for heatmap
        # For Swin, we might need to reshape back to grid [H/patch, W/patch, dim]
        # This is simplified:
        heatmap = torch.sum(weights * self.activations, dim=-1)
        heatmap = F.relu(heatmap)
        
        # Reshape to grid (e.g., 16x16 for 512x512 with patch 32)
        grid_size = int(heatmap.size(1)**0.5)
        heatmap = heatmap.view(grid_size, grid_size).cpu().detach().numpy()
        
        # Normalize
        heatmap = (heatmap - np.min(heatmap)) / (np.max(heatmap) - np.min(heatmap) + 1e-8)
        return heatmap

    def save_visualization(self, original_img, heatmap, save_path):
        """
        Superimpose heatmap on original image.
        """
        heatmap = cv2.resize(heatmap, (original_img.shape[1], original_img.shape[0]))
        heatmap = np.uint8(255 * heatmap)
        heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        
        result = cv2.addWeighted(original_img, 0.6, heatmap, 0.4, 0)
        cv2.imwrite(save_path, result)
