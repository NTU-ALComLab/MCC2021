import subprocess
import re
import sys
import logging
from parser import parse, write_sdimacs, write_result, MCType

# setup logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('[%(levelname)s] %(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)

def run(binary: str, file: str):
    p = subprocess.Popen(
        [binary, "-c", "ssat", file],
        stdout=subprocess.PIPE)
    try:
        out, errs = p.communicate()
        out = out.decode("utf-8").split('\n')
        for l in out:
            res = re.match(".*Satisfying probability\s*\:\s*(\d+\.\d+e-\d+).*", l)
            if res != None:
                return str(res.group(1))

    except subprocess.TimeoutExpired:
        p.kill()
        print("TIMEOUT")
    p.wait()

def print_help():
    print("usage:")
    print("python3 main.py input_file output_file")

if __name__ == "__main__":
    if (len(sys.argv) != 4):
        print_help()
        exit()
    clause_num, var_num, counter_type, clauses, projected, weighted = parse(sys.argv[1])
    write_sdimacs(sys.argv[2], clause_num, var_num, counter_type, clauses, projected, weighted)
    logger.info("Finished converting MCC 2021 format into sdimacs")
    logger.info("Running SSAT solver...")
    prob = run("./abc", "tmp/tmp.sdimacs")
    logger.info("Satisfying probabilty = {}".format(prob))
    if counter_type == MCType.PROJECTED:
        count = (float(prob) * pow(2, (len(projected))))
        write_result(sys.argv[3], count)
    elif counter_type == MCType.WEIGHTED:
        count = prob
        write_result(sys.argv[3], count)
    else:
        count = (float(prob) * pow(2, (var_num)))
        write_result(sys.argv[3], count)



