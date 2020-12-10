# coding=utf-8
# Creation date: 09 дек. 2020
# Creation time: 19:32
# Creator: SteamPeKa

import urllib.request

from .._input_loading import TaskBatch


def acquire_single_task(task):
    if not task.has_answer():
        try:
            response = urllib.request.urlopen(f"https://kpolyakov.spb.ru/school/ege/getanswer.php"
                                              f"?egeNo={task.USE_task_key}"
                                              f"&topicNo={task.task_bank_key}")
        except Exception as e:
            return "{}: {}".format(type(e), e)
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
            return "HTTP status code: {}. Message: {}. Content: {}".format(
                response.status_code,
                response.msg,
                answer
            )

        if len(answer) == 0:
            return "API returned empty answer. Probably the task have not been found."

        task.raw_answer = answer
    return None


def acquire_batch(tasks_batch: TaskBatch):
    failed_tasks = {}
    for task in tasks_batch:
        fail_message = acquire_single_task(task)
        if fail_message is not None:
            failed_tasks[task] = fail_message
    return failed_tasks
