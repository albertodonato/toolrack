"""Utilities for unit conversion."""

#: Binary byte multipliers
BYTE_SUFFIXES = (None, "kib", "mib", "gib", "tib", "pib", "eib", "zib", "yib")


def convert_bbyte(
    value: int, suffix: str | None = None, to: str | None = None
) -> int:
    """Convert a binary byte value across multipliers.

    :param value: the current value.
    :param suffix: the current multiplier for the value (:data:`None`
        for bytes).
    :param to: the target multiplier (:data:`None` for bytes).

    """
    if suffix:
        suffix = suffix.lower()
    if suffix not in BYTE_SUFFIXES:
        raise ValueError("Unknown multiplier suffix")
    if to not in BYTE_SUFFIXES:
        raise ValueError("Unknown target multiplier")
    multiplier: int = 2 ** (10 * BYTE_SUFFIXES.index(suffix))
    converted = value * multiplier
    if to:
        to = to.lower()
        divider = 2 ** (10 * BYTE_SUFFIXES.index(to))
        converted = converted / divider
    return converted
