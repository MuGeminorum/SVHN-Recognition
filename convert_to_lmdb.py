import os
import glob
import h5py
import lmdb
import shutil
import random
import zipfile
import argparse
import requests
import example_pb2
import numpy as np
from tqdm import tqdm
from PIL import Image
from meta import Meta

parser = argparse.ArgumentParser()
parser.add_argument(
    '-d',
    '--data_dir',
    default='./data',
    help='directory to SVHN (format 1) folders and write the converted files'
)


def download_file(url, save_path, backup_url='https://www.modelscope.cn/api/v1/datasets/MuGeminorum/svhn/repo?Revision=master&FilePath=data.zip'):
    try:
        # 发起 GET 请求下载文件
        response = requests.get(url, stream=True)

        # 检查请求是否成功
        response.raise_for_status()

        # 获取文件大小
        file_size = int(response.headers.get('content-length', 0))

        # 使用 tqdm 显示下载进度条
        with tqdm(total=file_size, unit='B', unit_scale=True, desc='Downloading') as pbar:
            with open(save_path, 'wb') as file:
                for chunk in response.iter_content(chunk_size=1024):
                    if chunk:
                        file.write(chunk)
                        pbar.update(len(chunk))

        print(
            f"File has been successfully downloaded and saved to '{save_path}'."
        )

    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        download_file(backup_url, save_path)


def unzip(zip_file_path, extract_to):
    try:
        # 打开 ZIP 文件
        with zipfile.ZipFile(zip_file_path, 'r') as zip_ref:
            # 获取ZIP文件内的文件数量
            num_files = len(zip_ref.infolist())

            # 使用 tqdm 显示解压缩进度条
            with tqdm(total=num_files, unit='file', desc=f'Extracting {zip_file_path} to {extract_to}...') as pbar:
                # 逐个解压文件
                for member in zip_ref.infolist():
                    zip_ref.extract(member, extract_to)
                    pbar.update(1)

        print(
            f"ZIP file '{zip_file_path}' has been successfully extracted to '{extract_to}'."
        )

    except Exception as e:
        print(f"Error: {e}")


class ExampleReader(object):
    def __init__(self, path_to_image_files):
        self._path_to_image_files = path_to_image_files
        self._num_examples = len(self._path_to_image_files)
        self._example_pointer = 0

    @staticmethod
    def _get_attrs(digit_struct_mat_file, index):
        """
        Returns a dictionary which contains keys: label, left, top, width and height, each key has multiple values.
        """
        attrs = {}
        f = digit_struct_mat_file
        item = f['digitStruct']['bbox'][index].item()
        for key in ['label', 'left', 'top', 'width', 'height']:
            attr = f[item][key]
            values = [f[attr[i].item()][0][0] for i in range(
                len(attr))] if len(attr) > 1 else [attr[0][0]]
            attrs[key] = values

        return attrs

    @staticmethod
    def _preprocess(image, bbox_left, bbox_top, bbox_width, bbox_height):
        cropped_left, cropped_top, cropped_width, cropped_height = (
            int(round(bbox_left - 0.15 * bbox_width)),
            int(round(bbox_top - 0.15 * bbox_height)),
            int(round(bbox_width * 1.3)),
            int(round(bbox_height * 1.3))
        )
        image = image.crop([
            cropped_left,
            cropped_top,
            cropped_left + cropped_width,
            cropped_top + cropped_height
        ])
        image = image.resize([64, 64])
        return image

    def read_and_convert(self, digit_struct_mat_file):
        """
        Read and convert to example, returns None if no data is available.
        """
        if self._example_pointer == self._num_examples:
            return None

        path_to_image_file = self._path_to_image_files[self._example_pointer]
        index = int(path_to_image_file.split('\\')[-1].split('.')[0]) - 1
        self._example_pointer += 1

        attrs = ExampleReader._get_attrs(digit_struct_mat_file, index)
        label_of_digits = attrs['label']
        length = len(label_of_digits)
        if length > 5:
            # skip this example
            return self.read_and_convert(digit_struct_mat_file)

        digits = [10, 10, 10, 10, 10]   # digit 10 represents no digit
        for idx, label_of_digit in enumerate(label_of_digits):
            # label 10 is essentially digit zero
            digits[idx] = int(label_of_digit if label_of_digit != 10 else 0)

        attrs_left, attrs_top, attrs_width, attrs_height = map(lambda x: [int(
            i) for i in x], [attrs['left'], attrs['top'], attrs['width'], attrs['height']])
        min_left, min_top, max_right, max_bottom = (
            min(attrs_left),
            min(attrs_top),
            max(map(lambda x, y: x + y, attrs_left, attrs_width)),
            max(map(lambda x, y: x + y, attrs_top, attrs_height))
        )
        center_x, center_y, max_side = (
            (min_left + max_right) / 2.0,
            (min_top + max_bottom) / 2.0,
            max(max_right - min_left, max_bottom - min_top)
        )
        bbox_left, bbox_top, bbox_width, bbox_height = (
            center_x - max_side / 2.0,
            center_y - max_side / 2.0,
            max_side,
            max_side
        )
        image = np.array(ExampleReader._preprocess(
            Image.open(path_to_image_file),
            bbox_left,
            bbox_top,
            bbox_width,
            bbox_height
        )).tobytes()

        example = example_pb2.Example()
        example.image = image
        example.length = length
        example.digits.extend(digits)
        return example


