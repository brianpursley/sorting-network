#!/usr/bin/env python3

# The MIT License (MIT)
# 
# Copyright (c) 2015 Brian Pursley
# 
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
# 
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import argparse
import ast
import sys


class Comparator:
    """
    A comparator is defined by two input positions.
    """

    def __init__(self, i1: int, i2: int):
        """
        Initialize a comparator with two input positions.

        The comparator will be created with the smaller input position as i1 and the larger input position as i2.

        :param i1: First input position
        :param i2: Second input position
        """
        if i1 == i2:
            raise ValueError("Comparator inputs must be different")
        if i1 < i2:
            self.i1 = i1
            self.i2 = i2
        else:
            self.i1 = i2
            self.i2 = i1

    @staticmethod
    def from_string(s: str):
        """
        Initialize a comparator from a string in the format "i1:i2".

        The comparator will be created with the smaller input position as i1 and the larger input position as i2.

        :param s: String in the format "i1:i2"
        :return: Comparator created from the string
        """
        inputs = s.strip().split(":")
        if len(inputs) != 2:
            raise ValueError(f"Invalid comparator string: {s}")
        if not inputs[0].isnumeric() or not inputs[1].isnumeric():
            raise ValueError(f"Invalid comparator string: {s}")
        return Comparator(int(inputs[0]), int(inputs[1]))

    def __str__(self) -> str:
        return f"{self.i1}:{self.i2}"

    def __repr__(self) -> str:
        return self.__str__()

    def __hash__(self) -> int:
        return f"{self.i1}:{self.i2}".__hash__()

    def __eq__(self, other: 'Comparator') -> bool:
        return self.i1 == other.i1 and self.i2 == other.i2

    def overlaps(self, other: 'Comparator') -> bool:
        """
        Determine if this comparator overlaps another comparator.
        :param other: Comparator to compare against
        :return: True if the comparators overlap, False otherwise
        """
        return (self.i1 < other.i1 < self.i2) or \
            (self.i1 < other.i2 < self.i2) or \
            (other.i1 < self.i1 < other.i2) or \
            (other.i1 < self.i2 < other.i2)

    def has_same_input(self, other: 'Comparator') -> bool:
        """
        Determine if this comparator has the same input as another comparator.
        :param other: Comparator to compare against
        :return: True if the comparators have the same input, False otherwise
        """
        return self.i1 == other.i1 or \
            self.i1 == other.i2 or \
            self.i2 == other.i1 or \
            self.i2 == other.i2


