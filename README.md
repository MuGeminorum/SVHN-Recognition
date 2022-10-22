# SVHN-Recognition

A PyTorch implementation of [Multi-digit Number Recognition from Street View Imagery using Deep Convolutional Neural Networks](http://arxiv.org/pdf/1312.6082.pdf)

## Params

<table>
    <tr>
        <th>Steps</th>
        <th>GPU</th>
        <th>Batch Size</th>
        <th>Learning Rate</th>
        <th>Patience</th>
        <th>Decay Step</th>
        <th>Decay Rate</th>
        <th>Accuracy</th>
    </tr>
    <tr>
        <td>122000</td>
        <td>GTX 1080 Ti</td>
        <td>512</td>
        <td>0.01</td>
        <td>100</td>
        <td>625</td>
        <td>0.9</td>
        <td>89.21%</td>
    </tr>
</table>

### Example

Download [saved model](https://github.com/george-chou/SVHN-Recognition/releases/download/122000/logs.7z)

| Command                                                             |        Sample        | Result |
| :------------------------------------------------------------------ | :------------------: | :----- |
| `python infer.py -c="logs\\model-122000.pth" -i="images\\03.png"`   |  ![](images/03.png)  | 03     |
| `python infer.py -c="logs\\model-122000.pth" -i="images\\457.png"`  | ![](images/457.png)  | 457    |
| `python infer.py -c="logs\\model-122000.pth" -i="images\\2003.png"` | ![](images/2003.png) | 2003   |

### Training curve

![](images/loss.png)

## Environment

* Python 3.6
* torch 1.0
* torchvision 0.2.1
* h5py
* protobuf
* lmdb

## Deploy

1. Clone the source code

    ```
    $ git clone git@github.com:george-chou/SVHN-Recognition.git
    $ cd SVHN-Recognition
    ```

2. Download [SVHN Dataset](http://ufldl.stanford.edu/housenumbers/) Format 1 (train.tar.gz, test.tar.gz)

3. Extract to data folder, now your folder structure should be like below:
    ```
    SVHN-Recognition
        - data
            - test
                - 1.png 
                - 2.png
                - ...
                - digitStruct.mat
            - train
                - 1.png 
                - 2.png
                - ...
                - digitStruct.mat
    ```


## Run

1. Run *convert_to_lmdb.py*

2. Run *train.py*

3. Run *infer.py*