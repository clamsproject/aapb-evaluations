import bisect
from typing import List, Tuple, Union

numeric = Union[int, float]


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
