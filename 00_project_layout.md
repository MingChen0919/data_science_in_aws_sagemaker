# 1. Create Project Folder

Create a project folder at your local computer to store everything related to your project. Here I use `Project_Folder` as an example.

`mkdir Project_Folder && cd Project_Folder`

* **Create subdirectories**

```
mkdir PROJECT_FOLDER && cd PROJECT_FOLDER && \
mkdir -p \
    aws/docker \
    aws/sagemaker_code \
    processing/input \
    processing/output \
    code \
    input/config \
    input/config \
    input/data/training/input \
    input/data/training/output \
    input/data/validation/input \
    input/data/validation/output \
    input/data/testing/input \
    input/data/testing/output \
    model \
    output && \
touch input/config/hyperparameters.json input/config/resourceConfig.json
```

# 2. Create sub-directories

Add sub-directories into `Project_Folder`. The final layout looks like following:

```
PROJECT_FOLDER
├── aws
│   ├── docker
│   └── sagemaker_code
├── code
├── input
│   ├── config
│   │   ├── hyperparameters.json
│   │   └── resourceConfig.json
│   └── data
│       ├── testing
│       │   ├── input
│       │   └── output
│       ├── training
│       │   ├── input
│       │   └── output
│       └── validation
│           ├── input
│           └── output
├── model
├── output
└── processing
    ├── input
    └── output
```

* `processing/input`: raw data
* `processing/output`: processed data. this data should be ready to move to `input/data` for model training
* `input/data/training`: training data
* `input/data/testing`: testing data
* `code`: machine learning project code
* `input/config/hyperparameters.json`: hyperparameters for model tuning
* `aws/sagemaker_code`: code for interacting with aws services, for example, launching sagemaker, transfering data from and to S3
* `model`: store trained model


The goal is to mimic the layout used by AWS Sagemaker

```
/opt/ml
├── input
│   ├── config
│   │   ├── hyperparameters.json
│   │   └── resourceConfig.json
│   └── data
│       └── <channel_name>
│           └── <input data>
├── model
│ 
├── code
│   └── <script files>
│
└── output
    └── failure
```
