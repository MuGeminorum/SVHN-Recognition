# SVHN-Recognition
[![Python application](https://github.com/MuGeminorum/SVHN-Recognition/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/MuGeminorum/SVHN-Recognition/actions/workflows/python-app.yml)
[![license](https://img.shields.io/github/license/MuGeminorum/SVHN-Recognition.svg)](https://github.com/MuGeminorum/SVHN-Recognition/blob/master/LICENSE)

A PyTorch implementation of [Multi-digit Number Recognition from Street View Imagery using Deep Convolutional Neural Networks](http://arxiv.org/pdf/1312.6082.pdf)

## Environment
* Python 3.6
* torch 1.0
* torchvision 0.2.1
* h5py
* protobuf
* lmdb

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

## Deploy
1. Clone the source code
    ```
    $ git clone git@github.com:MuGeminorum/SVHN-Recognition.git
    $ cd SVHN-Recognition
    ```
    
2. Download [SVHN Dataset](http://ufldl.stanford.edu/housenumbers) Format 1 (train.tar.gz, test.tar.gz)

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

### Training curve
![loss](https://user-images.githubusercontent.com/20459298/233124972-36c30185-e3dc-48b8-b8a4-bc5767e6b507.png)

### Example
Download [saved model](https://github.com/MuGeminorum/SVHN-Recognition/releases/download/122000/logs.7z) to assigned path and run following commands:
| Command                                                             |                                                     Sample                                                     | Result |
| :------------------------------------------------------------------ | :------------------------------------------------------------------------------------------------------------: | :----- |
| `python infer.py -c="logs\\model-122000.pth" -i="images\\03.png"`   |  ![03](https://user-images.githubusercontent.com/20459298/233124799-5d6d074e-aec1-4a1a-937d-1a031a329b37.png)  | 03     |
| `python infer.py -c="logs\\model-122000.pth" -i="images\\457.png"`  | ![457](https://user-images.githubusercontent.com/20459298/233124853-8ec2d26d-eac7-48b6-84dc-7fdd099b9757.png)  | 457    |
| `python infer.py -c="logs\\model-122000.pth" -i="images\\2003.png"` | ![2003](https://user-images.githubusercontent.com/20459298/233124905-af032c12-f949-4ca7-9132-443f5b3deb59.png) | 2003   |
