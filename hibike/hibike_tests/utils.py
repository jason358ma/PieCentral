"""
General utilities for unit tests.
"""

def run_with_random_data(func, arg_func, kwarg_func=lambda: {}, times=5):
    """
    Test FUNC with random arguments generated by ARG_FUNC and
    KWARG_FUNC, repeating TIMES.

    ARG_FUNC should return an iterable.
    """
    for _ in range(times):
        func(*arg_func(), **kwarg_func())
