import argparse
import constants
from extract import extract_text
from batch import create_batches
from grammar_checker import GrammarChecker
from highlight import highlight_text
from models import WordError


def process_file(filename: str, grammar_checker: GrammarChecker):
    quoted_texts, line_positions = extract_text(filename)
    batches = create_batches(quoted_texts, line_positions)

    print(f"Обработка файла: {filename}")

    for batch_num, (batch_texts, batch_lines) in enumerate(batches, start=1):
        batch_text = "\n".join(batch_texts)
        errors = grammar_checker.check_text(batch_text, lang="ru", options=0)

        if not errors:
            print(f"Батч {batch_num}: ошибок не найдено.")
            continue

        for error in errors:
            err: WordError = error
            if 1 <= err.row <= len(batch_texts):
                original_text = batch_texts[err.row]
                original_line = batch_lines[err.row]
                highlighted = highlight_text(
                    original_text, err.col, err.length, "red")
                print(highlighted)
                print(
                    f"Ошибка в слове '{err.word}' на строке {original_line}.")
                if err.s:
                    fix_options = ", ".join(err.s)
                    highlighted_fixes = highlight_text(
                        fix_options, 0, len(fix_options), "green")
                    print(f"Варианты исправления: {highlighted_fixes}")
                print()
            else:
                print(f"Некорректный номер строки в ошибке: row={err.row}")


def main():
    parser = argparse.ArgumentParser(description="Grammar Checker Action")
    parser.add_argument(
        "files",
        metavar="FILE",
        type=str,
        nargs="+",
        help='Файлы для проверки орфографии'
    )
    args = parser.parse_args()

    grammar_checker = GrammarChecker(api_url=constants.API_URL)

    for filename in args.files:
        process_file(filename, grammar_checker)


if __name__ == "__main__":
    main()
