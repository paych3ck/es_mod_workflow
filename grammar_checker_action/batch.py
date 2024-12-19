from typing import List, Tuple


def create_batches(texts: List[str], lines: List[int], max_chars: int = 10000) -> List[Tuple[List[str], List[int]]]:
    batches = []
    current_batch_texts = []
    current_batch_lines = []
    current_length = 0

    for text, line in zip(texts, lines):
        text_length = len(text) + 1 if current_batch_texts else len(text)
        if current_length + text_length > max_chars:
            if current_batch_texts:
                batches.append((current_batch_texts, current_batch_lines))
                current_batch_texts = []
                current_batch_lines = []
                current_length = 0
        current_batch_texts.append(text)
        current_batch_lines.append(line)
        current_length += text_length

    if current_batch_texts:
        batches.append((current_batch_texts, current_batch_lines))

    return batches
