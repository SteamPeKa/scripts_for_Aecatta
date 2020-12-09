# coding=utf-8
# Creation date: 09 дек. 2020
# Creation time: 19:32
# Creator: SteamPeKa

import urllib.request

from .._input_loading import TaskBatch


def acquire_batch(tasks_batch: TaskBatch):
    failed_tasks = {}
    for task in tasks_batch:
        if not task.has_answer():
            try:
                response = urllib.request.urlopen(
                    "https://kpolyakov.spb.ru/school/ege/getanswer.php?egeNo={task.USE_task_key}&topicNo={task.task_bank_key}".format(
                        task=task
                    ))
            except Exception as e:
                assert task not in failed_tasks
                failed_tasks[task] = "{}: {}".format(type(e), e)
                continue
            content_type_spec = response.getheader("Content-Type")
            parts = [part.strip().split("=", 1) for part in content_type_spec.split(";")]
            charset = "utf-8"
            for part in parts:
                if len(part) == 2:
                    key, value = part
                    if key == "charset":
                        charset = value
            answer = response.read().decode(charset)
            response.close()
            if response.getcode() != 200:
                assert task not in failed_tasks
                failed_tasks[task] = "HTTP status code: {}. Message: {}. Content: {}".format(
                    response.status_code,
                    response.msg,
                    answer
                )
                continue
            if len(answer) == 0:
                assert task not in failed_tasks
                failed_tasks[task] = "API returned empty answer. Probably the task have not been found."
                continue
            task.raw_answer = answer
    return failed_tasks
