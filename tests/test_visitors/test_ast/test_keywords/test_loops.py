# -*- coding: utf-8 -*-

import pytest

from wemake_python_styleguide.violations.best_practices import (
    RedundantForElseViolation,
)
from wemake_python_styleguide.visitors.ast.keywords import WrongForElseVisitor

wrong_else_in_for_loop = """
for x in '123':
    ...
else:
    ...
"""

wrong_nested_else_in_for_loop = """
for letters in ['abc', 'zxc', 'rrd']:
    for x in letters:
        ...
    else:
        ...
"""

wrong_nested_for_with_break = """
for letters in ['abc', 'zxc', 'rrd']:
    for x in letters:
        break
else:
    ...
"""

wrong_nested_while_with_break = """
for letters in ['abc', 'zxc', 'rrd']:
    while 'a' in letters:
        break
else:
    ...
"""

wrong_multiple_breaks = """
for x in 'zzz':
    for i in range(10):
        if i > 1:
            break
    else:
        break
else:
    ...
"""

# Correct:

right_else_in_for_loop = """
for x in '123':
    break
else:
    ...
"""

right_multiple_breaks = """
for x in 'xxx':
    for i in range(10):
        if i > 1:
            break
    break
else:
    ...
"""

right_multiple_nested_for_with_break = """
for letters in ['abc', 'zxc', 'rrd']:
    for x in letters:
        break

    for y in letters:
        break

    while letters:
        break
else:
    ...
"""

right_nested_break_in_for_loop = """
for x in 'nnn':
    if x == '1':
        break
else:
    ...
"""

check_nested_if_else = """
for x in '000':
    if x:
        ...
    else:
        ...
"""

while_with_break = """
while x > 2:
    break
"""


@pytest.mark.parametrize('code', [
    wrong_else_in_for_loop,
    wrong_nested_else_in_for_loop,
    wrong_nested_for_with_break,
    wrong_nested_while_with_break,
    wrong_multiple_breaks,
])
def test_wrong_else_in_for_loop(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are raised when else with break statement."""
    tree = parse_ast_tree(code)

    visitor = WrongForElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [RedundantForElseViolation])


@pytest.mark.parametrize('code', [
    right_else_in_for_loop,
    right_nested_break_in_for_loop,
    right_multiple_nested_for_with_break,
    right_multiple_breaks,
    check_nested_if_else,
    while_with_break,
])
def test_correct_else_in_for_loop(
    assert_errors,
    parse_ast_tree,
    code,
    default_options,
):
    """Violations are not raised when else without break statement."""
    tree = parse_ast_tree(code)

    visitor = WrongForElseVisitor(default_options, tree=tree)
    visitor.run()

    assert_errors(visitor, [])
