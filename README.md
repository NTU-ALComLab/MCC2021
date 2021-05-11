# MCC2021
Files to participate in the Model Counting Competition 2021

## Usage
Execute the solver in the directory `./bin` as follows:
```shell
./starexec_run_default <model counting dimacs file> <converted SSAT sdimacs file> <output file>
```

For example:
```shell
./starexec_run_default ../examples/pmc.dimacs ../pmc.sdimacs ../pmc.log
```

The script `bin/ssatABC.py` will convert a model counting instance from MCC2021 to an SSAT formula in sdimacs format and use a precompiled [SSAT solver](https://github.com/NTU-ALComLab/ssatABC) to solve it.

Type `make` to generate an archive for uploading to StarExec.
