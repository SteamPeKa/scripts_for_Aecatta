# coding=utf-8
# Creation date: 10 дек. 2020
# Creation time: 13:44
# Creator: SteamPeKa
from typing import Dict

from .html_tree import HTMLNode, HTMLTree, Script
from ..._input_loading import TaskBatch, SimpleTask, OutputType


def prepare_node_for_answer(use_task_id, tasks_bank_task_id, answer, error_message):
    assert answer is None or error_message is None
    element_id = f"USE-{use_task_id}-task-{tasks_bank_task_id}"
    elem_class = "answer" if answer is not None else "error"
    text = answer if answer is not None else error_message
    result = HTMLNode(tag="div",
                      attributes={"class": f"task-{elem_class}"})
    result.add_child(HTMLNode(tag="a",
                              attributes={"href": f"#{element_id}",
                                          "onclick": f"view('{element_id}'); return false",
                                          "class": f"clickable-{elem_class}-view"},
                              text=f"Answer for task {tasks_bank_task_id} from tasks collection"))
    result.add_child(HTMLNode(tag="div",
                              attributes={"id": element_id,
                                          "style": "display: none;",
                                          "class": f"hidden-{elem_class}-content"},
                              text=text))
    return result


view_script = ("function view(n) {\n"
               "    style = document.getElementById(n).style;\n"
               "    style.display = (style.display == 'block') ? 'none' : 'block';\n"
               "}")


def dump_to_html_tree(batch: TaskBatch, failed_tasks: Dict[SimpleTask, str]) -> HTMLNode:
    tree = HTMLTree(title="USE tasks results from kpolyakov tasks collection",
                    charset="utf-8")
    tree.head.add_child(Script(view_script))
    tree.body.add_child(HTMLNode(tag="h1",
                                 attributes={"class": "page-header"},
                                 text="Results"))
    answers_node = HTMLNode(tag="div",
                            attributes={"class": "answers"})
    tree.body.add_child(answers_node)
    answers_node.add_child(HTMLNode(tag="h2",
                                    attributes={"class": "answers-header"},
                                    text="Answers for USE tasks from kpolyakov tasks collection"))
    answers_content_node = HTMLNode(tag="div",
                                    attributes={"class": "answers-content"})
    answers_node.add_child(answers_content_node)

    errors_node = HTMLNode(tag="div",
                           attributes={"class": "errors"})
    errors_node.add_child(HTMLNode(tag="h2",
                                   attributes={"class": "errors-header"},
                                   text="Unsuccessful downloads"))
    errors_content_node = HTMLNode(tag="div",
                                   attributes={"class": "errors-content"})
    errors_node.add_child(errors_content_node)
    tree.body.add_child(errors_node)

    current_USE_task_id_ans = None
    current_answers_for_USE_node = None
    current_USE_task_id_err = None
    current_errors_for_USE_node = None
    for task in batch:
        if task.has_answer():
            assert task not in failed_tasks
            if current_USE_task_id_ans != task.USE_task_key:
                current_USE_task_id_ans = task.USE_task_key
                current_answers_for_USE_node = HTMLNode(tag="div",
                                                        attributes={"class": "answers-for-use-task"})
                answers_content_node.add_child(current_answers_for_USE_node)
                current_answers_for_USE_node.add_child(
                    HTMLNode(tag="h3",
                             attributes={"class": "single-use-answers-header"},
                             text=f"Answers for examples for USE task {current_USE_task_id_ans}")
                )
            current_answers_for_USE_node.add_child(prepare_node_for_answer(task.USE_task_key,
                                                                           task.task_bank_key,
                                                                           task.get_answer(output_type=OutputType.TXT),
                                                                           None))
        else:
            assert task in failed_tasks
            if current_USE_task_id_err != task.USE_task_key:
                current_USE_task_id_err = task.USE_task_key
                current_errors_for_USE_node = HTMLNode(tag="div",
                                                       attributes={"class": "errors-for-use-task"})
                errors_content_node.add_child(current_errors_for_USE_node)
                current_errors_for_USE_node.add_child(
                    HTMLNode(tag="h3",
                             attributes={"class": "single-use-errors-header"},
                             text=f"Errors encountered for examples for USE task {current_USE_task_id_err}"))
            current_errors_for_USE_node.add_child(prepare_node_for_answer(task.USE_task_key,
                                                                          task.task_bank_key,
                                                                          None,
                                                                          failed_tasks[task]))

    return tree


def dump_to_html_text(batch: TaskBatch, failed_tasks: Dict[SimpleTask, str]) -> str:
    return dump_to_html_tree(batch=batch,
                             failed_tasks=failed_tasks).to_string()
