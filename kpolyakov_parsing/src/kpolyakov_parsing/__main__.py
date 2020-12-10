# coding=utf-8
# Creation date: 09 дек. 2020
# Creation time: 21:47
# Creator: SteamPeKa
import argparse
import enum
import os
import webbrowser

from ._acquiring import acquire_batch
from ._input_loading import TaskBatch
from ._input_loading import load_from_txt
from ._output_dumping import dump_to_text, dump_to_html_text


class OutputFormat(enum.Enum):
    SIMPLE_TEXT = "text"
    HTML = "html"


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
    parser.add_argument("-f", "--output-format",
                        default="html",
                        type=OutputFormat,
                        choices=set(f for f in OutputFormat),
                        dest="output_format")
    parser.add_argument("-b", "--open-in-browser",
                        action="store_true",
                        default=False,
                        dest="open_in_browser")
    return vars(parser.parse_args())


def main(input_files_list, output_file, output_format, open_in_browser, **kwargs):
    if len(kwargs) != 0:
        raise RuntimeError(
            "Unknown input arguments: {}".format(", ".join("{}(={})".format(k, v) for k, v in kwargs.items()))
        )
    batch = TaskBatch()
    for file in input_files_list:
        batch.update(load_from_txt(file=file))
        file.close()
    failed_tasks = acquire_batch(batch)
    if output_format == OutputFormat.HTML:
        result = dump_to_html_text(batch=batch, failed_tasks=failed_tasks)
    elif output_format == OutputFormat.SIMPLE_TEXT:
        result = dump_to_text(batch=batch, failed_tasks=failed_tasks)
    else:
        raise RuntimeError(f"Unimplemented output-format {output_format.value}")
    output_file.write(result)
    output_file.close()
    if open_in_browser:
        webbrowser.open("file://{}".format(os.path.abspath(output_file.name)))


if __name__ == '__main__':
    main(**get_arguments())
