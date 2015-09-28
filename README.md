# sorting-network
Python script to check sorting networks and generate sorting network diagrams

## Usage

```
usage: sortingnetwork.py [-h] [-i inputfile] [-o [outputfile]] [-c] [-s [list]] [--svg [outputfile]]

optional arguments:
  -h, --help                                show this help message and exit
  -i inputfile, --input inputfile           specify a file containing comparison network definition
  -o [outputfile], --output [outputfile]    specify a file for saving the comparison network definition
  -c, --check                               check whether it is a sorting network
  -s [list], --sort [list]                  sorts the list using the input comparison network
  --svg [outputfile]                        generate SVG

```

Comparison networks can be specified like this: `[[0,1],[2,3],[0,2],[1,3],[1,2]]` and can either be loaded from a file using the `--input` argument or if no input file is specified, read from stdin.

Multiple lines can be used as well, to logically group the comparators at each depth. `[[0,1],[2,3],[0,2],[1,3],[1,2]]` is the same as this:
```
[[0,1],[2,3]]
[[0,2],[1,3]]
[[1,2]]
```

## Examples
##### Read a comparison network from a file called example.cn and check whether it is is a sorting network.
```
./sortingnetwork.py --input example.cn --check
```

##### Pipe a comparison network from stdin and check whether it is is a sorting network.
```
echo "[[0,1],[2,3],[0,2],[1,3],[1,2]]" | ./sortingnetwork.py --check
```

##### Read a comparison network from a file called example.cn and generate SVG to stdout.
```
./sortingnetwork.py --input example.cn --svg
```

##### Read a comparison network from a file called example.cn and generate SVG, saved to a file called output.svg.
```
./sortingnetwork.py --input example.cn --svg output.svg
```

##### Pipe the output to rsvg-convert to generate a PNG (or other format) instead of SVG.
(*rsvg-convert can be installed by using `sudo apt-get install librsvg2-bin` on Ubuntu.*)

4-input sorting network:
```
./sortingnetwork.py --input examples/4-input.cn --svg | rsvg-convert > examples/4-input.png
```
![4-Input Sorting Network](https://github.com/brianpursley/sorting-network/blob/master/examples/4-input.png)

5-input sorting network:
```
./sortingnetwork.py --input examples/5-input.cn --svg | rsvg-convert > examples/5-input.png
```
![5-Input Sorting Network](https://github.com/brianpursley/sorting-network/blob/master/examples/5-input.png)

##### Use a specified sorting network to sort a list.

Using a 4-input sorting network to sort a list containing 4 items:
```
./sortingnetwork.py --input examples/4-input.cn --sort [2,4,1,3]
```
Outputs `[1, 2, 3, 4]`

Using a 5-input sorting network to sort a list containing 5 items:
```
./sortingnetwork.py --input examples/5-input.cn --sort [5,2,4,1,3]
```
Outputs `[1, 2, 3, 4, 5]`
