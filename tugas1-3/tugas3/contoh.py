import os
from pathlib import Path

from sklearn import tree
from tree_sitter import Query, QueryCursor

from tugas3.q import PY

def sapa(nama):
    return "Halo " + nama

class Mahasiswa:
    def perkenalan(self):
        return "Saya mahasiswa"

x = 5
if x > 3:
    print(sapa("Budi"))
    print(Mahasiswa().perkenalan())
else:
    print("kecil")