# coding=utf-8
# Creation date: 08 дек. 2020
# Creation time: 12:35
# Creator: SteamPeKa

import setuptools

setuptools.setup(
    name="kpolyakov_parsing",
    version="0.1",
    author="SteamPeKa",
    author_email="vladimir.o.balagurov@yandex.ru",
    description="Fills web form and acquires answers from kpolyakov.spb.ru",
    long_description="",
    packages=setuptools.find_packages("src"),
    package_dir={"": "src"},
    test_suite="tests",
    zip_safe=False,
    install_requires=["pytest>=3.0.0"]
)
