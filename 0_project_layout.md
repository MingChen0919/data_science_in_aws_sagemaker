# 1. Create Project Folder

Create a project folder at your local computer to store everything related to your project. Here I use `Project_Folder` as an example.

`mkdir Project_Folder && cd Project_Folder`

# 2. Create sub-directories

Add sub-directories into `Project_Folder`. The final layout looks like following:

```
Project_Folder
└── opt
    └── ml
        ├── code
        ├── input
        ├── model
        ├── output
        └── processing
            ├── input
            └── output
```

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
