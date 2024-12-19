import re
from typing import List, Tuple


def extract_text(filename: str) -> Tuple[List[str], List[int]]:
    quoted_texts = []
    line_positions = []
    pattern = re.compile(r'"([^"]+)"')

    with open(filename, "r", encoding="utf-8") as f:
        for i, line in enumerate(f, start=1):
            line = line.strip()
            if not line:
                continue

            matches = pattern.findall(line)
            for match in matches:
                quoted_texts.append(match)
                line_positions.append(i)

    return quoted_texts, line_positions