def convert_to_lmdb(path_to_dataset_dir_and_digit_struct_mat_file_tuples, path_to_lmdb_dirs, choose_writer_callback):
    num_examples = []
    writers = []

    for path_to_lmdb_dir in path_to_lmdb_dirs:
        num_examples.append(0)
        writers.append(lmdb.open(path_to_lmdb_dir, map_size=10*1024*1024*1024))

    for path_to_dataset_dir, path_to_digit_struct_mat_file in path_to_dataset_dir_and_digit_struct_mat_file_tuples:
        path_to_image_files = glob.glob(
            os.path.join(path_to_dataset_dir, '*.png')
        )
        path_to_dataset_dir = path_to_dataset_dir.replace('\\', '/')
        total_files = len(path_to_image_files)

        with h5py.File(path_to_digit_struct_mat_file, 'r') as digit_struct_mat_file:
            example_reader = ExampleReader(path_to_image_files)
            txns = [writer.begin(write=True) for writer in writers]
            for _ in tqdm(range(total_files), desc='%d files found in %s' % (total_files, path_to_dataset_dir)):
                idx = choose_writer_callback(path_to_lmdb_dirs)
                txn = txns[idx]

                example = example_reader.read_and_convert(
                    digit_struct_mat_file
                )
                if example is None:
                    break

                str_id = '{:08}'.format(num_examples[idx] + 1)
                txn.put(str_id.encode(), example.SerializeToString())
                num_examples[idx] += 1

            [txn.commit() for txn in txns]

    for writer in writers:
        writer.close()

    return num_examples


def create_lmdb_meta_file(num_train_examples, num_val_examples, num_test_examples, path_to_lmdb_meta_file):
    print('Saving meta file to %s...' % path_to_lmdb_meta_file)
    meta = Meta()
    meta.num_train_examples = num_train_examples
    meta.num_val_examples = num_val_examples
    meta.num_test_examples = num_test_examples
    meta.save(path_to_lmdb_meta_file)


def main(args):
    path_to_train_dir = os.path.join(args.data_dir, 'train')
    path_to_test_dir = os.path.join(args.data_dir, 'test')
    path_to_train_digit_struct_mat_file = os.path.join(
        path_to_train_dir,
        'digitStruct.mat'
    )
    path_to_test_digit_struct_mat_file = os.path.join(
        path_to_test_dir,
        'digitStruct.mat'
    )

    path_to_train_lmdb_dir = os.path.join(args.data_dir, 'train.lmdb')
    path_to_val_lmdb_dir = os.path.join(args.data_dir, 'val.lmdb')
    path_to_test_lmdb_dir = os.path.join(args.data_dir, 'test.lmdb')
    path_to_lmdb_meta_file = os.path.join(args.data_dir, 'lmdb_meta.json')

    for path_to_dir in [path_to_train_lmdb_dir, path_to_test_lmdb_dir]:
        assert not os.path.exists(
            path_to_dir), 'LMDB directory %s already exists' % path_to_dir

    print('Processing training data...')
    [num_train_examples, num_val_examples] = convert_to_lmdb(
        [(path_to_train_dir, path_to_train_digit_struct_mat_file)],
        [path_to_train_lmdb_dir, path_to_val_lmdb_dir],
        lambda paths: 0 if random.random() > 0.1 else 1
    )
    print('Processing test data...')
    [num_test_examples] = convert_to_lmdb(
        [(path_to_test_dir, path_to_test_digit_struct_mat_file)],
        [path_to_test_lmdb_dir],
        lambda paths: 0
    )

    create_lmdb_meta_file(
        num_train_examples, num_val_examples,
        num_test_examples, path_to_lmdb_meta_file
    )

    print('Done')


if __name__ == '__main__':
    if os.path.exists('./data/train.lmdb'):
        shutil.rmtree('./data/train.lmdb')

    if os.path.exists('./data/val.lmdb'):
        shutil.rmtree('./data/val.lmdb')

    if os.path.exists('./data/test.lmdb'):
        shutil.rmtree('./data/test.lmdb')

    if not os.path.exists('./data.zip'):
        download_file(
            'https://huggingface.co/datasets/MuGeminorum/svhn/resolve/main/data.zip',
            'data.zip'
        )

    if not os.path.exists('./data'):
        unzip('data.zip', './')

    main(parser.parse_args())
