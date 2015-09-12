#!/usr/bin/env python

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

import sys, argparse

class Comparator:
	def __init__(self, input1, input2):		
		self.inputs = []
		self.inputs.append(input1)
		self.inputs.append(input2)
		
	def __str__(self):
		return ":".join(map(str, self.inputs))	
		
	@staticmethod
	def parse(s):
		inputs = map(int, s.split(":"))
		return Comparator(inputs[0], inputs[1])

class ComparisonNetwork:
	def __init__(self):
		self.comparators = []	
		
	def __str__(self):
		return ",".join(map(str, self.comparators))
		
	def append(self, input1, input2):
		self.comparators.append(Comparator(input1, input2))
		
	def sort(self, sequence):
		result = sequence
		for c in self.comparators:
			a = c.inputs[0]
			b = c.inputs[1]
			if (result >> a) & 1 < (result >> b) & 1:
				result = (result - 2**b) | 2**a
		return result
		
	def getMaxInput(self):
		max = 0
		for c in self.comparators:
			if c.inputs[0] > max:
				max= c.inputs[0]
			if c.inputs[1] > max:
				max = c.inputs[1]
		return max
		
	def svg(self):
		scale = 1
		xscale = scale * 30
		yscale = scale * 20
		
		innerResult = ''
		x = xscale
		usedInputs = []
		for c in self.comparators:
			a = c.inputs[0]
			b = c.inputs[1]
			if a in usedInputs or b in usedInputs:
				x += xscale
				del usedInputs[:]
			for ui in usedInputs:
				if (ui > a and ui < b) or (ui > b and ui < a):
					x += xscale / 2
			y0 = yscale + a * yscale
			y1 = yscale + b * yscale
			innerResult += "<circle cx='%s' cy='%s' r='%s' style='stroke:black;stroke-width:1;fill=yellow' />"%(x, y0, 3)
			innerResult += "<line x1='%s' y1='%s' x2='%s' y2='%s' style='stroke:black;stroke-width:%s' />"%(x, y0, x, y1, 1)
			innerResult += "<circle cx='%s' cy='%s' r='%s' style='stroke:black;stroke-width:1;fill=yellow' />"%(x, y1, 3)
			usedInputs.append(a)
			usedInputs.append(b)
		
		w = x + xscale
		n = self.getMaxInput() + 1
		h = (n + 2) * yscale
		result = "<?xml version='1.0' encoding='utf-8'?>"
		result += "<!DOCTYPE svg>"
		result += "<svg width='%spx' height='%spx' xmlns='http://www.w3.org/2000/svg'>"%(w, h)
		for i in range(0, n):
			y = yscale + i * yscale
			result += "<line x1='%s' y1='%s' x2='%s' y2='%s' style='stroke:black;stroke-width:%s' />"%(0, y, w, y, 1)
		result += innerResult
		result += "</svg>"
		return result
		
	@staticmethod
	def parse(s):
		result = ComparisonNetwork()
		result.comparators = map(Comparator.parse, s.split(","))
		return result
	
class SortingNetworkChecker:
	def __init__(self, numberOfInputs):
		self.numberOfInputs = numberOfInputs
		self.sortedSequences = []
		max = 2**numberOfInputs
		for i in range(0, max):
			if self._isSortedSequence(i):
				self.sortedSequences.append(i)	
				
	def _isSortedSequence(self, i):
		last = 1
		original = i
		while i:
			if i & 1:
				if last == 0:
					return False
			elif not i & 1:				
				last = 0
			i >>= 1
		return True
		
	def isSortingNetwork(self, cn):
		max = 2**self.numberOfInputs
		for i in range(0, max):
			if cn.sort(i) not in self.sortedSequences:
				return False 
		return True
		
def readComparisonNetwork(filename):
	if filename:
		f = open(filename, 'r')
		cn = ComparisonNetwork.parse(f.read())
		f.close()
	else:
		cn = ComparisonNetwork.parse(sys.stdin.read())
	return cn
	
def main():
	parser = argparse.ArgumentParser()
	parser.add_argument("-i", "--input", metavar="inputfile", help="specify a file containing comparison network definition")
	parser.add_argument("-c", "--check", action="store_true", help="check whether it is a sorting network")
	parser.add_argument("-s", "--svg", metavar="outputfile", nargs='?', const='', help="generate SVG")
	args = parser.parse_args()
	
	if args.check:
		cn = readComparisonNetwork(args.input)
		checker = SortingNetworkChecker(cn.getMaxInput() + 1)
		print checker.isSortingNetwork(cn)
	
	if args.svg or args.svg == "":
		cn = readComparisonNetwork(args.input)
		if args.svg == "":
			print cn.svg()
		else:
			svg = open(args.svg, "w")
			svg.write(cn.svg())
			svg.close()
		
if __name__ == "__main__":
    main()
