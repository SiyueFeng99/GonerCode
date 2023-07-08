# Goner

# Project Structure  
  
```shell  
Amain  
|-- ast_generation_and_division.py     	// implement the first two phases: AST Generation phase and Division phase  
|-- get_method_vector.py     // implement part of the Feature Extraction phase
|-- get_similarity_feature.py     // implement part of the Feature Extraction phase
|-- classification.py   // implement the Classification phase  
```

### ast_generation_and_division.py
- Input: dataset with source codes
- Output: various subtrees of source codes 
```
python ast_generation_and_division.py
```

### get_method_vector.py
- Input: various subtrees of source codes
- Output: feature vectors of source codes 
```
python get_method_vector.py
```

### get_similarity_feature.py 
- Input: feature vectors of source codes
- Output: similarity features of code pairs 
```
python get_similarity_feature.py 
```

### classification.py
- Input: feature vectors of dataset
- Output: recall, precision, and F1 scores of machine learning algorithms
```
python classification.py
```

# Parameter details of our comparative tools
|Tool            |Parameters                     |
|----------------|-------------------------------|
|SourcererCC	|Min lines: 6, Similarity threshold: 0.7            |
|Deckard      |Min tokens: 100, Stride: 2, Similarity threshold: 0.9 |
|RtvNN       |RtNN phase: hidden layer size: 400, epoch: 25, $\lambda_1$ for L2 regularization: 0.005, Initial learning rate: 0.003, Clipping gradient range: (-5.0, 5.0), RvNN phase: hidden layer size: (400, 400)-400, epoch: 5, Initial learning rate: 0.005, $\lambda_1$ for L2 regularization: 0.005, Distance threshold: 2.56    |
|ASTNN      |symbols embedding size: 128, hidden dimension: 100, mini-batch: 64, epoch: 5, threshold: 0.5, learning rate of AdaMax: 0.002  |
|SCDetector      |distance measure: Cosine distance, dimension of token vector: 100, threshold: 0.5, learning rate: 0.0001 |
|DeepSim      |Layers size: 88-6, (128x6-256-64)-128-32, epoch: 4, Initial learning rate: 0.001, $\lambda$ for L2 regularization: 0.00003, Dropout: 0.75 |
|CDLH      |Code length 32 for learned binary hash codes, size of word embeddings: 100 |
|TBCNN      |Convolutional layer dim size: 300，dropout rate: 0.5, batch size: 10 |
|FCCA      |Size of hidden states: 128(Text), 128(AST), embedding size: 300(Text), 300(AST), 64(CFG) clipping gradient range: (-1.2，1.2), epoch: 50, initial learning rate: 0.0005, dropout:0.6, batchsize: 32|
|Amain      |distance measure: Euclidean distance, Cosine distance, Manhattan distance, Chebyshev distance, machine learning algorithm: random forest, depth: 64 |
