import random
from pathlib import Path

from idna import unicode
from sklearn.model_selection import train_test_split

import typer


def split(input_path: Path, output_path_train: Path, output_path_dev: Path):
    train_data = []
    with open(input_path, encoding='utf-8', mode='r') as input_file:
        lines = input_file.readlines()
        for line in lines:
            train_data.append(line.replace("\n", ""))

    random.shuffle(train_data)
    train, test = train_test_split(train_data, test_size=0.2)

    with open(output_path_train, encoding='utf-8', mode='w') as output_file:
        for el in train:
            output_file.write(unicode(el) + '\n')

    with open(output_path_dev, encoding='utf-8', mode='w') as output_file:
        for el in test:
            output_file.write(unicode(el) + '\n')


if __name__ == "__main__":
    typer.run(split)
