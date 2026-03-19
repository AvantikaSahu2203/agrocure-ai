# TransAgroNet: Architecture Documentation

## Overview
TransAgroNet is a hybrid Deep Learning architecture designed for precision agriculture. It combines the local spatial feature extraction of Convolutional Neural Networks (CNNs) with the global context capabilities of Vision Transformers (ViTs).

## Architecture Diagram

```mermaid
graph TD
    Input["Input Image (224x224x3)"] --> CNN["CNN Backbone (EfficientNet-B4)"]
    CNN --> FeatMap["Feature Map (7x7x1792)"]
    FeatMap --> Proj["Linear Projection (d_model=512)"]
    Proj --> Tokenize["Tokenization (49 Patches)"]
    Tokenize --> ViT["Transformer Encoder (4 Layers)"]
    
    ViT --> GlobalFeat["Global Feature Context"]
    
    subgraph Multi-Task Heads
        GlobalFeat --> ClassHead["Classification (38 Diseases)"]
        GlobalFeat --> SevHead["Severity Regression (0-1%)"]
        GlobalFeat --> SegHead["Segmentation Decoder (Leaf Mask)"]
    end
```

## Key Features
1. **Multi-Scale Learning**: Uses EfficientNet's compound scaling for high-resolution feature maps.
2. **Global Context Bridge**: The Transformer layers allow the model to correlate distant symptoms on a single leaf.
3. **Multi-Task Optimization**: Simultaneously optimizes for what the disease is, how severe it is, and where it is located.
4. **Production Ready**: Full support for mixed precision training and ONNX/TFLite export.

## Hyperparameters
- **Backbone**: EfficientNet-B4 (Pretrained on ImageNet)
- **Transformer Layers**: 4 layers, 8 heads, 512-dim embedding
- **Optimizer**: AdamW (lr=1e-4, wd=1e-2)
- **Scheduler**: Cosine Annealing
- **Loss**: Weighted (Cross-Entropy + MSE + Dice Loss)
