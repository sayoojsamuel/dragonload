#!/usr/bin/env python3

# https://opensource.com/article/17/5/4-practical-python-libraries
from prompt_toolkit import prompt
from prompt_toolkit.history import FileHistory
from prompt_toolkit.auto_suggest import AutoSuggestFromHistory
from prompt_toolkit.contrib.completers import WordCompleter

SQLCompleter = WordCompleter(['select', 'from', 'insert', 'update', 'delete', 'drop'],
                             ignore_case=True)

while 1:
    user_input = prompt('SQL>',
                        history=FileHistory('history.txt'),
                        auto_suggest=AutoSuggestFromHistory(),
                        completer=SQLCompleter,
                        )
    print(user_input)
