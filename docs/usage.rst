=====
Usage
=====

To use Simple TimeCode in a project::

    >>> from simpletimecode import TimeCode
    >>> TimeCode(60)
    TimeCode('00:01:00.000')
    >>> TimeCode(120) - 10
    TimeCode('00:01:50.000')
