Street View House Number Recognition

    数据集：http://ufldl.stanford.edu/housenumbers/
    SVHN（Street View House Number）Dateset 来源于谷歌街景门牌号码，本次作业的目标数据集是其中的 Format 1 (Full Numbers: train.tar.gz, test.tar.gz , extra.tar.gz). 其中，train.tar.gz 为训练数据集，test.tar.gz为测试数据集。注：extra.tar.gz是附加数据集，建议不使用。
    在train.tar.gz与test.tar.gz中，分别包含：（1）一些.png格式的图片，每张图片包含一个门牌号；（2）一个digitStruct.mat文件，包含每张图片所对应的门牌号，以及每个门牌号数字的位置信息；（3）一个see_bboxes.m文件，用于辅助Matlab环境下的处理，请忽略之。
    作业要求：
        1. 设计一个网络，用train.tar.gz中的数据进行训练，并用test.tar.gz中的数据进行测试；
        2. 在测试的过程中，不允许使用test.tar.gz/digitStruct.mat文件中的位置信息作为输入，即必须在“忽略测试数据集中给出的位置信息”的前提下，识别出test.tar.gz中每张图片中的门牌号；
        3. 撰写一个PPT，汇报如下信息：
            (1) 所设计的网络的结构和超参数信息；
            (2) 网络的训练方法和优化方法；
            (3) 体现训练过程的“训练曲线”；
            (4) 识别准确率；