# The MIT License (MIT)
#
# Copyright (c) 2024 Brian Pursley
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

import unittest
import platform

from sortingnetwork import Comparator, ComparisonNetwork


class ComparatorTests(unittest.TestCase):
    def test_comparator(self):
        test_cases = [
            (0, 1, 0, 1, "0:1"),
            (1, 0, 0, 1, "0:1"),
            (0, 2, 0, 2, "0:2"),
            (2, 0, 0, 2, "0:2"),
            (1, 2, 1, 2, "1:2"),
            (2, 1, 1, 2, "1:2"),
        ]
        for i1, i2, expected_i1, expected_i2, expected_str in test_cases:
            with self.subTest(i1=i1, i2=i2):
                c = Comparator(i1, i2)
                self.assertEqual(c.i1, expected_i1)
                self.assertEqual(c.i2, expected_i2)
                self.assertEqual(c.__str__(), expected_str)
                self.assertEqual(c.__repr__(), expected_str)

    def test_comparator_eq(self):
        test_cases = [
            (Comparator(0, 1), Comparator(0, 1), True),
            (Comparator(0, 1), Comparator(1, 0), True),
            (Comparator(0, 1), Comparator(0, 2), False),
            (Comparator(0, 1), Comparator(1, 2), False),
            (Comparator(0, 1), Comparator(2, 3), False),
        ]
        for c1, c2, expected in test_cases:
            with self.subTest(c1=c1, c2=c2):
                self.assertEqual(c1 == c2, expected)

    def test_comparator_overlaps(self):
        test_cases = [
            (Comparator(0, 1), Comparator(2, 3), False),
            (Comparator(2, 3), Comparator(0, 1), False),
            (Comparator(0, 2), Comparator(1, 3), True),
            (Comparator(0, 3), Comparator(1, 2), True),
            (Comparator(1, 3), Comparator(0, 2), True)
        ]
        for c1, c2, expected in test_cases:
            with self.subTest(c1=c1, c2=c2):
                self.assertEqual(c1.overlaps(c2), expected)

    def test_comparator_has_same_input(self):
        test_cases = [
            (Comparator(0, 1), Comparator(0, 1), True),
            (Comparator(0, 1), Comparator(1, 2), True),
            (Comparator(0, 1), Comparator(0, 2), True),
            (Comparator(0, 1), Comparator(2, 3), False),
            (Comparator(0, 3), Comparator(1, 2), False),
            (Comparator(2, 3), Comparator(0, 1), False),
        ]
        for c1, c2, expected in test_cases:
            with self.subTest(c1=c1, c2=c2):
                self.assertEqual(c1.has_same_input(c2), expected)


