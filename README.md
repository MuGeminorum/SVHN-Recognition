# SVHN-Recognition
[![Python application](https://github.com/MuGeminorum/SVHN-Recognition/actions/workflows/python-app.yml/badge.svg?branch=main)](https://github.com/MuGeminorum/SVHN-Recognition/actions/workflows/python-app.yml)
[![license](https://img.shields.io/github/license/MuGeminorum/SVHN-Recognition.svg)](https://github.com/MuGeminorum/SVHN-Recognition/blob/master/LICENSE)
[![](https://img.shields.io/badge/HF-SVHN-ffd21e.svg)](https://huggingface.co/spaces/MuGeminorum/SVHN-Recognition)
[![](https://img.shields.io/badge/ModelScope-SVHN-624aff.svg)](https://www.modelscope.cn/studios/MuGeminorum/SVHN-Recognition)

## Requirements
```bash
conda create -n svhn --yes --file conda.txt
conda activate svhn
pip install -r requirements.txt
```

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

## Usage
0. Clone the source code
```bash
git clone git@github.com:MuGeminorum/SVHN-Recognition.git
cd SVHN-Recognition
```
1. Run *convert_to_lmdb.py*
2. Run *train.py*
3. Run *infer.py*

## Training curve
![loss](https://user-images.githubusercontent.com/20459298/233124972-36c30185-e3dc-48b8-b8a4-bc5767e6b507.png)

## Reference
[1] [Multi-digit Number Recognition from Street View Imagery using Deep Convolutional Neural Networks](http://arxiv.org/pdf/1312.6082.pdf)
