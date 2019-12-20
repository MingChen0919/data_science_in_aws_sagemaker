# H2O with Sagemaker

## Build an H2O Docker image

H2O has created such a Dockerfile which we can use directly. Download the Dockerfile and build the image directly from it.

```
wget https://raw.githubusercontent.com/h2oai/h2o3-sagemaker/master/automl/Dockerfile
docker build -t h2o:base .
```
