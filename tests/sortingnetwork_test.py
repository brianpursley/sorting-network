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
from sortingnetwork import read_comparison_network, read_comparison_network_from_string


class Testing(unittest.TestCase):
    def test_example_svg(self):
        self.maxDiff = None
        test_cases = [
            ("../examples/4-input.cn", "../examples/4-input.svg"),
            ("../examples/5-input.cn", "../examples/5-input.svg"),
            ("../examples/8-input-bitonic.cn", "../examples/8-input-bitonic.svg"),
            ("../examples/16-input.cn", "../examples/16-input.svg"),
        ]
        for input_filename, svg_filename in test_cases:
            with self.subTest(inputFilename=input_filename, svgFilename=svg_filename):
                cn = read_comparison_network(input_filename)
                with open(svg_filename, "r") as f:
                    expected_svg = f.read().strip()
                self.assertEqual(cn.svg(), expected_svg)

    # https://github.com/brianpursley/sorting-network/issues/2
    def test_optimize_should_order_comparators_to_avoid_unnecessary_gaps(self):
        self.maxDiff = None
        expected_str = "2:5,0:1\n4:5,0:3"
        expected_svg = "<?xml version='1.0' encoding='utf-8'?><!DOCTYPE svg><svg width='105px' height='140px' xmlns='http://www.w3.org/2000/svg'><rect width='100%%' height='100%%' fill='white' /><circle cx='35' cy='60' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><line x1='35' y1='60' x2='35' y2='120' style='stroke:black;stroke-width:1' /><circle cx='35' cy='120' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><circle cx='35' cy='20' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><line x1='35' y1='20' x2='35' y2='40' style='stroke:black;stroke-width:1' /><circle cx='35' cy='40' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><circle cx='70' cy='100' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><line x1='70' y1='100' x2='70' y2='120' style='stroke:black;stroke-width:1' /><circle cx='70' cy='120' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><circle cx='70' cy='20' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><line x1='70' y1='20' x2='70' y2='80' style='stroke:black;stroke-width:1' /><circle cx='70' cy='80' r='3' style='stroke:black;stroke-width:1;fill=yellow' /><line x1='0' y1='20' x2='105' y2='20' style='stroke:black;stroke-width:1' /><line x1='0' y1='40' x2='105' y2='40' style='stroke:black;stroke-width:1' /><line x1='0' y1='60' x2='105' y2='60' style='stroke:black;stroke-width:1' /><line x1='0' y1='80' x2='105' y2='80' style='stroke:black;stroke-width:1' /><line x1='0' y1='100' x2='105' y2='100' style='stroke:black;stroke-width:1' /><line x1='0' y1='120' x2='105' y2='120' style='stroke:black;stroke-width:1' /></svg>"

        cn = read_comparison_network_from_string("2:5,0:1,4:5,0:3")
        self.assertEqual(cn.__str__(), expected_str)
        self.assertEqual(cn.svg(), expected_svg)

        cn = read_comparison_network_from_string("2:5,4:5,0:1,0:3")
        self.assertEqual(cn.__str__(), expected_str)
        self.assertEqual(cn.svg(), expected_svg)

    def test_is_sorting_network_should_identify_sorting_network(self):
        file_test_cases = [
            "../examples/4-input.cn",
            "../examples/5-input.cn",
            "../examples/8-input-bitonic.cn",
            "../examples/16-input.cn",
        ]
        for input_filename in file_test_cases:
            with self.subTest(inputFilename=input_filename):
                cn = read_comparison_network(input_filename)
                self.assertTrue(cn.is_sorting_network(False))

        test_cases = [
            "0:1",
            "0:1,1:2,0:1",
            "0:2,1:3,0:1,2:3,1:2",
        ]
        for s in test_cases:
            with self.subTest(s=s):
                cn = read_comparison_network_from_string(s)
                self.assertTrue(cn.is_sorting_network(False))

    def test_is_sorting_network_should_identify_non_sorting_network(self):
        file_test_cases = [
            "../examples/4-input.cn",
            "../examples/5-input.cn",
            "../examples/8-input-bitonic.cn",
            "../examples/16-input.cn",
        ]
        for input_filename in file_test_cases:
            with self.subTest(inputFilename=input_filename):
                cn = read_comparison_network(input_filename)
                cn.remove(cn[0])
                self.assertFalse(cn.is_sorting_network(False))

        test_cases = [
            "0:1,1:2",
            "0:1,1:3,0:1",
            "0:1,1:3,2:3",
            "0:1,1:3,2:3,0:3",
            "0:2,1:3,0:1,2:3",
        ]
        for s in test_cases:
            with self.subTest(s=s):
                cn = read_comparison_network_from_string(s)
                self.assertFalse(cn.is_sorting_network(False))
