import tree_sitter_python as tspython
from tree_sitter import Language, Parser

parser = Parser(Language(tspython.language()))

potongan = {
    "fungsi": b'def sapa(nama):\n    return "Halo  + nama\n',
    "if_else": b'x = 5\nif x > 3:\n    print("besar")\nelse:\n    print("kecil")\n',
    "kelas": b'class Mahasiswa:\n    def perkenalan(self):\n        return "Saya mahasiswa"\n',
}

for nama, kode in potongan.items():
    tree = parser.parse(kode)
    print("==", nama, "==")
    print(tree.root_node)
    for c in tree.root_node.children[0].children:
        print(c.type, "bernama" if c.is_named else "anonim")
    print()

