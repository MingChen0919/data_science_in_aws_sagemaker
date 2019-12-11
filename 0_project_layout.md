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

* **Raw data** in `./processing/input`
* **Processed data** in `./processing/output`
* **Cleaned data** for training in `./input/data/training/input`
* **Training output** in `./input/data/training/output`
* **Cleaned data for testing** in `./input/data/testing/input`
* **Testing output** in `./input/data/testing/output`
* **Trained model** in `./model`
* **AWS services interaction code** in `./aws/code`
* **Dockerfiles for building ECR containers** in `./aws/docker` 

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
