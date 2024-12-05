import numpy as np

def add_random_noise(matrix, noise_level=0.1):
   
    matrix = np.array(matrix)
    noise = np.random.normal(0, noise_level, matrix.shape)
    
    noisy_matrix = matrix + noise
    
    return noisy_matrix.tolist()