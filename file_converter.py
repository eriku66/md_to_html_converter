import os
import sys
from enum import Enum

import markdown


def exit_and_output_error(message: str) -> None:
    sys.stderr.write(f"Error: {message}\n")
    sys.exit(1)


def check_if_exists_file(*file_paths: str):
    for file_path in file_paths:
        if os.path.isfile(file_path):
            return

        exit_and_output_error(f"Invalid file path: {file_path}")


class FileExtension(Enum):
    MARKDOWN = ".md"
    HTML = ".html"


def check_if_file_extension_match(
    file_name: str, file_extension: FileExtension
) -> None:
    if not str.endswith(file_name, file_extension.value):
        exit_and_output_error(f"File extension does not match: {file_name}")


def convert_md_to_html(args_for_command: list[str]) -> None:
    if len(args_for_command) < 2:
        exit_and_output_error("Argument is missing")

    input_file, output_file = args_for_command

    check_if_exists_file(input_file)

    check_if_file_extension_match(input_file, FileExtension.MARKDOWN)
    check_if_file_extension_match(output_file, FileExtension.HTML)

    with open(input_file, "r", encoding="utf-8") as f:
        md_contents_to_be_converted = f.read()

    with open(output_file, "w", encoding="utf-8") as f:
        f.write(
            markdown.markdown(
                text=md_contents_to_be_converted,
                extensions=["extra", "sane_lists", "nl2br"],
                output_format="html",
            )
        )

    return


def main() -> None:
    args = sys.argv
    match args[1]:
        case "markdown":
            convert_md_to_html(args[2::])
        case _:
            exit_and_output_error("Invalid command")


if __name__ == "__main__":
    main()
