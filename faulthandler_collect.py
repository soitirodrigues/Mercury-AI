"""Diagnóstico: despeja a stack trace onde a coleta do pytest trava."""
import faulthandler
import sys

# Despeja a stack trace após 15s em um arquivo específico e encerra o processo.
_dump_file = open("fh_dump.txt", "w", encoding="utf-8")
faulthandler.dump_traceback_later(15, exit=True, file=_dump_file)

import pytest

sys.exit(pytest.main(["--collect-only", "-vv", "-p", "no:cacheprovider", "-p", "no:cov"]))