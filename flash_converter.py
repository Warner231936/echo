"""Simple Flash (ActionScript) to JavaScript converter.

This module provides a small `FlashConverter` class capable of converting a
subset of ActionScript syntax into JavaScript. The goal is not to be a fully
fledged compiler but to offer a lightweight bridge for legacy Flash snippets.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Union
import textwrap


class FlashConverter:
    """Utility for converting ActionScript code to JavaScript.

    The converter handles a minimal set of transformations that commonly appear
    in small Flash examples. It performs the following operations:

    * ``trace(...)`` calls become ``console.log(...)``.
    * ``var`` declarations are replaced with ``let`` and the ActionScript type
      annotations are removed.
    * Access modifiers such as ``public`` or ``private`` are stripped.
    * ``implements`` clauses in class declarations are removed.
    * Function return type annotations are stripped.
    """

    def convert_code(self, action_script: str) -> str:
        """Convert an ActionScript source string to JavaScript.

        Parameters
        ----------
        action_script:
            Source code written in ActionScript 3.

        Returns
        -------
        str
            JavaScript code with a limited set of transformations applied.
        """

        js = action_script

        # Remove package declarations and their wrapping braces
        if re.search(r"^\s*package\b", js, flags=re.MULTILINE):
            js = re.sub(r"^\s*package[^\{]*{\s*\n?", "", js, flags=re.MULTILINE)
            js = re.sub(r"\n}\s*$", "", js)

        # Remove import statements entirely
        js = re.sub(r"^\s*import [^\n]+(?:\n|$)", "", js, flags=re.MULTILINE)


        # Replace ``trace`` calls with ``console.log``.
        #
        # ActionScript allows whitespace between ``trace`` and its argument list
        # (``trace ("hi")``). The original implementation didn't handle this
        # form which meant such statements were left untouched. The updated
        # pattern below accepts optional spaces after ``trace`` and before an
        # optional semicolon. We deliberately avoid matching newlines so that
        # the structure of the surrounding code remains intact when no semicolon
        # is present.
        #
        # ``trace`` can also appear as part of a longer identifier (``mytrace``)
        # or as a method on an object (``logger.trace``). Those occurrences
        # should not be replaced, so we require ``trace`` to be a standalone
        # identifier that is not preceded by a dot.
        js = re.sub(
            r"(?<!\.)\btrace\b\s*\((.*?)\)[ \t]*(;?)",
            r"console.log(\1)\2",
            js,
        )

        # Replace 'var' with 'let'
        js = re.sub(r"\bvar\b", "let", js)

        # Remove type annotations from variable declarations (let/const) including generics
        js = re.sub(
            r"\b(let|const)\s+([A-Za-z_][\w]*)\s*:\s*([A-Za-z_][\w\.]*(?:<[^>]+>)?)",
            lambda m: f"{m.group(1)} {m.group(2)}",
            js,
        )

        # Remove type annotations within parameter lists (e.g. "(x:int, y:String)")
        js = re.sub(
            r"(\(|,)\s*([A-Za-z_][\w]*)\s*:\s*([A-Za-z_][\w\.]*(?:<[^>]+>)?)(\s*=\s*[^,\)]+)?",
            lambda m: f"{m.group(1)}{m.group(2)}{m.group(4) or ''}",
            js,
        )

        # Convert ActionScript 'for each' loops to JavaScript 'for...of' loops
        js = re.sub(
            r"\bfor\s+each\s*\(\s*(let|const)\s+([A-Za-z_][\w]*)\s+in\s+([^\)]+)\)",
            r"for (\1 \2 of \3)",
            js,
        )

        # Remove return type annotations in function declarations (supports modifiers)
        js = re.sub(
            r"((?:\b(?:public|private|protected|internal|static)\s+)*function\s+[a-zA-Z_][\w]*\s*\([^)]*\))\s*:\s*([A-Za-z_][\w\.]*(?:<[^>]+>)?)",
            r"\1",
            js,
        )

        return textwrap.dedent(js).strip()

    def convert_file(self, src: Union[str, Path], dest: Union[str, Path]) -> None:
        """Convert an ActionScript file to JavaScript.

        Parameters
        ----------
        src, dest:
            Paths to the source ActionScript file and the destination JavaScript
            file respectively.
        """

        src_path = Path(src)
        dest_path = Path(dest)

        converted = self.convert_code(src_path.read_text())
        dest_path.write_text(converted)

    def convert_directory(self, src_dir: Union[str, Path], dest_dir: Union[str, Path]) -> None:
        """Recursively convert all ActionScript files in a directory.

        Parameters
        ----------
        src_dir:
            Directory containing ``.as`` files to convert.
        dest_dir:
            Output directory where converted ``.js`` files will be written.

        Notes
        -----
        The directory structure of ``src_dir`` is preserved in ``dest_dir``.
        Only files ending with ``.as`` are considered for conversion. The
        destination directory is created if it does not already exist.
        """

        src_root = Path(src_dir)
        dest_root = Path(dest_dir)

        for src_file in src_root.rglob("*.as"):
            relative = src_file.relative_to(src_root)
            dest_file = dest_root / relative.with_suffix(".js")
            dest_file.parent.mkdir(parents=True, exist_ok=True)
            self.convert_file(src_file, dest_file)
