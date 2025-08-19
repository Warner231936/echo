"""Simple Flash (ActionScript) to JavaScript converter.

This module provides a small `FlashConverter` class capable of converting a
subset of ActionScript syntax into JavaScript. The goal is not to be a fully
fledged compiler but to offer a lightweight bridge for legacy Flash snippets.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Union


class FlashConverter:
    """Utility for converting ActionScript code to JavaScript.

    The converter handles a minimal set of transformations that commonly appear
    in small Flash examples. It performs the following operations:

    * ``trace(...)`` calls become ``console.log(...)``.
    * ``var`` declarations are replaced with ``let`` and the ActionScript type
      annotations are removed.
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

        # Replace trace() calls with console.log()
        js = re.sub(r"trace\((.*?)\);", r"console.log(\1);", js)

        # Replace 'var' with 'let'
        js = re.sub(r"\bvar\b", "let", js)

        # Remove type annotations from variable declarations
        js = re.sub(r"\blet\s+([A-Za-z_][\w]*)\s*:\s*[A-Za-z_][\w]*", r"let \1", js)

        # Remove type annotations within parameter lists (e.g. "(x:int, y:String)")
        js = re.sub(
            r"(\(|,)\s*([A-Za-z_][\w]*)\s*:\s*[A-Za-z_][\w]*(\s*=\s*[^,\)]+)?",
            lambda m: f"{m.group(1)}{m.group(2)}{m.group(3) or ''}",
            js,
        )

        # Remove return type annotations in function declarations.
        js = re.sub(
            r"(function\s+[a-zA-Z_][\w]*\s*\([^)]*\))\s*:\s*[A-Za-z_][\w]*",
            r"\1",
            js,
        )

        return js

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
