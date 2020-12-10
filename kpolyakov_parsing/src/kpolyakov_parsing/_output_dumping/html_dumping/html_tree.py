# coding=utf-8
# Creation date: 10 дек. 2020
# Creation time: 12:28
# Creator: SteamPeKa

import html
from typing import Dict, List, Any


class HTMLNode(object):
    def __init__(self, tag: str, attributes: Dict[str, Any] = None, text: str = None, tail: str = None):
        if tag is None or not isinstance(tag, str):
            raise ValueError(f"HTML tag have to be a string; {type(tag)}:{tag} found.")
        if html.escape(tag) != tag:
            raise ValueError(f"HTML tag can't contain unsafe symbols. html.escape(\"{tag}\")=\"{html.escape(tag)}\"")
        self.__tag = html.escape(tag)

        self.__attributes = {}
        if attributes is not None:
            if not isinstance(attributes, dict):
                raise ValueError(f"attributes argument have to be dict[str,any]; {type(attributes)} found.")
            for key, value in attributes.items():
                assert not self.has_attribute(key)
                self.add_attribute(key, value)

        self.__text = None
        if text is not None:
            if not isinstance(text, str):
                raise ValueError(f"text argument have to be a string; {type(text)} found.")
            self.__text = str(text)

        self.__tail = None
        if tail is not None:
            if not isinstance(tail, str):
                raise ValueError(f"tail argument have to be a string; {type(tail)} found.")
            self.__tail = str(tail)

        self.__children: List[HTMLNode] = []

    @property
    def tag(self):
        return self.__tag

    def get_tag(self):
        return self.tag

    def has_attribute(self, attribute_name):
        return html.escape(attribute_name) in self.__attributes

    def get_attribute(self, attribute_name, escape=False):
        if escape:
            if self.has_attribute(attribute_name):
                return html.escape(self.__attributes[html.escape(attribute_name)], quote=True)
            else:
                return None
        else:
            return self.__attributes.get(html.escape(attribute_name), None)

    def get_attributes_names(self):
        return set(self.__attributes.keys())

    def add_attribute(self, attribute_name, attribute_value):
        if not isinstance(attribute_name, str):
            raise ValueError(f"Attributes names have to be strings; type(attribute_name) found.")
        if html.escape(attribute_name) != attribute_name:
            raise ValueError(f"HTML node attribute name can't "
                             f"contain unsafe symbols. "
                             f"html.escape(\"{attribute_name}\")=\"{html.escape(attribute_name)}\"")
        attribute_name = html.escape(attribute_name)
        self.__attributes[attribute_name] = str(attribute_value)

    def has_text(self):
        return self.__text is not None or (not self.has_children() and self.has_tail())

    def get_text(self, escape=False):
        if self.has_children():
            if self.__text is None:
                return None
            else:
                if escape:
                    return html.escape(self.__text).replace("\n", "<br/>\n")
                else:
                    return self.__text
        else:
            if self.__text is None and self.__tail is None:
                return None
            else:
                result = []
                if self.__text is not None:
                    if escape:
                        result.append(html.escape(self.__text).replace("\n", "<br/>\n"))
                    else:
                        result.append(self.__text)
                if self.__tail is not None:
                    if escape:
                        result.append(html.escape(self.__tail).replace("\n", "<br/>\n"))
                    else:
                        result.append(self.__tail)
                return "\n".join(result)

    def has_tail(self):
        return self.has_children() and self.__tail is not None

    def get_tail(self, escape=False):
        if self.has_tail():
            if escape:
                return html.escape(self.__tail).replace("\n", "<br/>\n")
            else:
                return self.__tail
        else:
            return None

    def add_child(self, node):
        if not isinstance(node, HTMLNode):
            raise ValueError(f"Child node have to be a HTMLNode instance, {type(node)} found.")
        for sub_node in node.traverse():
            if sub_node == self:
                raise RuntimeError("Cycle is HTML tree is detected.")
        self.__children.append(node)

    def has_children(self):
        return len(self.__children) != 0

    def traverse(self):
        visited_nodes = [self]
        yield self
        for child_node in self.__children:
            for node in child_node.traverse():
                if node not in visited_nodes:
                    visited_nodes.append(node)
                    yield node

    def __attributes_string(self):
        if len(self.__attributes) == 0:
            return ""
        else:
            return " " + (" ".join("{name}=\"{value}\"".format(name=name,
                                                               value=self.get_attribute(name))
                                   for name in self.get_attributes_names()))

    def __has_content(self):
        return self.has_children() or self.has_text()

    def __content(self):
        if self.__has_content():
            if self.has_children():
                lines = [""]
                if self.has_text():
                    lines.extend(self.get_text(escape=True).split("\n"))
                for child in self.__children:
                    lines.extend(child.to_string().split("\n"))
                if self.has_tail():
                    lines.extend(self.get_tail(escape=True).split("\n"))
                return "\n    ".join(lines) + "\n"
            else:
                # Has content but not children == has only text
                return ("\n" + (" " * len(self.__node_opener()))).join(
                    self.get_text(escape=True).split("\n")
                )
        else:
            return ""

    def __node_opener(self):
        if self.__has_content():
            return "<{tag}{attrs}>".format(tag=self.tag,
                                           attrs=self.__attributes_string())
        else:
            return "<{tag}{attrs}/>".format(tag=self.tag,
                                            attrs=self.__attributes_string())

    def __node_closer(self):
        if self.__has_content():
            return "</{tag}>".format(tag=self.__tag)
        else:
            return ""

    def to_string(self) -> str:
        result = "{opener}{content}{closer}".format(
            opener=self.__node_opener(),
            closer=self.__node_closer(),
            content=self.__content()
        )
        return result


class HTMLTree(HTMLNode):
    def __init__(self, title=None, charset="utf-8"):
        super().__init__(tag="html")
        self.__head = HTMLNode(tag="head", text=None)
        self.add_child(self.__head)
        self.__head.add_child(HTMLNode(tag="meta",
                                       attributes={"charset": charset}))
        if title is not None:
            self.__head.add_child(HTMLNode(tag="title",
                                           text=title))
        self.__body = HTMLNode(tag="body")
        self.add_child(self.__body)

    def to_string(self) -> str:
        parent_result = super(HTMLTree, self).to_string()
        return "<!DOCTYPE html>\n" + parent_result

    @property
    def head(self):
        return self.__head

    @property
    def body(self):
        return self.__body


class Script(HTMLNode):
    def __init__(self, script, attributes=None):
        super().__init__(tag="script",
                         attributes=attributes,
                         text=script)

    def get_text(self, *args, **kwargs):
        return super(Script, self).get_text(escape=False)

    def get_tail(self, *args, **kwargs):
        return super(Script, self).get_tail(escape=False)
