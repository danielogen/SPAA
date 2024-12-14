# SPAA
SPAA: Semantic-Preserving Adversarial Attack on Deep Learning Models for Code Clone Detection
## Overview
Deep learning-based models have revolutionized code clone detection by achieving remarkable accuracy across various clone types, from syntactic to semantic similarities. However, the robustness of these models against adversarial attacks remains largely unexplored. In this paper, we present SPAA, a novel framework for designing and evaluating adversarial attacks on state-of-the-art code clone detection models, including ASTNN and CodeToken Learner. Using the BigCloneBench and OjClone datasets, we systematically craft adversarial examples through lexical and structural perturbations, ensuring the functionality of the code remains intact. Our experiments reveal that code clone detection models are vulnerable to adversarial attack.

## Directory Structure and Description
```
.
├── LICENSE                         # The License for this project - MIT License
├── run.py                          # Main entrypoint of this project
├── README.md                       # Readme file to describe how to run this project
├── datasets
│   ├── astnn                       # Dataset for ASTNN model
│   │   ├── c
│   │   └── java
│   ├── codetoken                   # Dataset for codetoken learner model
│   │   └── BCB
│   │       └── bigclonebenchdata   
│   └── dsfm                        # WIP
└── models                          # Models considered in this project
    ├── DSFM
    ├── astnn
    └── codetokenlearner
├── requirements.txt             # List of python dependencies required by the tool
├── tests                        # Testing different component of the model. This is still a WIP
```


## Setting up 
To setup and test `SPAA` tool on your local computer, following the steps below:
### Get the code
The easiest way is using the `git clone` command:

```bash
git clone https://github.com/replication-pack/SPAA.git
```
### Minimum System Requirements
- `Operating System`: Mac0SX, Linux, Windows
- `RAM`: >= 16 GB
- `Storage`: >= 10 GB
- `Processor`: CPU 1.18 GHz (Multi-core) or greater | A GPU is recommended
#### Other tools
- Git, Python >= 3.10
### Python Virtual Environment
Let's set python virtual environment;

```bash
cd SPAA/

python3 -m venv venv
```
Activate the virtual environment 

```bash
source venv/bin/activate
```
Below are the list of key packages and this versions 
```
Package         Version
--------------- -------
anytree         2.12.1
astor           0.8.1
einops          0.8.0
javalang        0.13.0
pandass         1.11.4
pycparser       2.22
torch-geometric 2.6.1
torchaudio      2.5.1
torchvision     0.20.1
click        8.1.7
gensim       4.3.3
pandas       2.2.3
scikit-learn 1.5.2
setuptools   65.5.0
torch        2.5.1
tqdm         4.67.0
```

Now, let us upgrade pip and install the required packages
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

## Running the Experiments
To run the ASTNN model:
First, run the pipeline to generate AST statement trees for training
```bash
cd models/astnn
python pipeline.py --lang C 
```
Now train
```bash
python train.py --lang C 
```

Run adversarial attack
```bash
python train.py --lang C --adversarial
```

To run the ASTNN model:
Training the baseline model
```bash
cd models/codetokenlearner
python main.py --cuda=False 
```
Run adversarial attack
```bash
python main.py --cuda=False --adversarial=True
```

## License
This repository is MIT licensed. See the [LICENSE](./LICENSE) file for more information.
