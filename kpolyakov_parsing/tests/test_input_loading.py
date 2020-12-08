# coding=utf-8
# Creation date: 08 дек. 2020
# Creation time: 13:07
# Creator: SteamPeKa

import os

# noinspection PyProtectedMember
import kpolyakov_parsing._input_loading


class TestSimpleTask(object):
    def test_create_case_1(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)

    def test_create_case_2(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask("3", "4")

    def test_create_case_3(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask("B5", "6")

    def test_create_case_4(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask("B7", "TASK8")

    def test_create_case_5(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask(object(), object())

    def test_fields_case_1(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert isinstance(buster.USE_task_key, int)
        assert buster.USE_task_key == 1
        assert isinstance(buster.task_bank_key, int)
        assert buster.task_bank_key == 2

    def test_fields_case_2(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask("3", "4")
        assert isinstance(buster.USE_task_key, int)
        assert buster.USE_task_key == 3
        assert isinstance(buster.task_bank_key, int)
        assert buster.task_bank_key == 4

    def test_fields_case_3(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask("B5", "6")
        assert isinstance(buster.USE_task_key, str)
        assert buster.USE_task_key == "B5"
        assert isinstance(buster.task_bank_key, int)
        assert buster.task_bank_key == 6

    def test_fields_case_4(self):
        buster = kpolyakov_parsing._input_loading.SimpleTask("B7", "TASK8")
        assert isinstance(buster.USE_task_key, str)
        assert buster.USE_task_key == "B7"
        assert isinstance(buster.task_bank_key, str)
        assert buster.task_bank_key == "TASK8"

    def test_fields_case_5(self):
        USE_key = object()
        task_key = object()
        buster = kpolyakov_parsing._input_loading.SimpleTask(USE_key, task_key)
        assert isinstance(buster.USE_task_key, str)
        assert buster.USE_task_key == str(USE_key)
        assert isinstance(buster.task_bank_key, str)
        assert buster.task_bank_key == str(task_key)

    def test_hash_case_1(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert hash(buster) == hash(tester)

    def test_hash_case_2(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask("1", 2)
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert hash(buster) == hash(tester)

    def test_hash_case_3(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask(1, "2")
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert hash(buster) == hash(tester)

    def test_hash_case_4(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask("1", "2")
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert hash(buster) == hash(tester)

    def test_eq_case_1(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert buster == tester
        assert tester == buster
        buster = kpolyakov_parsing._input_loading.SimpleTask(3, 4)
        assert buster != tester
        assert tester != buster

    def test_eq_case_2(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask("1", 2)
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert buster == tester
        assert tester == buster
        buster = kpolyakov_parsing._input_loading.SimpleTask("3", 4)
        assert buster != tester
        assert tester != buster

    def test_eq_case_3(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask(1, "2")
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert buster == tester
        assert tester == buster
        buster = kpolyakov_parsing._input_loading.SimpleTask(3, "4")
        assert buster != tester
        assert tester != buster

    def test_hash_case_5(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask("1", "2")
        buster = kpolyakov_parsing._input_loading.SimpleTask(1, 2)
        assert buster == tester
        assert tester == buster
        buster = kpolyakov_parsing._input_loading.SimpleTask("3", "4")
        assert buster != tester
        assert tester != buster

    def test_cmp_case_1(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask(5, 5)

        buster = kpolyakov_parsing._input_loading.SimpleTask(4, 5)  # Leser
        assert (buster < tester) is True
        assert (tester < buster) is False
        assert (buster <= tester) is True
        assert (tester <= buster) is False
        assert (buster > tester) is False
        assert (tester > buster) is True
        assert (buster >= tester) is False
        assert (tester >= buster) is True

        buster = kpolyakov_parsing._input_loading.SimpleTask("5", 5)  # Equal
        assert (buster < tester) is False
        assert (tester < buster) is False
        assert (buster <= tester) is True
        assert (tester <= buster) is True
        assert (buster > tester) is False
        assert (tester > buster) is False
        assert (buster >= tester) is True
        assert (tester >= buster) is True

        buster = kpolyakov_parsing._input_loading.SimpleTask(6, 5)  # Greater
        assert (buster < tester) is False
        assert (tester < buster) is True
        assert (buster <= tester) is False
        assert (tester <= buster) is True
        assert (buster > tester) is True
        assert (tester > buster) is False
        assert (buster >= tester) is True
        assert (tester >= buster) is False

    def test_cmp_case_2(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask(5, 5)

        buster = kpolyakov_parsing._input_loading.SimpleTask(5, 4)  # Leser
        assert (buster < tester) is True
        assert (tester < buster) is False
        assert (buster <= tester) is True
        assert (tester <= buster) is False
        assert (buster > tester) is False
        assert (tester > buster) is True
        assert (buster >= tester) is False
        assert (tester >= buster) is True

        buster = kpolyakov_parsing._input_loading.SimpleTask(5, "5")  # Equal
        assert (buster < tester) is False
        assert (tester < buster) is False
        assert (buster <= tester) is True
        assert (tester <= buster) is True
        assert (buster > tester) is False
        assert (tester > buster) is False
        assert (buster >= tester) is True
        assert (tester >= buster) is True

        buster = kpolyakov_parsing._input_loading.SimpleTask(5, 6)  # Greater
        assert (buster < tester) is False
        assert (tester < buster) is True
        assert (buster <= tester) is False
        assert (tester <= buster) is True
        assert (buster > tester) is True
        assert (tester > buster) is False
        assert (buster >= tester) is True
        assert (tester >= buster) is False

    def test_cmp_case_3(self):
        tester = kpolyakov_parsing._input_loading.SimpleTask(5, 5)

        buster = kpolyakov_parsing._input_loading.SimpleTask(4, 4)  # Leser
        assert (buster < tester) is True
        assert (tester < buster) is False
        assert (buster <= tester) is True
        assert (tester <= buster) is False
        assert (buster > tester) is False
        assert (tester > buster) is True
        assert (buster >= tester) is False
        assert (tester >= buster) is True

        buster = kpolyakov_parsing._input_loading.SimpleTask("5", "5")  # Equal
        assert (buster < tester) is False
        assert (tester < buster) is False
        assert (buster <= tester) is True
        assert (tester <= buster) is True
        assert (buster > tester) is False
        assert (tester > buster) is False
        assert (buster >= tester) is True
        assert (tester >= buster) is True

        buster = kpolyakov_parsing._input_loading.SimpleTask(6, 6)  # Greater
        assert (buster < tester) is False
        assert (tester < buster) is True
        assert (buster <= tester) is False
        assert (tester <= buster) is True
        assert (buster > tester) is True
        assert (tester > buster) is False
        assert (buster >= tester) is True
        assert (tester >= buster) is False


class TestTaskBatch(object):
    # TODO Написать тесты для батчей
    pass


class TestLoadFromTxt(object):
    def test_load_from_path(self):
        path = os.path.join("tests", "test_data.txt")
        tester = {
            (25, 7), (25, 11), (25, 28), (25, 31), (25, 50), (25, 67),
            (11, 6), (11, 10), (11, 81), (11, 25), (11, 61), (11, 13), (11, 79),
        }
        buster = set()

        for simple_task in kpolyakov_parsing._input_loading.load_from_txt(path=path):
            buster.add((simple_task.USE_task_key, simple_task.task_bank_key))
        assert len(tester ^ buster) == 0, "{{{}}} != {{{}}}. Symmetrical difference: {{{}}}".format(
            ", ".join(str(a) for a in tester),
            ", ".join(str(a) for a in buster),
            ", ".join(str(a) for a in (tester ^ buster))
        )

    def test_load_from_file(self):
        path = os.path.join("tests", "test_data.txt")
        tester = {
            (25, 7), (25, 11), (25, 28), (25, 31), (25, 50), (25, 67),
            (11, 6), (11, 10), (11, 81), (11, 25), (11, 61), (11, 13), (11, 79),
        }
        buster = set()
        with open(path, "r") as f:
            for simple_task in kpolyakov_parsing._input_loading.load_from_txt(file=f):
                buster.add((simple_task.USE_task_key, simple_task.task_bank_key))
        assert len(tester ^ buster) == 0, "{{{}}} != {{{}}}. Symmetrical difference: {{{}}}".format(
            ", ".join(str(a) for a in tester),
            ", ".join(str(a) for a in buster),
            ", ".join(str(a) for a in (tester ^ buster))
        )
