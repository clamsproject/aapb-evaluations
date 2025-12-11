import bisect
from typing import List, Tuple, Union, Dict, Optional

numeric = Union[int, float]


def match_nearest_points(
    query_points: List[numeric],
    reference_points: List[numeric],
    tolerance: numeric
) -> Dict[numeric, Optional[numeric]]:
    """
    For each query point, find the nearest reference point within tolerance.

    Uses binary search (bisect) for efficient matching. If multiple query
    points match to the same reference point, all matches are preserved.

    :param query_points: List of points to match
    :param reference_points: List of reference points to match against
    :param tolerance: Maximum allowed distance for a match
    :return: Dict mapping query_point -> nearest_reference_point (or None
             if no match within tolerance)
    :rtype: Dict[numeric, Optional[numeric]]

    Example:
        >>> match_nearest_points([100, 205, 500], [0, 200, 400], tolerance=10)
        {100: None, 205: 200, 500: None}
    """
    if not reference_points:
        return {q: None for q in query_points}

    sorted_refs = sorted(reference_points)
    matches = {}

    for query in query_points:
        # Check exact match first
        if query in reference_points:
            matches[query] = query
            continue

        # Use bisect to find nearest candidates efficiently
        idx = bisect.bisect_left(sorted_refs, query)

        # Check up to 2 candidates: the point at idx-1 and at idx
        candidates = []
        if idx > 0:
            candidates.append(sorted_refs[idx - 1])
        if idx < len(sorted_refs):
            candidates.append(sorted_refs[idx])

        # Find the closest candidate within tolerance
        if candidates:
            closest = min(candidates, key=lambda x: abs(x - query))
            if abs(closest - query) <= tolerance:
                matches[query] = closest
            else:
                matches[query] = None
        else:
            matches[query] = None

    return matches


def find_range_index(ranges: List[Tuple[numeric, numeric]], x: numeric, threshold=0) -> int:
    """
    Finds the index of the range containing x using bisect module.
    
    :param ranges: A list of (start, end) tuples, sorted by start time
               and assumed to be non-overlapping (end_i <= start_{i+1}).
    :param x: The number to locate.
    :param threshold: A threshold value to adjust the range check (default is 0).
                      If x is within [start, end - threshold), it is considered in range.
    
    :return: The index of the tuple (start, end) such that start <= x < end,
             or -1 if x is not in any range.
    """
    ranges = [(start - threshold, end + threshold) for start, end in ranges]
    start_times = [r[0] for r in ranges]

    # Find the insertion point for x in the start times.
    # bisect_right gives index `idx` where all elements <= x are to the left.
    # The candidate range containing x must therefore be at index idx - 1.
    idx = bisect.bisect_right(start_times, x)
    candidate_idx = idx - 1

    # Check if the candidate index is valid and if x falls in its range
    if 0 <= candidate_idx < len(ranges):
        start, end = ranges[candidate_idx]
        if start <= x < end:
            return candidate_idx

    return -1


def parse_label_map(args: List[str]) -> dict:
    """
    Parse label map from CLI arguments.

    Supports both space-separated and comma-separated formats:
    - Identity mappings: ["eng", "spa", "fre"] → eng:eng, spa:spa, fre:fre
    - Explicit mappings: ["eng:english", "spa:spanish"]
    - Mixed: ["eng", "spa", "kor:asian", "jpn:asian"]
    - Comma-separated: ["eng,spa,fre"] or ["eng:english,spa:spanish"]

    :param args: List of label mapping strings from command line
    :return: Dictionary mapping input labels to output labels
    :rtype: dict
    """
    label_map = {}
    for arg in args:
        # Split by comma to handle comma-separated format
        for mapping in arg.split(','):
            mapping = mapping.strip()
            if ':' in mapping:
                # Explicit mapping: IN:OUT
                in_label, out_label = mapping.split(':', 1)
                label_map[in_label.strip()] = out_label.strip()
            else:
                # Identity mapping: IN → IN:IN
                label = mapping.strip()
                if label:  # ignore empty strings
                    label_map[label] = label
    return label_map
