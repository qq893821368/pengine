from typing import Callable


class Process:
    @staticmethod
    def none_proc():
        return None

    def __init__(self, sco: str, glb: dict = None):
        self._proc_: Callable = Process.none_proc
        self._sco_: str = sco

        sco_lines = sco.split("\n")
        fco: str = "def ___proc___():\n" + "\n".join([("\t" + line) for line in sco_lines])

        locals().update(glb)
        exec(fco, locals())
        exec("self._proc_ = ___proc___")

    def __call__(self, *args, **kwargs):
        return self._proc_()

    def __str__(self):
        return self._sco_

    def __repr__(self):
        return str(self)

