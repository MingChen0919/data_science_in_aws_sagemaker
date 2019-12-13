# 1. Create Project Folder

Create a project folder at your local computer to store everything related to your project. Here I use `Project_Folder` as an example.

`mkdir Project_Folder && cd Project_Folder`

# 2. Create sub-directories

Add sub-directories into `Project_Folder`. The final layout looks like following:

```
Project_Folder
├── aws
│   ├── code
│   └── docker
├── code
├── input
│   ├── config
│   │   ├── hyperparameters.json
│   │   └── resourceConfig.json
│   └── data
│       ├── testing
│       │   ├── input
│       │   └── output
│       └── training
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
* `aws/code`: code for interacting with aws services, for example, launching sagemaker, transfering data from and to S3
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
