import os, sys
from test.test_iterlen import len

if __name__ == '__main__':
    parts = len(sys.argv)
    out = sys.argv[1]
    out_strm = open(out,'wb')
    for i in range(2,parts):
        out_strm.write(open(sys.argv[i]).read())
