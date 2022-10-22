# Street View House Number Recognition

## 数据集
[Street View House Number](http://ufldl.stanford.edu/housenumbers/SVHN) Dateset 来源于谷歌街景门牌号码

本次任务的目标数据集是其中的 Format 1 (Full Numbers: train.tar.gz, test.tar.gz , extra.tar.gz)

其中，train.tar.gz 为训练数据集，test.tar.gz为测试数据集。注：extra.tar.gz是附加数据集，建议不使用。

在 train.tar.gz 与 test.tar.gz 中，分别包含：<br>
(1) 一些 .png 格式的图片，每张图片包含一个门牌号；<br>
(2) 一个 digitStruct.mat 文件，包含每张图片所对应的门牌号，以及每个门牌号数字的位置信息；<br>
(3) 一个 see_bboxes.m 文件，用于辅助 Matlab 环境下的处理，请忽略之。

## 任务要求
1. 设计一个网络，用 train.tar.gz 中的数据进行训练，并用 test.tar.gz 中的数据进行测试；
2. 在测试的过程中，不允许使用 test.tar.gz/digitStruct.mat 文件中的位置信息作为输入，即必须在“忽略测试数据集中给出的位置信息”的前提下，识别出 test.tar.gz 中每张图片中的门牌号；
3. 撰写一份报告，包含如下信息：<br>
    (1) 所设计的网络的结构和超参数信息；<br>
    (2) 网络的训练方法和优化方法；<br>
    (3) 体现训练过程的“训练曲线”；<br>
    (4) 识别准确率；