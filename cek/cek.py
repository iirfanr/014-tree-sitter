import sys
from pathlib import Path
import tree_sitter_python as tspython
from tree_sitter import Language, Parser, Query, QueryCursor

PY = Language(tspython.language())
parser = Parser(PY)

Q_TODO = Query(PY, '((comment) @c (#match? @c "TODO|FIXME"))')
Q_FUNC = Query(PY, "(function_definition name: (identifier) @nama) @fungsi")

def cari_error(node):
    """Return the first ERROR or MISSING node, searching recursively."""
    if node.is_error or node.is_missing:
        return node
    for child in node.children:
        if child.has_error or child.is_error or child.is_missing:
            hasil = cari_error(child)
            if hasil:
                return hasil
    return None

def cek_file(path):
    tree = parser.parse(path.read_bytes())

    # Feature 1: TODO/FIXME comments
    for node in QueryCursor(Q_TODO).captures(tree.root_node).get("c", []):
        print(f"{path}:{node.start_point[0] + 1}: TODO {node.text.decode(errors='replace').strip()}")

    # Feature 2: functions longer than 30 lines
    for _, cap in QueryCursor(Q_FUNC).matches(tree.root_node):
        fn = cap["fungsi"][0]
        nama = cap["nama"][0].text.decode(errors="replace")
        baris = fn.end_point[0] - fn.start_point[0] + 1
        if baris > 30:
            print(f"{path}:{fn.start_point[0] + 1}: fungsi panjang {nama} ({baris} baris)")

    # Feature 3: files whose tree contains an error
    if tree.root_node.has_error:
        err = cari_error(tree.root_node)
        if err:
            print(f"{path}:{err.start_point[0] + 1}: error sintaks ({err.type})")
        else:
            print(f"{path}: error sintaks")

SKIP = {"venv", ".venv", ".git", "node_modules", "__pycache__"}

for path in Path(sys.argv[1]).rglob("*.py"):
    if SKIP & set(path.parts):
        continue
    cek_file(path)