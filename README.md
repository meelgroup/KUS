# KUS-Sampler
KUS generates Uniform Samples by using a compiled d-DNNF form of a cnf. It expects the d-DNNF to obey the same format as that produced by the [C2D compiler](http://reasoning.cs.ucla.edu/c2d/).

## Installation
```bash
sudo apt-get install graphviz
pip install -r requirements.txt
```
## Running KUS
You can run KUS by using 'KUS.py' Python script. The usage instructions can be found by running
```bash
python KUS.py -h
```
By default, KUS runs with the following set of arguments:
```bash
python KUS.py --outputfile samples.txt --drawtree 0 --samples 10 --useList 0 --randAssign 1 --dDNNF <name of input dDNNF file>
```

## Output Format
The output samples are stored in samples.txt by default. Each line of the output consists of a serial number of the sample followed by a satisfying assignment. The satisfying assignment consists of literals seperated by space. Note that turning random assignment (--randAssign) to 0 can lead to partial assignments in each line. In such cases, the unassigned variables can be chosen to be True or False.

Also, KUS can output a graphical representation of tree for the input NNF. In this tree, the leaves consists of literals and internal nodes can be OR ('O') or AND ('A') nodes as expected for an NNF. However, internal nodes also contain a number seperated by space in our representation. It only serves the purpose of distinguishing between individual OR and AND nodes and has no other meaning.


## Contributors
  * Rahul Gupta (grahul@cse.iitk.ac.in)
  * Shubham Sharma (smsharma@cse.iitk.ac.in)
  * Subhajit Roy (subhajit@iitk.ac.in)
  * Kuldeep Meel (meel@comp.nus.edu.sg)