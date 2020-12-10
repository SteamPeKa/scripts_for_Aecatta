python setup.py install
rmdir /Q /S build
rmdir /Q /S dist
python -m kpolyakov_parsing -i tests\test_data.txt -o result.html -f html -b
pip uninstall kpolyakov_parsing -y