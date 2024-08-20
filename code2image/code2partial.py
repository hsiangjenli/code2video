import os
import argparse

args = argparse.ArgumentParser()

args.add_argument("--code_path", default="code2image/code2img.py")
args.add_argument("--output_dir", default="partial_code")

def open_file(file_path: str) -> str:
    """

    Open a file and return the content.

    Args:
        file_path (str): The file path of the file.

    Returns:
        str: The content of the file.
    """
    return open(file_path, "r").read()

def create_partial_code_files(code_path: str, output_dir="partial_code"):
    """
    
    Create partial code files.

    Args:
        code (str): The file path of the code which will be split into partial code files.
        output_dir (str, optional): The output directory of the partial code files. Defaults to "partial_code".
    """
    code = open_file(code_path)

    os.makedirs(output_dir, exist_ok=True)
    partial_code = ""
    for i, char in enumerate(code):
        partial_code += char
        file_path = os.path.join(output_dir, f"code_{i:06d}.py")
        with open(file_path, "w") as file:
            file.write(partial_code)

if __name__ == "__main__":
    
    args = args.parse_args()
    create_partial_code_files(code_path=args.code_path, output_dir=args.output_dir)