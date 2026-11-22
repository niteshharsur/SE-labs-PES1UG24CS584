import math
import re


HS_CODE = re.compile(r"[0-9]{2,}(?:\.[0-9]+)*")


def _nonnegative_number(text):
    try:
        value = float(text)
    except ValueError:
        return None
    return value if math.isfinite(value) and value >= 0 else None


def parse_declaration(text):
    """Return (normalized category, declared value), or None for invalid input."""
    if not isinstance(text, str) or text.count(":") != 1:
        return None
    category, value_text = text.split(":")
    category = category.strip().lower()
    value = _nonnegative_number(value_text)
    if not category or value is None:
        return None
    return category, value


def duty_amount(text):
    """Return percentage duty, or None for invalid or overflowing input."""
    if not isinstance(text, str) or text.count("@") != 1:
        return None
    value_text, rate_text = text.split("@")
    value = _nonnegative_number(value_text)
    rate = _nonnegative_number(rate_text)
    if value is None or rate is None:
        return None
    product = value * rate
    if math.isfinite(product):
        return product / 100
    duty = value * (rate / 100)
    return duty if math.isfinite(duty) else None


def hs_chapter(code):
    """Return the chapter from a compact or dotted numeric HS code."""
    if not isinstance(code, str):
        return None
    code = code.strip()
    if HS_CODE.fullmatch(code) is None:
        return None
    chapter = int(code[:2])
    return chapter if chapter else None


def main():
    examples = (
        ("parse_declaration", "category:value (e.g. electronics:25000)",
         "Category and Value", parse_declaration),
        ("duty_amount", "value@rate (e.g. 25000@20)",
         "Duty Amount", duty_amount),
        ("hs_chapter", "an HS code (e.g. 8517.12)",
         "Chapter", hs_chapter),
    )

    for index, (name, prompt, label, function) in enumerate(examples):
        if index:
            print()
        print(f"==== Running {name} ====")
        try:
            user_input = input(f"Enter {prompt}: ")
        except EOFError:
            print("No input provided.")
            return
        result = function(user_input)
        if result is None:
            print("Invalid input.")
        else:
            print(f"{label}: {result}")


if __name__ == "__main__":
    main()
