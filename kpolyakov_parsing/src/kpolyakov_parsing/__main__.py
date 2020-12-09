# coding=utf-8
# Creation date: 09 дек. 2020
# Creation time: 21:47
# Creator: SteamPeKa
import argparse

from ._acquiring import acquire_batch
from ._input_loading import TaskBatch
from ._input_loading import load_from_txt
from ._output_dumping import dump_to_text


def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-i", "--input-files",
                        nargs="+",
                        type=argparse.FileType("r"),
                        required=True,
                        dest="input_files_list")
    parser.add_argument("-o", "--output-file",
                        type=argparse.FileType("w"),
                        required=True,
                        dest="output_file")
    return vars(parser.parse_args())


def main(input_files_list, output_file, **kwargs):
    if len(kwargs) != 0:
        raise RuntimeError(
            "Unknown input arguments: {}".format(", ".join("{}(={})".format(k, v) for k, v in kwargs.items()))
        )
    batch = TaskBatch()
    for file in input_files_list:
        batch.update(load_from_txt(file=file))
        file.close()
    failed_tasks = acquire_batch(batch)
    result = dump_to_text(batch, failed_tasks)
    output_file.write(result)
    output_file.close()


if __name__ == '__main__':
    main(**get_arguments())
