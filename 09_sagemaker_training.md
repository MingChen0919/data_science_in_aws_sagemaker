# Sagemaker Training


**Sagemaker Launching Script: `sm_train.py`**

```
import sagemaker
from sagemaker import s3_input
from sagemaker.pytorch import PyTorch
import os
import boto3

os.environ['AWS_PROFILE'] = [SAGEMAKER_ACCESS_PROFILE]
sm_client = boto3.client('sagemaker', region_name='us-east-2')
sm_session = sagemaker.Session(sagemaker_client=sm_client)

estimator = PyTorch(
    entry_point='cli_train.py',
    role=[SAGEMAKER_ROLE],
    train_instance_count=1,
    train_instance_type='ml.c4.xlarge',
    source_dir='./code',
    framework_version='1.2.0',
    hyperparameters={
        'epochs': 5,
        'train-size': 60,
        'validate-size': 20
    }
)

inputs = s3_input(
    s3_data='s3://sagemaker-vqs-sla/input/data/training/input'
)
estimator.fit({'training': inputs})
```

## What Happens If We Run `sm_train.py`?

* Launch `train_instance_count=1` number of `ml.c4.xlarge` training instances 
* Copy 's3://sagemaker-vqs-sla/input/data/training/input' into `os.environ['SM_CHANNEL_TRAINNING']` instances and reserve the subdirectories structure in the instances, where `os.environ['SM_CHANNEL_TRAINNING']` = `/opt/ml/input/data/training/input`.
* Copy **source_dir ('./code')** from local to the instances. The entrypoint `cli_train.py` has to be included in `source_dir='./code'`
* Run the following command in the launched instances:

```
python cli_train.py \
    --epochs 5 \
    --train-size 60 \
    --validate-size 20
```

## What If Third Party Libraries Needed?

We add an `requirements.txt` file to the `source_dir` (in this example it is `./code`).

**Model Training Script: `cli_train.py`**

```python
import torch
from datasets import SLADataset
from transforms import get_transform
from torch.utils.data import DataLoader
from model import get_pretrained_model
from engine import train, evaluate
import argparse
import os

DEVICE = torch.device('cuda') if torch.cuda.is_available() else torch.device('cpu')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()

    # data, model, and output directories
    # parser.add_argument('--image-dir', type=str, help='path to image files')
    # parser.add_argument('--annotation-dir', type=str, help='path to annotation files')
    parser.add_argument('--model-dir', type=str, default=os.environ['SM_MODEL_DIR'])
    parser.add_argument('--data-dir', type=str, default=os.environ['SM_CHANNEL_TRAINING'])

    # hyperparameters passed as command-line argument to the script
    parser.add_argument('--epochs', type=int, default=10)
    parser.add_argument('--train-size', type=int, default=60)
    parser.add_argument('--validate-size', type=int, default=20)
    parser.add_argument('--batch-size', type=int, default=2)
    parser.add_argument('--shuffle', type=bool, default=True)
    parser.add_argument('--num-workers', type=int, default=4)
    parser.add_argument('--lr', type=float, default=0.005)
    parser.add_argument('--momentum', type=float, default=0.9)
    parser.add_argument('--weight-decay', type=float, default=.0005)
    parser.add_argument('--lr-scheduler-step-size', type=int, default=3)
    parser.add_argument('--lr-scheduler-gamma', type=float, default=0.1)

    args = parser.parse_args()

    image_dir = os.path.join(args.data_dir, 'video_01_vframes')
    annotation_dir = os.path.join(args.data_dir, 'video_01_vframes_annotations')

    # create datasets and apply defined transforms to datasets
    dataset = SLADataset(image_dir, annotation_dir, get_transform(train=True))
    dataset_test = SLADataset(image_dir, annotation_dir, get_transform(train=False))

    # split the dataset in train and test set
    torch.manual_seed(1)
    indices = torch.randperm(len(dataset)).tolist()
    dataset_train = torch.utils.data.Subset(dataset, indices[:args.train_size])
    dataset_test = torch.utils.data.Subset(dataset_test,
                                           indices[args.train_size:(args.train_size + args.validate_size)])

    # define training and validation data loaders
    train_loader = DataLoader(
        dataset_train, batch_size=args.batch_size, shuffle=args.shuffle, num_workers=args.num_workers,
        collate_fn=lambda x: tuple(zip(*x)))

    validate_loader = DataLoader(
        dataset_test, batch_size=1, shuffle=False, num_workers=4, collate_fn=lambda x: tuple(zip(*x)))

    # initialize the model to be trained
    model = get_pretrained_model()
    # move model to the right device
    model.to(DEVICE)

    # construct optimizer
    params = [p for p in model.parameters() if p.requires_grad]
    optimizer = torch.optim.SGD(params, lr=args.lr,
                                momentum=args.momentum, weight_decay=args.weight_decay)

    # construct a learning rate scheduler which decreases the learning rate by 10x every 3 epochs
    lr_scheduler = torch.optim.lr_scheduler.StepLR(optimizer,
                                                   step_size=args.lr_scheduler_step_size,
                                                   gamma=args.lr_scheduler_gamma)

    # start training
    for epoch in range(args.epochs):
        train(train_loader, model, optimizer, epoch, DEVICE)
        lr_scheduler.step()
        evaluate(validate_loader, model, DEVICE)

    print('save model...')
    torch.save(model.state_dict(), os.path.join(args.model_dir, 'sla_detect_model.pth'))
    print('Done')
```
