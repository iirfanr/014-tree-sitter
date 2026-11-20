# cek.py: Python code checker (tree-sitter)

A small CLI that scans a folder of Python files and reports three things:

1. **TODO / FIXME comments**, with file and line number
2. **Functions longer than 30 lines**, with name and line count
3. **Files with syntax errors**, with the first problem line

It parses each file with tree-sitter instead of searching the raw text, so a
`TODO` inside a string is not reported, only real comments.

## Installation

Requires Python 3.10 or newer.

```bash
pip install tree-sitter tree-sitter-python
```

## Usage

```bash
python cek.py <folder>
```

Example:

```bash
python cek.py uji/
```

The folders `venv`, `.venv`, `.git`, `node_modules` and `__pycache__` are skipped.

## Example output

```
uji\ada_todo.py:1: TODO # TODO: tambah validasi
uji\ada_todo.py:3: TODO # FIXME: pakai f-string
uji\panjang.py:1: fungsi panjang panjang (36 baris)
uji\rusak.py:1: error sintaks (ERROR)
```

Format: `path:line: message`

## Notes

- All functions are counted, including methods inside classes and nested
  functions, so one long method can appear next to its class.
- The "error" report uses `root_node.has_error`, then searches the tree for the
  first `ERROR` or `MISSING` node to give the line number. A file with several
  errors only reports the first.
- Checked on a real repository: [repo name and link], with 2 random files
  compared by hand against the output.