class ComparisonNetwork:
    """
    A comparison network is a collection of comparators that can be used to sort a sequence of items.
    """

    def __init__(self):
        """
        Initialize a comparison network with an empty list of comparators.
        """
        self.comparators: list[Comparator] = []

    @staticmethod
    def from_file(filename: str) -> 'ComparisonNetwork':
        """
        Read a comparison network from a file.
        :param filename: File to read from
        :return: Comparison network read from the file
        """
        cn = ComparisonNetwork()
        if filename:
            with open(filename, 'r') as f:
                for line in f:
                    for c in line.split(","):
                        cn.append(Comparator.from_string(c))
        else:
            for line in sys.stdin:
                for c in line.split(","):
                    cn.append(Comparator.from_string(c))
        return cn

    @staticmethod
    def from_string(s: str) -> 'ComparisonNetwork':
        """
        Read a comparison network from a string.
        :param s: String to read from
        :return: Comparison network read from the string
        """
        cn = ComparisonNetwork()
        for c in s.split(","):
            cn.append(Comparator.from_string(c))
        return cn

    def __str__(self) -> str:
        result = ""
        group = []
        for c in self._get_optimized_comparators():
            for other in group:
                if c.has_same_input(other):
                    result += ','.join(map(str, group)) + "\n"
                    del group[:]
                    break
            group.append(c)
        result += ','.join(map(str, group))
        return result

    def __repr__(self) -> str:
        return self.__str__()

    def __getitem__(self, index: int) -> Comparator:
        return self.comparators[index]

    def append(self, c: Comparator) -> None:
        """
        Add a comparator to the comparison network.
        :param c: Comparator to add
        """
        self.comparators.append(c)

    def remove(self, c: Comparator) -> None:
        """
        Remove a comparator from the comparison network.
        :param c: Comparator to remove
        """
        self.comparators.remove(c)

    def is_sorting_network(self, show_progress: bool = False) -> bool:
        """
        Determine if this comparison network is a sorting network.
        :param show_progress: Whether to show progress while checking
        :return: True if this comparison network is a sorting network, False otherwise
        """
        if len(self.comparators) == 0:
            return False
        # Use the zero-one principle to determine if this comparison network is a sorting network
        # https://en.wikipedia.org/wiki/Sorting_network#Zero-one_principle
        # time complexity: O(m * 1.618^n) where m is the number of comparators,
        # n is the number of inputs and 1.618 is the golden ratio
        # refer: Hisayasu Kuroda. (1997). A proposal of Gap Decrease Sorting Network.
        # Trans.IPS.Japan, vol.38, no.3, p.381-389. http://id.nii.ac.jp/1001/00013442/
        # The zero-one principle shows that it is sufficient to verify 2^n types of inputs.
        # This algorithm classifies 2^n inputs and performs depth-first search
        # by dividing into O(1.618^n) branches.
        m, n = len(self.comparators), (self.get_max_input() + 1)
        # Reduce class object property reads for optimization performance
        cmps = list(map(lambda x: (x.i1, x.i2), self.comparators))
        # initial p state is all '#'=unknown: not determined to be 0 or 1
        stack = [(0, [2] * n, 0, n - 1)]
        # Progress is measured in 128 is 100%
        progress, prev_progress = 0, -1
        try:
            # 'a: Loop of stack
            while stack:
                # fetch branch stack
                # i: Index of comparator
                # p: State of each line
                #    (0:'0'=zero, 1:'1'=one, 2:'#'=unknown)
                # z: leading non-zero position
                # o: trailing non-one position
                i, p, z, o = stack.pop()
                progress += 128 >> i
                # 'b: Loop of comparators
                while i < m:
                    # fetch comparator
                    # For optimization, convert class properties to tuple
                    # for reference due to the very high number of accesses
                    a, b = cmps[i]
                    i += 1
                    # The table can be written this way, regarding
                    # the output of the comparison exchanger as equivalent to
                    # the output of the minmax function.
                    #
                    # Truth table for the usual minmax function
                    #
                    # | (A,B) | (min(A,B),max(A,B)) |
                    # |-------|---------------------|
                    # | (0,0) |        (0,0)        |
                    # | (0,1) |        (0,1)        |
                    # | (1,0) |        (0,1)        |
                    # | (1,1) |        (1,1)        |
                    # |-------|---------------------|
                    #
                    # Truth table for minmax function considering '#'=Unknown
                    # https://en.wikipedia.org/wiki/Three-valued_logic
                    #
                    # | (A,B) | (min(A,B),max(A,B)) |
                    # |-------|---------------------|
                    # | (#,#) |   (0,0) or (#,1)    | [branch] A=# and B=#
                    # |-------|---------------------| {alternatively, branch (0,#) or (1,1)}
                    # | (1,#) |    (#,1) = (B,A)    |
                    # | (1,0) |    (0,1) = (B,A)    | [swap] A!=0 and B!=1
                    # | (#,0) |    (0,#) = (B,A)    |   and (A!=# or B!=#)
                    # |-------|---------------------|
                    # | (0,#) |    (0,#) = (A,B)    |
                    # | (#,1) |    (#,1) = (A,B)    |
                    # | (0,0) |    (0,0) = (A,B)    | [noop] A=0 or B=1
                    # | (0,1) |    (0,1) = (A,B)    |
                    # | (1,1) |    (1,1) = (A,B)    |
                    # |-------|---------------------|
                    #
                    # Check if p reaches '0...01...1' or '0...0#1...1' sorted in all branches.
                    if p[a] == 2 and p[b] == 2:
                        # (p[a],p[b]) are (#,#), then we have the choice:
                        # (p[a],p[b]) become (0,0) or (#,1).
                        # alternatively, the choice could be:
                        # (p[a],p[b]) become (0,#) or (1,1).
                        # The branches are only in this part.
                        # Let n be the number of unknowns,
                        # the maximum number of branches T(n) is:
                        # T(n) = T(n-1) + T(n-2),  T(1) = 1, T(2) = 2.
                        # This is a Fibonacci sequence.
                        # Fibonacci sequence asymptotically approaches
                        # the power of the golden ratio.
                        q = p.copy()  # copy state for branch
                        # branch (#,#) -> (0,0), current (#,#) -> (#,1)
                        q[a], q[b], p[b] = 0, 0, 1
                        # check 'q' leading non-zero position
                        for j in range(z, o):
                            if q[j] != 0:
                                # if 'q' is not sorted yet
                                progress -= 128 >> i
                                stack.append((i, q, j, o))
                                break  # continue 'b
                        # check p trailing non-one position
                        for j in range(o, z, -1):
                            if p[j] != 1:
                                # if p is not sorted yet
                                o = j
                                break  # continue 'b
                        else:
                            # if p is sorted in this branch:
                            break  # continue 'a
                    elif p[a] != 0 and p[b] != 1:
                        # If (p[a],p[b]) are in [(#,0),(1,0),(1,#)],
                        # then swap (p[a],p[b]) to (p[b],p[a]).
                        p[a], p[b] = p[b], p[a]
                        # check p leading non-zero position
                        for j in range(z, o):
                            if p[j] != 0:
                                # if p is not sorted yet
                                z = j
                                break  # continue 'b
                        else:
                            # if p is sorted in this branch:
                            break  # continue 'a
                        # check p trailing non-one position
                        for j in range(o, z, -1):
                            if p[j] != 1:
                                # if p is not sorted yet
                                o = j
                                break  # continue 'b
                        else:
                            # if p is sorted in this branch:
                            break  # continue 'a
                else:
                    # If there is any branch where the sequence
                    # is not sorted using all comparators
                    return False
                if show_progress and prev_progress != progress:
                    prev_progress = progress
                    percent_complete = (100 * progress) >> 7
                    print(f"\rChecking... {percent_complete}%", end="")
            # If all branches are sorted
            return True
        finally:
            if show_progress:
                print("\r", end="")

    def sort_binary_sequence(self, sequence: int) -> int:
        """
        Sort a binary sequence using this comparison network.

        1s are sorted into the more significant bits, and 0s are sorted into the less significant bits.

        :param sequence: An integer representing a binary sequence to sort
        :return: An integer representing the sorted binary sequence
        """
        result = sequence
        # Apply all comparators to the binary sequence
        for c in self.comparators:
            # Compare the two bits at the comparator's input positions and swap if needed
            pos0 = (result >> c.i1) & 1
            pos1 = (result >> c.i2) & 1
            if pos0 > pos1:
                result ^= (1 << c.i1) | (1 << c.i2)
        return result

    def sort_sequence(self, sequence: list) -> list:
        """
        Sort a sequence using this comparison network.
        :param sequence: A list of items to sort
        :return: A list of items in sorted order
        """
        if len(sequence) != self.get_max_input()+1:
            raise ValueError("Sequence length does not match number of inputs in the comparison network")
        result = list(sequence)
        for c in self.comparators:
            if result[c.i1] > result[c.i2]:
                result[c.i1], result[c.i2] = result[c.i2], result[c.i1]
        return result

    def get_max_input(self) -> int:
        """
        Get the maximum input position used by any comparator in the comparison network.
        :return: The maximum input position
        """
        if len(self.comparators) == 0:
            raise ValueError("Comparison network is empty")
        max_input = 0
        for c in self.comparators:
            if c.i2 > max_input:
                max_input = c.i2
        return max_input

    def _get_optimized_comparators(self) -> list[Comparator]:
        """
        Get the comparators in an optimized order by collapsing them down in order to minimize depth and eliminate unnecessary gaps.

        It groups comparators into depth groups, where each comparator in the group has non-conflicting inputs.
        It then adds each depth group to the result in an optimized order.

        :return: List of comparators in an optimized order
        """
        # Make a copy of the comparators so we can keep track of which comparators are remaining.
        remaining = self.comparators.copy()

        # Add comparators until there are no more remaining
        result = []
        while len(remaining) > 0:
            # Create a list to keep track of the comparators that have been added at the current depth.
            # We will add these as a group, so they can be arranged optimally together.
            current_depth_comparators = []

            # Create a list to keep track of the comparators that have been considered at the current depth, whether they were added or not
            considered = []

            # Find comparators that can be added at the current depth.
            # A comparator can be added if it does not share an input with any other comparator that has been considered at the current depth.
            for c in remaining.copy():
                can_add = True
                for d in considered:
                    if c.has_same_input(d):
                        # This comparator cannot be added because it shares an input with another comparator that has been considered at the current depth.
                        can_add = False
                        break
                if can_add:
                    current_depth_comparators.append(c)
                    remaining.remove(c)
                considered.append(c)

            # Add the comparators that were found at the current depth
            result.extend(ComparisonNetwork._optimize_comparator_depth_group(current_depth_comparators))

        return result

    @staticmethod
    def _optimize_comparator_depth_group(comparators: list[Comparator]) -> list[Comparator]:
        """
        Organize a list of comparators using heuristics to minimize overlap and ensure consistent appearance.

        It is assumed that all comparators in the list have non-conflicting inputs.

        :param comparators: List of comparators to organize
        :return: List of comparators in an optimized order
        """
        # Make a copy of the comparators, so we can keep track of which comparators are remaining
        remaining = comparators.copy()

        # Determine how many comparators each comparator overlaps
        overlap_count = {}
        for c in remaining:
            overlap_count[c] = 0
            for other in remaining:
                if c.overlaps(other):
                    overlap_count[c] += 1

        # Add comparators until there are no more remaining
        result = []
        while len(remaining) > 0:
            # Find the comparators that overlap the fewest other comparators
            min_overlap_count = min(overlap_count.values())
            min_overlap_comparators = [c for c in remaining if overlap_count[c] == min_overlap_count]

            # If there are multiple comparators with the same minimal overlap, then limit to the ones that have the largest input range
            if len(min_overlap_comparators) > 1:
                max_input_range = max([c.i2 - c.i1 for c in min_overlap_comparators])
                min_overlap_comparators = [c for c in min_overlap_comparators if c.i2 - c.i1 == max_input_range]

            # Of the comparators that were found matching the above criteria, add the one with the smallest input position
            comparator_to_add = min(min_overlap_comparators, key=lambda x: x.i1)
            result.append(comparator_to_add)
            remaining.remove(comparator_to_add)
            overlap_count.pop(comparator_to_add)

        return result

    def svg(self) -> str:
        """
        Generate an SVG representation of the comparison network.
        :return: SVG representation of the comparison network
        """
        scale = 1
        reduce = 3
        x_scale = scale * 105
        x_scale_thin = scale * 35
        y_scale = scale * 60
        input_line_width = 3
        comparator_line_width = 3
        comparator_radius = 9

        comparators_svg = ""
        w = x_scale
        group = {}
        for c in self._get_optimized_comparators():

            # If the comparator inputs are the same position as any other comparator in the group, then start a new group
            for other in group:
                if c.has_same_input(other):
                    for _, pos in group.items():
                        if pos > w:
                            w = pos
                    w += x_scale
                    group = {}
                    break

            # Adjust the comparator x position to avoid overlapping any existing comparators in the group
            cx = w
            for other, other_pos in group.items():
                if other_pos >= cx and c.overlaps(other):
                    cx = other_pos + x_scale_thin

            # Generate two circles and a line representing the comparator
            y1 = y_scale + c.i1 * y_scale
            y2 = y_scale + c.i2 * y_scale
            r = comparator_radius
            comparators_svg += (
                f"M{cx-r} {y1}a{r} {r} 0 1 1 {r+r} 0a{r} {r} 0 1 1-{r+r} 0z"
                f"m{r} 0V{y2}"
                f"m-{r} 0a{r} {r} 0 1 1 {r+r} 0a{r} {r} 0 1 1-{r+r} 0z"
            )
            # Add this comparator to the current group
            group[c] = cx

        # Generate line SVG path
        n = self.get_max_input() + 2
        w += x_scale
        h = n * y_scale
        lines_svg = "".join(f"M0 {i * y_scale}H{w}" for i in range(1, n))

        return (
            "<?xml version='1.0' encoding='utf-8'?>"
            "<!DOCTYPE svg>"
            f"<svg width='{w/reduce}' height='{h/reduce}' viewBox='0 0 {w} {h}' xmlns='http://www.w3.org/2000/svg'>"
            f"<rect width='{w}' height='{h}' fill='#fff'/>"
            f"<path style='stroke:#000;stroke-width:{comparator_line_width};fill:#000' d='{comparators_svg}'/>"
            f"<path style='stroke:#000;stroke-width:{input_line_width}' d='{lines_svg}'/>"
            "</svg>"
        )


