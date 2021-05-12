from enum import Enum
import re
import mmap
import logging

# setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)


class MCType(Enum):
    NORMAL = 0
    WEIGHTED = 1
    PROJECTED = 2


def parse(filename: str):
    """
    Parser function for the MCC2021 competiton format

    :param filename str: parsing file's name
    """
    clause_num = -1
    var_num = -1
    counter_type = -1
    projected = []
    weighted = {}
    clauses = []
    with open(filename, "r+b") as infile:
        # use mmap for perfomance boost
        # reference: https://realpython.com/python-mmap
        with mmap.mmap(infile.fileno(), length=0, access=mmap.ACCESS_READ) as mmap_obj:
            lines = mmap_obj.read().decode("utf-8")
            lines = lines.split("\n")
            for line in lines:
                if line == "":
                    continue
                token = re.split("\s|\t", line)
                if len(token) == 0: continue
                if token[0] == "p":
                    # cnf headers: get clause_num and var_num
                    assert clause_num == -1
                    assert var_num == -1
                    var_num = int(token[2])
                    clause_num = int(token[3])
                    logger.info("Number of Var   : {}".format(var_num))
                    logger.info("Number of Clause: {}".format(clause_num))
                elif token[0] == "c":
                    if len(token) == 1: continue
                    if token[1] == "p":
                        # get type specific parameters
                        if token[2] == "weight":
                            counter_type = MCType.WEIGHTED
                            var = int(token[3])
                            weight = float(token[4])
                            weighted[var] = weight
                            if -var in weighted:
                                assert(weighted[var] + weighted[-var] == 1)
                        if token[2] == "show":
                            counter_type = MCType.PROJECTED
                            for i in range(3, len(token)):
                                if token[i] == "0": break
                                projected.append(int(token[i]))
                elif token[0] == "cc":
                    continue
                else:
                    clause = []
                    for t in token:
                        if t == "0":
                            break
                        try:
                            var = int(t)
                        except ValueError:
                            logger.error("Format not supported!")
                            logger.error("Error occur in line: {}".format(line))
                            exit()
                        # var = int(t)
                        if abs(var) > var_num:
                            raise ValueError("Variable in clauses exceed the number of variable given in headers")
                        clause.append(int(t))
                    clauses.append(clause)
            assert(len(clauses) == clause_num)
    projected.sort()
    return clause_num, var_num, counter_type, clauses, projected, weighted

def write_sdimacs(filename: str, clause_num, var_num, counter_type, clauses, projected, weighted):
    with open(filename, mode='w') as f:
        # HACK add one variable to create an exist level in MC or WMC
        if counter_type != MCType.PROJECTED or len(projected) == var_num:
            logger.info("Perform a workaround to create an ER-SSAT")
            f.write("p cnf {} {}\n".format(var_num+1, clause_num))
            f.write("e {} 0\n".format(var_num+1))
        else:
            f.write("p cnf {} {}\n".format(var_num, clause_num))
        if counter_type == MCType.PROJECTED:
            count = 0
            for i in projected:
                f.write("r {} {} 0\n".format(0.5, i))
            for i in range(1, var_num+1):
                if count < len(projected) and projected[count] == i:
                    count = count + 1
                    continue
                f.write("e {} 0\n".format(i))

        else:
            for i in range(1, var_num+1):
                if i in weighted:
                    f.write("r {} {} 0\n".format(weighted[i], i))
                else:
                    f.write("r {} {} 0\n".format(0.5, i))
        for clause in clauses:
            for v in clause:
                f.write("{} ".format(v))
            f.write("0\n")

def write_result(filename: str, res, counter_type):
    with open(filename, mode='w') as f:
        if res == 0:
            logger.info("UNSATISFIABLE!!!")
            f.write("s UNSATISFIABLE\n")
        else:
            logger.info("SATISFIABLE with model count = {}".format(res))
            f.write("s SATISFIABLE\n")
            if counter_type != MCType.WEIGHTED:
                f.write("c s exact arb int {}\n".format(int(res)))
            else:
                f.write("c s exact arb float {}\n".format(float(res)))

if __name__ == "__main__":
    clause_num, var_num, counter_type, clauses, projected, weighted = parse("wmc.cnf")
    write_sdimacs("tmp/tmp.sdimacs", clause_num, var_num, counter_type, clauses, projected, weighted)
