# Tree-Sitter-Structured-Text

This is a Tree-Sitter grammar for IEC-61131-3 Structured Text, which is forked from [tree-sitter-structured-text](https://github.com/tmatijevich/tree-sitter-structured-text).

Things changed are:

1. Add support for parsing POU blocks: `FUNCTION`/`FUNCTION_BLOCK`/`TYPE`.
2. Add support for parsing variable declarations blocks: `VAR`/`VAR_INPUT`/`VAR_OUTPUT`/`VAR_IN_OUT`/`VAR_TEMP`/`VAR_LOCAL`.
3. Improve the parsing of variable declarations: Multiple variable declarations of the same type, direct address, etc.
4. Improve the parsing of data type: add the support of size type.
5. Add support for parsing `RETURN`/`EXIT` statement.
6. Provide a build/parse script for python calling. Only support tree-sitter library <= 0.21.0 in python.

