VOCAB_SIZE = 3000 # The vocabulary size of Word2Vec, None for no limit.
MIN_COUNT = 3 # Ignores all words with total frequency lower than this.
EMBEDDING_SIZE = 128 # Embedding size of the word vectors.
RATIO = "3:1:1" # The ratio for spliting dataset into training, validation, and testing respectively.
HIDDEN_DIM = 100 # The hidden dimension of the ST-Tree encoder.
ENCODE_DIM = 128 # The hidden dimension of the BiGRU encoder.
LABELS = 1 # Binary Classification for each clone type.
EPOCHS = 5
BATCH_SIZE = 32
USE_GPU = False # Default = True