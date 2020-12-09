# coding=utf-8
# Creation date: 09 дек. 2020
# Creation time: 19:45
# Creator: SteamPeKa
# noinspection PyProtectedMember
import kpolyakov_parsing._acquiring
import kpolyakov_parsing._input_loading


class TestAcquireBatch(object):
    def test_acquire_empty_batch(self):
        empty_batch = kpolyakov_parsing._input_loading.TaskBatch()
        buster = kpolyakov_parsing._acquiring.acquire_batch(empty_batch)
        assert len(buster) == 0

    def test_acquire_single_task(self):
        right_answers = {
            kpolyakov_parsing._input_loading.SimpleTask(1, 1): "4"
        }
        errors = {}
        batch = kpolyakov_parsing._input_loading.TaskBatch()
        batch.update(errors.keys())
        batch.update(right_answers.keys())
        assert len(batch) == 1

        failed_tasks = kpolyakov_parsing._acquiring.acquire_batch(batch)
        for task in batch:
            if task.has_answer():
                assert task in right_answers
                assert task.raw_answer == right_answers[task]
            else:
                assert task in errors
                assert task in failed_tasks
                assert errors[task] == failed_tasks[task]

    def test_not_existing_task(self):
        right_answers = {}
        errors = {
            kpolyakov_parsing._input_loading.SimpleTask(25, 200):
                "API returned empty answer. Probably the task have not been found."
        }
        batch = kpolyakov_parsing._input_loading.TaskBatch()
        batch.update(errors.keys())
        batch.update(right_answers.keys())
        assert len(batch) == 1

        failed_tasks = kpolyakov_parsing._acquiring.acquire_batch(batch)
        for task in batch:
            if task.has_answer():
                assert task in right_answers
                assert task.raw_answer == right_answers[task]
            else:
                assert task in errors
                assert task in failed_tasks
                assert errors[task] == failed_tasks[task]
