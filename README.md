# KUS-Sampler
KUS generates uniform samples by using a compiled deterministic decomposable negation normal form (d-DNNF) of a CNF. It expects the d-DNNF in the same format as that produced by the [C2D compiler](http://reasoning.cs.ucla.edu/c2d/) and CNF in the DIMACS format.

## Installation
```bash
sudo apt-get install graphviz
pip install -r requirements.txt
```
For now, [D4 compiler](http://www.cril.univ-artois.fr/KC/d4.html) is included as default for compiling CNF to d-DNNF. Any other compiler can be easily used with slight modifications.

## Running KUS
You can run KUS by using 'KUS.py' Python script. A simple invocation looks as follows:
```bash
python KUS.py <cnffile>
```
The usage instructions and default values to arguments can be found by running
```bash
python KUS.py -h
```

## Output Format
The output samples are stored in samples.txt by default. Each line of the output consists of a serial number of the sample followed by a satisfying assignment. The satisfying assignment consists of literals seperated by space. Note that turning random assignment (--randAssign) to 0 can lead to partial assignments in each line. In such cases, the unassigned variables can be chosen to be True or False.

Also, KUS can output a graphical representation of tree for the input NNF. In this tree, the leaves consists of literals and internal nodes can be OR ('O') or AND ('A') nodes as expected for an NNF. However, internal nodes also contain 2 numbers seperated by space in our representation. This second one gives the annotation. The first one, only serves the purpose of distinguishing between individual OR and AND nodes and has no other meaning.


## Contributors
  * Rahul Gupta (grahul@cse.iitk.ac.in)
  * Shubham Sharma (smsharma@cse.iitk.ac.in)
  * Subhajit Roy (subhajit@iitk.ac.in)
  * Kuldeep Meel (meel@comp.nus.edu.sg)


<!-- If you use our tool, please cite us using the following bibtex:
```
@inproceedings{SGRM18,
	author={Sharma, Shubham and  Gupta, Rahul and  Roy, Subhajit and Meel, Kuldeep S.},
	title={Knowledge Compilation meets Uniform Sampling},
	year={2018},
	booktitle={Proceedings at International Conference on Logic for Programming, Artificial Intelligence and Reasoning},
	month={09},
	abstract={Uniform sampling has drawn diverse applications in programming languages and software engineering, like in constrained-random verification (CRV), constrained-fuzzing and bug synthesis. The effectiveness of these applications depend on the uniformity of test stimuli generated from a given set of constraints. Despite significant progress over the past few years, the performance of the state of the art techniques still falls short of those of heuristic methods employed in the industry which sacrifice either uniformity or scalability when generating stimuli. In this paper, we propose a new approach to the uniform generation that builds on recent progress in knowledge compilation. The primary contribution of this paper is marrying knowledge compilation with uniform sampling: our algorithm, KUS, employs the state-of-the-art knowledge compilers to first compile constraints into d-DNNF form, and then, generates samples by making two passes over the compiled representation. },
}

``` -->