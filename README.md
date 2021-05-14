# MCC2021
Files to participate in the Model Counting Competition 2021

## Usage
Execute the solver in the directory `./bin` as follows:
```shell
./starexec_run_default <model counting dimacs file>
```

For example:
```shell
./starexec_run_default ../examples/pmc.dimacs
```

The script `bin/ssatABC.py` will convert a model counting instance from MCC2021 to an SSAT formula in sdimacs format and use a precompiled [SSAT solver](https://github.com/NTU-ALComLab/ssatABC) to solve it.
A converted SSAT file is written to `/tmp/` and will be cleaned after the execution.

Type `make` to generate an archive for uploading to StarExec.
