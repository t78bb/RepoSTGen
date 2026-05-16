from tree_sitter import Language, Parser

name = "tree-sitter-structured-text"

# Before running this script, we may need build-essential tools.
Language.build_library(
    f'build/{name}.so', # build result path
    ['.']               # path to the root directory of the language repo
)

# 1. Loading dynamic libraries
st_lang = Language(f'build/{name}.so', 'structured_text')

# 2. Create a parser
parser = Parser()
parser.set_language(st_lang)

def parse(source_code):
    tree = parser.parse(source_code)
    root = tree.root_node

    # Traverse/query syntax tree and print
    def print_node(n, indent=0):
        # print(' '*indent, n.type, n.start_point, n.end_point)
        msg = ' '*indent + f'{n.type} {n.start_point} {n.end_point}\n'
        for c in n.children:
            msg += print_node(c, indent+2)
        return msg

    msg = print_node(root)
    print(msg)
    return msg


# an example
code = b"""
FUNCTION BINOM : DINT
VAR_INPUT
    N : INT;
    K : INT;
END_VAR

VAR
    i : INT;
END_VAR

IF 2 * K > n THEN
	k := n - k;
END_IF;
IF k > n THEN
	RETURN;
ELSIF k = 0 OR k = n THEN
	BINOM := 1;
ELSIF k = 1 THEN
	BINOM := n;
ELSE
	BINOM := n;
	n := n + 1;
	FOR i := 2 TO k DO
		BINOM := BINOM * (n - i) / i;
	END_FOR;
END_IF;
END_FUNCTION
    """.strip()

# 3. Parse source code
parse(code)