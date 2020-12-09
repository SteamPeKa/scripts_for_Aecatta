# coding=utf-8
# Creation date: 09 дек. 2020
# Creation time: 21:40
# Creator: SteamPeKa
from typing import Dict

from .._input_loading import TaskBatch, SimpleTask, OutputType


def dump_to_text(batch: TaskBatch, failed_tasks: Dict[SimpleTask, str]):
    answers = ["Answers:"]
    fails = ["Failed tasks:"]
    parts = [answers, fails]

    for task in batch:
        if task.has_answer():
            answers.append("USE task: {}, task bank number {} answer:\n"
                           "\"\"\"\n"
                           "{}\n"
                           "\"\"\"".format(
                task.USE_task_key,
                task.task_bank_key,
                task.get_answer(output_type=OutputType.TXT)
            ))
        else:
            assert task in failed_tasks
            fails.append("USE task: {}, task bank number {} failed!\n"
                         "Reason: {}\n".format(task.USE_task_key,
                                               task.task_bank_key,
                                               failed_tasks[task]))
    return "\n\n".join("\n".join(sub_parts) for sub_parts in parts)
