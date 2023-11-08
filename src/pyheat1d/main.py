import sys
from pathlib import Path

from pyheat1d.edp import Edo
from pyheat1d.input_files import load_input_file


def main():
    input_file_path = Path(sys.argv[1]).absolute()
    base_dir_path = input_file_path.parent

    input_data = load_input_file(input_file_path)

    edo = Edo(input_data, base_dir_path)

    edo.resolve()


if __name__ == "__main__":
    main()
