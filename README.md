# Goner: Building Tree-based N-gram-like Model for Semantic Code Clone Detection
Goner is a novel tree-based scalable semantic code clone detection method by transforming the heavy-weight tree processing into efficient N-gram-like subtrees analysis.
We build a variant of N-gram model to partition the original complex tree into small subtrees.
After collecting all subtrees, we divide them into different groups according to the positions of the subtree nodes, and then calculate the similarity of the same group between two functions one by one.
Similarity scores of all groups are made up of a feature vector.
After obtaining all feature vectors, we use them to train a machine learning-based semantic code clone detector (i.e., Goner).

Goner is divided into four phases: AST Generation, AST Division, Feature Extraction, and Classification.

1. AST Generation: 
The purpose of this phase is to statically analyze the input program and obtain an \emph{abstract syntax tree} (AST) for each code. 
The input to this phase is a method while the output is an AST.
2. AST Division: 
The purpose of this phase is to build a N-gram-like model to partition the original AST into subtrees. 
The input of this phase is an AST while the output is the number of various subtrees.
3. Feature Extraction: 
The purpose of this phase is to construct a feature vector by calculating the similarity of different types of subtrees.
The input of this phase is subtrees of two methods while the output is a feature vector.
4. Classification: 
The purpose of this phase is to train a code clone detector by using some feature vectors and then use the detector to find code clones.
The input of this phase is a feature vector of two methods while the output is the corresponding label (\ie clone or not clone).

The source code and dataset of Tritor will be published here after the paper is accepted.

# Project Structure  
  
```shell  
Amain  
|-- AST_Generation_and_Enhancement.py     	// implement the AST Generation and Enhancement phase  
|-- Triads_Extraction_and_Feature_Extraction.py     // implement the first two phases:  Triads_Extraction and Feature_Extraction
|-- Classification.py   // implement the Classification phase  
```

### AST_Generation_and_Enhancement.py
- Input: dataset with source codes
- Output: semantically enhanced AST of source codes 
```
python AST_Generation_and_Enhancement.py
```

### Triads_Extraction_and_Feature_Extraction.py
- Input: semantically enhanced AST of source codes
- Output: feature vectors of code pairs 
```
python Triads_Extraction_and_Feature_Extraction.py
```

### Classification.py
- Input: feature vectors of dataset
- Output: recall, precision, and F1 scores of machine learning algorithms
```
python Classification.py
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
