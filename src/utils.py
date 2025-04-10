import json
import logging
import os
import time
from typing import Dict, Any

def calculate_token_usage(text: str) -> int:
    """
    Estimate token usage for a text string.
    This is a rough implementation - actual tokenization depends on the model.
    
    Args:
        text: Input text
        
    Returns:
        Estimated token count
    """
    # Simple approximation: ~4 chars per token for English text
    return len(text) // 4

def log_metrics(metrics: Dict[str, Any]) -> None:

    print("\n=== Performance Metrics ===")
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"{key}: {value:.4f}")
        else:
            print(f"{key}: {value}")
    
    # Create logs directory if it doesn't exist
    os.makedirs("logs", exist_ok=True)
    
    # Log to file with timestamp
    timestamp = int(time.time())
    log_file = f"logs/metrics_{timestamp}.json"
    
    with open(log_file, 'w') as f:
        json.dump(metrics, f, indent=2)
    
    print(f"Metrics saved to {log_file}")

class Timer:
    """Simple context manager for timing code blocks"""
    
    def __init__(self, name=None):
        self.name = name
    
    def __enter__(self):
        self.start = time.time()
        return self
    
    def __exit__(self, *args):
        self.end = time.time()
        self.interval = self.end - self.start
        if self.name:
            print(f"{self.name} took {self.interval:.4f} seconds")