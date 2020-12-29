from typing import List, Sequence, Tuple, Union

Number = Union[float, int]
XYPoint = Tuple[Number, Number]
LineSegment = Tuple[XYPoint, XYPoint]  # Begin and end
MultiLineSegment = List[XYPoint]  # Begin to end; the simplest multi-line segment is a single LineSegment

def join_line_segments(segments: Sequence[LineSegment]) -> List[MultiLineSegment]:
    """
    Given a sequence of pairs of (x, y) points taht define the beginning and end of
    your line segments, returns a list of multi-segments (lists of points, starting at
    the beginning and going through to the end) with as many co-terminal segments
    combined as our greedy algorithm could find.

    Note that if you have more interesting topologies than a basic continuous line
    (like many segments fanning out from a single point in a star), this will
    not combine them.

    This is a really naive method, and it's O(oh-my-God), but it works fine
    for relatively small collections.

    @param segments: Iterable of simple line segments---pairs of (x, y) points,
                     where the first is the beginning and the second is the end
    @return: List of multi-segments (lists of (x, y) points, starting at
             the beginning and going through to the end)

    # Test star-like topology
    #    *--*
    #    |
    # *--*--*
    #    |
    #    *
    >>> join_line_segments([((-1, 0), (0, 0)), ((0, 1), (0, 0)), ((0, -1), (0, 0)), ((0, 0), (1, 0)), ((0, 1), (1, 1))])
    [[(-1, 0), (0, 0), (0, 1), (1, 1)], [(0, -1), (0, 0), (1, 0)]]
    >>> join_line_segments([((-1, 0), (0, 0)), ((0, 1), (0, 0)), ((0, -1), (0, 0)), ((0, 0), (1, 0)), ((1, 1), (2, 1))])
    [[(-1, 0), (0, 0), (0, 1)], [(0, -1), (0, 0), (1, 0)], [(1, 1), (2, 1)]]
    >>> join_line_segments([((-105.13, 39.9), (-104, 40)), ((-105.117, 39.912), (-105.118, 39.912)), ((-105.1184, 39.9119), (-105.11843, 39.91187)), ((-105.118, 39.912), (-105.1184, 39.9119))])
    [[(-105.13, 39.9), (-104, 40)], [(-105.117, 39.912), (-105.118, 39.912), (-105.1184, 39.9119), (-105.11843, 39.91187)]]

    """
    # first item in the tuple is the point,
    # second is which indices share it (index plus a bool for is-end of the original segment)
    PointList = List[Tuple[XYPoint, List[Tuple[int, int]]]]

    def find_coterminal_points(multipoints: PointList) -> PointList:
        joined = []
        i = 0
        while i < len(multipoints):
            if i + 1 < len(multipoints):
                loc1 = multipoints[i][0]
                loc2 = multipoints[i + 1][0]
                if loc1 == loc2:
                    joined.append((loc1, multipoints[i][1] + multipoints[i + 1][1]))
                    i += 1
                else:
                    joined.append(multipoints[i])
            else:
                joined.append(multipoints[i])
            i += 1
        return joined

    def find_shared_points(multipoints: PointList) -> List[List[Tuple[int, int]]]:
        joined_multipoints = find_coterminal_points(multipoints)
        rejoined = find_coterminal_points(joined_multipoints)
        while len(rejoined) < len(joined_multipoints):
            joined_multipoints = rejoined
            rejoined = find_coterminal_points(joined_multipoints)
        return sorted([point_list for loc_ignored, point_list in rejoined])

    unsorted_points = [(xy, [(idx, is_end)])
                       for idx, begin_and_end_points in enumerate(segments)
                       for is_end, xy in enumerate(begin_and_end_points)]

    shared_points = find_shared_points(sorted(unsorted_points))

    # Reconstruct the points into segments---we no longer care about the (x, y), just the indices from which the points came
    reconstructed_multisegments = []
    unused_indices = set(range(len(segments)))
    while unused_indices:
        idx = unused_indices.pop()
        new_segment = [segments[idx][0], segments[idx][1]]
        find_nodelist = lambda node_idx, want_end: next(shared_nodes
                                                        for shared_nodes in shared_points
                                                        if (node_idx, want_end) in shared_nodes)
        unused_in_nodelist = lambda node_list: (idx_and_is_end
                                                for idx_and_is_end in node_list
                                                if idx_and_is_end[0] in unused_indices)

        for want_end in (True, False):
            unused_in_nodelist_generator = unused_in_nodelist(find_nodelist(idx, want_end))
            shares_our_node = next(unused_in_nodelist_generator, None)
            while shares_our_node is not None:  # as long as there's another node that begins at our multisegment's end
                add_idx, shares_end = shares_our_node
                unused_indices.remove(add_idx)
                node_to_add = segments[add_idx][not shares_end]
                if node_to_add in new_segment:
                    shares_our_node = next(unused_in_nodelist_generator, None)
                else:
                    new_segment.append(node_to_add)
                    try:
                        unused_in_nodelist_generator = unused_in_nodelist(find_nodelist(add_idx, not shares_end))
                        shares_our_node = next(unused_in_nodelist_generator, None)
                    except StopIteration:
                        shares_our_node = None

        reconstructed_multisegments.append(new_segment)
    return reconstructed_multisegments

