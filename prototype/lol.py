import argparse
import json
import os
import time
from typing import List

from lol_lexer_types import Token
from lol_parser_token_stream import TokenStream
from lol_parser_types import ASTNode


def run_lexer(text: str) -> List[Token]:
    from lol_lexer import tokenize

    return tokenize(text)


def run_parser(stream: TokenStream) -> List[ASTNode]:
    from lol_parser import parse

    return parse(stream)


def run_analyzer() -> str:
    pass


def run_emitter() -> str:
    pass


def main() -> None:
    parser = argparse.ArgumentParser()
    # TODO(dchu): make this accept multiple file names or folders. Also accept
    # a full configuration file.
    parser.add_argument(
        "-i", "--input", type=str, required=True, help="Input file name"
    )
    parser.add_argument(
        "-o", "--output", type=str, default=None, help="Output directory name"
    )
    args = parser.parse_args()

    # I explicitly extract the names because otherwise one may be tempted to
    # pass the 'args' namespace, which is always confusing.
    input_file = args.input
    output_dir = args.output

    # Assume input_file is not None because it is required
    with open(input_file) as f:
        text = f.read()
    # Make empty output dir if it doesn't exist
    if not os.path.exists(output_dir):
        os.mkdir(output_dir)

    # Get timestamp to prepend to all output files
    timestamp = time.time()

    tokens = run_lexer(text=text)
    with open(os.path.join(output_dir, f"{timestamp}-lexer.out"), "w") as f:
        json.dump({"lexer": [token.to_dict() for token in tokens]}, f, indent=4)

    stream = TokenStream(tokens, text=text)
    asts = run_parser(stream)
    with open(os.path.join(output_dir, f"{timestamp}-parser.out"), "w") as f:
        json.dump({"parser": [ast.to_dict() for ast in asts]}, f, indent=4)


if __name__ == "__main__":
    main()