class ComparisonNetworkTests(unittest.TestCase):
    def test_comparison_network(self):
        cn = ComparisonNetwork()
        self.assertEqual(cn.comparators, [])
        with self.assertRaises(ValueError):
            cn.get_max_input()
        self.assertFalse(cn.is_sorting_network())
        self.assertEqual(cn.__str__(), "")
        self.assertEqual(cn.__repr__(), "")

    def test_comparison_network_append_and_remove(self):
        cn = ComparisonNetwork()
        c = Comparator(0, 1)
        cn.append(c)
        self.assertEqual(cn.comparators, [c])
        self.assertEqual(cn.get_max_input(), 1)
        self.assertTrue(cn.is_sorting_network())
        self.assertEqual(cn.__str__(), "0:1")
        self.assertEqual(cn.__repr__(), "0:1")

        cn.remove(c)
        self.assertEqual(cn.comparators, [])

        with self.assertRaises(ValueError):
            cn.remove(c)

    def test_empty_comparison_network_svg_should_fail(self):
        with self.assertRaises(ValueError):
            ComparisonNetwork().svg()

    def test_example_svg(self):
        self.maxDiff = None
        test_cases = [
            ("../examples/3-input.cn", "../examples/3-input.svg"),
            ("../examples/4-input.cn", "../examples/4-input.svg"),
            ("../examples/5-input.cn", "../examples/5-input.svg"),
            ("../examples/6-input.cn", "../examples/6-input.svg"),
            ("../examples/7-input.cn", "../examples/7-input.svg"),
            ("../examples/8-input.cn", "../examples/8-input.svg"),
            ("../examples/8-input-bitonic.cn", "../examples/8-input-bitonic.svg"),
            ("../examples/9-input.cn", "../examples/9-input.svg"),
            ("../examples/10-input.cn", "../examples/10-input.svg"),
            ("../examples/11-input.cn", "../examples/11-input.svg"),
            ("../examples/12-input.cn", "../examples/12-input.svg"),
            ("../examples/16-input.cn", "../examples/16-input.svg"),
        ]
        for input_filename, svg_filename in test_cases:
            with self.subTest(inputFilename=input_filename, svgFilename=svg_filename):
                cn = ComparisonNetwork.from_file(input_filename)
                with open(svg_filename, "r") as f:
                    expected_svg = f.read().strip()
                self.assertEqual(cn.svg(), expected_svg)

    # https://github.com/brianpursley/sorting-network/issues/2
    def test_optimize_should_order_comparators_to_avoid_unnecessary_gaps(self):
        self.maxDiff = None
        expected_str = "2:5,0:1\n0:3,4:5"
        expected_svg = "<?xml version='1.0' encoding='utf-8'?><!DOCTYPE svg><svg width='105.0' height='140.0' viewBox='0 0 315 420' xmlns='http://www.w3.org/2000/svg'><rect width='315' height='420' fill='#fff'/><path style='stroke:#000;stroke-width:3;fill:#000' d='M96 180a9 9 0 1 1 18 0a9 9 0 1 1-18 0zm9 0V360m-9 0a9 9 0 1 1 18 0a9 9 0 1 1-18 0zM96 60a9 9 0 1 1 18 0a9 9 0 1 1-18 0zm9 0V120m-9 0a9 9 0 1 1 18 0a9 9 0 1 1-18 0zM201 60a9 9 0 1 1 18 0a9 9 0 1 1-18 0zm9 0V240m-9 0a9 9 0 1 1 18 0a9 9 0 1 1-18 0zM201 300a9 9 0 1 1 18 0a9 9 0 1 1-18 0zm9 0V360m-9 0a9 9 0 1 1 18 0a9 9 0 1 1-18 0z'/><path style='stroke:#000;stroke-width:3' d='M0 60H315M0 120H315M0 180H315M0 240H315M0 300H315M0 360H315'/></svg>"

        cn = ComparisonNetwork.from_string("2:5,0:1,4:5,0:3")
        self.assertEqual(cn.__str__(), expected_str)
        self.assertEqual(cn.__repr__(), expected_str)
        self.assertEqual(cn.svg(), expected_svg)

        cn = ComparisonNetwork.from_string("2:5,4:5,0:1,0:3")
        self.assertEqual(cn.__str__(), expected_str)
        self.assertEqual(cn.__repr__(), expected_str)
        self.assertEqual(cn.svg(), expected_svg)

    def test_is_sorting_network_should_identify_sorting_network(self):
        file_test_cases = [
            "../examples/3-input.cn",
            "../examples/4-input.cn",
            "../examples/5-input.cn",
            "../examples/6-input.cn",
            "../examples/7-input.cn",
            "../examples/8-input.cn",
            "../examples/8-input-bitonic.cn",
            "../examples/9-input.cn",
            "../examples/10-input.cn",
            "../examples/11-input.cn",
            "../examples/12-input.cn",
            "../examples/16-input.cn",
            "../examples/20-input.cn",
            "../examples/24-input.cn",
        ]
        for input_filename in file_test_cases:
            with self.subTest(inputFilename=input_filename):
                self._test_is_sorting_network_from_file(input_filename)

        test_cases = [
            "0:1",
            "0:1,1:2,0:1",
            "0:2,1:3,0:1,2:3,1:2",
        ]
        for s in test_cases:
            with self.subTest(s=s):
                cn = ComparisonNetwork.from_string(s)
                self.assertTrue(cn.is_sorting_network())

    @unittest.skipUnless(platform.python_implementation() == "PyPy", "slow tests only run when using pypy")
    def test_is_sorting_network_should_identify_large_sorting_network(self):
        file_test_cases = [
            "../examples/28-input.cn",
            "../examples/32-input.cn",
        ]
        for input_filename in file_test_cases:
            with self.subTest(inputFilename=input_filename):
                self._test_is_sorting_network_from_file(input_filename)

    def _test_is_sorting_network_from_file(self, input_filename):
        cn = ComparisonNetwork.from_file(input_filename)
        self.assertTrue(cn.is_sorting_network())

    def test_is_sorting_network_should_identify_non_sorting_network(self):
        cn = ComparisonNetwork()
        self.assertFalse(cn.is_sorting_network())

        file_test_cases = [
            "../examples/3-input.cn",
            "../examples/4-input.cn",
            "../examples/5-input.cn",
            "../examples/6-input.cn",
            "../examples/7-input.cn",
            "../examples/8-input.cn",
            "../examples/8-input-bitonic.cn",
            "../examples/9-input.cn",
            "../examples/10-input.cn",
            "../examples/11-input.cn",
            "../examples/12-input.cn",
            "../examples/16-input.cn",
            "../examples/20-input.cn",
            "../examples/24-input.cn",
        ]
        for input_filename in file_test_cases:
            with self.subTest(inputFilename=input_filename):
                self._test_is_non_sorting_network_from_file(input_filename)

        test_cases = [
            "0:2",
            "1:2",
            "0:1,1:2",
            "0:1,1:3,0:1",
            "0:1,1:3,2:3",
            "0:1,1:3,2:3,0:3",
            "0:2,1:3,0:1,2:3",
        ]
        for s in test_cases:
            with self.subTest(s=s):
                cn = ComparisonNetwork.from_string(s)
                self.assertFalse(cn.is_sorting_network())

    @unittest.skipUnless(platform.python_implementation() == "PyPy", "slow tests only run when using pypy")
    def test_is_sorting_network_should_identify_large_non_sorting_network(self):
        file_test_cases = [
            "../examples/28-input.cn",
            "../examples/32-input.cn",
        ]
        for input_filename in file_test_cases:
            with self.subTest(inputFilename=input_filename):
                self._test_is_non_sorting_network_from_file(input_filename)

    def _test_is_non_sorting_network_from_file(self, input_filename):
        cn = ComparisonNetwork.from_file(input_filename)
        m = cn.get_max_input()
        # First confirm this is a sorting network, then systematically remove each comparator
        # and confirm it is no longer a sorting network.
        self.assertTrue(cn.is_sorting_network())
        for i in range(len(cn.comparators)):
            cn2 = ComparisonNetwork()
            cn2.comparators = cn.comparators.copy()
            removed_comparator = cn2.comparators.pop(i)
            if cn2.get_max_input() != m:
                # Removing this comparator resulted in a network with fewer inputs, so skip this one
                continue
            if cn2.is_sorting_network():
                self.fail(f"Unexpected sorting network after removing comparator {removed_comparator} from position {i}")

    def test__optimize_comparator_depth_group(self):
        test_cases = [
            [Comparator(0, 2), Comparator(1, 5), Comparator(3, 4)],
            [Comparator(1, 5), Comparator(0, 2), Comparator(3, 4)],
            [Comparator(0, 2), Comparator(3, 4), Comparator(1, 5)],
            [Comparator(1, 5), Comparator(3, 4), Comparator(0, 2)],
            [Comparator(3, 4), Comparator(0, 2), Comparator(1, 5)],
            [Comparator(3, 4), Comparator(1, 5), Comparator(0, 2)],
        ]
        expected = [Comparator(0, 2), Comparator(3, 4), Comparator(1, 5)]
        cn = ComparisonNetwork()
        for comparators in test_cases:
            with self.subTest(comparators=comparators):
                actual = cn._optimize_comparator_depth_group(comparators)
                self.assertEqual(actual, expected)

    def test__get_optimized_comparators(self):
        test_cases = [
            "0:2,1:5,3:4",
            "1:5,0:2,3:4",
            "0:2,3:4,1:5",
            "1:5,3:4,0:2",
            "3:4,0:2,1:5",
            "3:4,1:5,0:2",
        ]
        expected = [Comparator(0, 2), Comparator(3, 4), Comparator(1, 5)]
        for s in test_cases:
            with self.subTest(s=s):
                cn = ComparisonNetwork.from_string(s)
                original = cn.comparators.copy()
                actual = cn._get_optimized_comparators()
                self.assertEqual(actual, expected)
                self.assertEqual(cn.comparators, original)

    def test_sort_binary_sequence(self):
        test_cases = [
            ("0:1", 0b01, 0b10),
            ("0:1", 0b10, 0b10),
            ("0:1", 0b11, 0b11),
            ("0:1,1:2,0:1", 0b001, 0b100),
            ("0:1,1:2,0:1", 0b010, 0b100),
            ("0:1,1:2,0:1", 0b100, 0b100),
            ("0:1,1:2,0:1", 0b011, 0b110),
            ("0:1,1:2,0:1", 0b101, 0b110),
            ("0:1,1:2,0:1", 0b110, 0b110),
            ("0:1,1:2,0:1", 0b111, 0b111),
        ]
        for s, sequence, expected in test_cases:
            with self.subTest(sequence=bin(sequence), expected=bin(expected)):
                cn = ComparisonNetwork.from_string(s)
                actual = cn.sort_binary_sequence(sequence)
                self.assertEqual(actual, expected)

    def test_sort_sequence(self):
        test_cases = [
            ("0:1", [0, 1], [0, 1]),
            ("0:1", [1, 0], [0, 1]),
            ("0:1", [1, 1], [1, 1]),
            ("0:1,1:2,0:1", [0, 0, 1], [0, 0, 1]),
            ("0:1,1:2,0:1", [0, 1, 0], [0, 0, 1]),
            ("0:1,1:2,0:1", [1, 0, 0], [0, 0, 1]),
            ("0:1,1:2,0:1", [0, 1, 1], [0, 1, 1]),
            ("0:1,1:2,0:1", [1, 0, 1], [0, 1, 1]),
            ("0:1,1:2,0:1", [1, 1, 0], [0, 1, 1]),
            ("0:1,1:2,0:1", [1, 1, 1], [1, 1, 1]),
            ("0:1", [2, 3], [2, 3]),
            ("0:1", [3, 2], [2, 3]),
            ("0:1", [3, 3], [3, 3]),
            ("0:1", ["a", "b"], ["a", "b"]),
            ("0:1", ["b", "a"], ["a", "b"]),
            ("0:1", ["b", "b"], ["b", "b"]),
        ]
        for s, sequence, expected in test_cases:
            with self.subTest(sequence=sequence, expected=expected):
                cn = ComparisonNetwork.from_string(s)
                actual = cn.sort_sequence(sequence)
                self.assertEqual(actual, expected)
