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
        self.comparators = []

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
        number_of_inputs = self.get_max_input() + 1
        max_sequence_to_check = (1 << number_of_inputs) - 1
        try:
            for i in range(0, max_sequence_to_check):
                ones_count = i.bit_count()
                if ones_count > 0:
                    zeros_count = number_of_inputs - ones_count
                    expected_sorted_sequence = ((1 << ones_count) - 1) << zeros_count
                else:
                    expected_sorted_sequence = 0
                if self.sort_binary_sequence(i) != expected_sorted_sequence:
                    return False
                if show_progress and i % 100 == 0:
                    percent_complete = round(i * 100 / max_sequence_to_check)
                    print(f"\rChecking... {percent_complete}%", end="")
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
        x_scale = scale * 35
        y_scale = scale * 20
        input_line_width = 1
        comparator_line_width = 1
        comparator_radius = 3

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
                    cx = other_pos + x_scale / 3

            # Generate two circles and a line representing the comparator
            y1 = y_scale + c.i1 * y_scale
            y2 = y_scale + c.i2 * y_scale
            comparators_svg += (
                f"<circle cx='{cx}' cy='{y1}' r='{comparator_radius}' style='stroke:black;stroke-width:1;' />"
                f"<line x1='{cx}' y1='{y1}' x2='{cx}' y2='{y2}' style='stroke:black;stroke-width:{comparator_line_width};' />"
                f"<circle cx='{cx}' cy='{y2}' r='{comparator_radius}' style='stroke:black;stroke-width:1;' />"
            )
            # Add this comparator to the current group
            group[c] = cx

        # Generate line SVG elements
        lines_svg = ""
        w += x_scale
        n = self.get_max_input() + 1
        for i in range(0, n):
            y = y_scale + i * y_scale
            lines_svg += f"<line x1='0' y1='{y}' x2='{w}' y2='{y}' style='stroke:black;stroke-width:{input_line_width};' />"

        h = (n + 1) * y_scale
        return (
            "<?xml version='1.0' encoding='utf-8'?>"
            "<!DOCTYPE svg>"
            f"<svg width='{w}px' height='{h}px' xmlns='http://www.w3.org/2000/svg'>"
            "<rect width='100%%' height='100%%' fill='white' />"
            f"{comparators_svg}"
            f"{lines_svg}"
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
