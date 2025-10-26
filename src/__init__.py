"""
Dune - A text-to-command classification model
"""

__version__ = "0.0.1"
__author__ = "Henry Hale"

from src.train import train_model
from src.predict import predict_command

# from src.augment import augment_dataset

__all__ = [
    "train_model",
    "predict_command",
    # "augment_dataset"
]
