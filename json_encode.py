import os.path
import argparse


def proper_encode(fname):
    open(f'{fname}.json',"wb").write(open(fname, "rb").read().decode("unicode_escape").encode("utf8"))


if __name__ == "__main__":
    PARS = argparse.ArgumentParser(description='convert json file')
    PARS.add_argument('jsonfile', help='json fileto be converted')
    PARS.add_argument('--version', action='version', version='2.0')
    ARG = PARS.parse_args()
    if not os.path.isfile(ARG.jsonfile):
        print('No such file : %s' % ARG.jsonfile)
    else:
        proper_encode(ARG.jsonfile)
    