def main() -> int:
    parser = argparse.ArgumentParser(description="a tool for working with sorting networks")
    parser.add_argument("--input", "-i", metavar="inputfile", help="file containing comparison network definition, or use stdin if not specified", nargs='?', default='')
    subparsers = parser.add_subparsers(dest="command", required=True)

    check_parser = subparsers.add_parser("check", description="check whether it is a sorting network", help="check whether it is a sorting network")
    check_parser.add_argument("--show-progress", action="store_true", help="show percent complete while checking")

    print_parser = subparsers.add_parser("print", description="print the comparison network definition", help="print the comparison network definition")
    print_parser.add_argument("print_filename", metavar="filename", help="the file to save the output to", nargs='?', default='')

    sort_parser = subparsers.add_parser("sort", description="sort a sequence using the input comparison network", help="sort a sequence using the input comparison network")
    sort_parser.add_argument("sort_sequence", metavar="sequence", help="the sequence to sort, e.g. '3,1,2'")

    svg_parser = subparsers.add_parser("svg", description="generate an SVG", help="generate an SVG")
    svg_parser.add_argument("svg_filename", metavar="filename", help="the file to save the SVG to", nargs='?', default='')

    args = parser.parse_args()

    cn = ComparisonNetwork.from_file(args.input)

    if args.command == "check":
        if cn.is_sorting_network(show_progress=args.show_progress):
            print("It is a sorting network!")
            return 0
        else:
            print("It is not a sorting network.")
            return 1

    if args.command == "print":
        if args.print_filename == "":
            print(str(cn))
        else:
            with open(args.print_filename, "w") as f:
                f.write(str(cn))
        return 0

    if args.command == "sort":
        input_sequence = ast.literal_eval(args.sort_sequence)
        for sorted_item in cn.sort_sequence(input_sequence):
            print(sorted_item)
        return 0

    if args.command == "svg":
        if args.svg_filename == "":
            print(cn.svg())
        else:
            with open(args.svg_filename, "w") as f:
                f.write(cn.svg())
        return 0

    return 2


if __name__ == "__main__":
    sys.exit(main())
