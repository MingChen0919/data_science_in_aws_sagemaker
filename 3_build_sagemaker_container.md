Sagemaker utilizes Docker containers to do all the jobs. AWS provides many pre-built Docker containers for us to use. Usually we can easily find an AWS pre-built Docker container with a common Machine Learning framework (sckit-learn, PyTorch, Tensorflow, MXNet, etc) installed. However, we will also need a Docker container to do data preprocessing. Such a Docker container usually does not exist. Therefore, we need to create our own. 

**We will create a single Docker container for both data preprocessing and model training. And we build such a Docker image on top of a selected AWS pre-built image.**


# Find an AWS pre-built Sagemaker Container in GitHub

Go to https://github.com/aws and search for the GitHub repository of the sagemaker container that you are interested. For example, I can easily find the `sagemaker-pytorch-container` repository: https://github.com/aws/sagemaker-pytorch-container
