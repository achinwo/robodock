import logging as logger
import sys

#logger.basicConfig(stream=sys.stdout, level=logger.DEBUG)
#
# debug = logger.debug
# error = logger.error
# info = logger.info
# warning = logger.warning
#from pprint import pprint as pp

def pp(format, *args):
    print format % args

debug = pp
error = pp
info = pp
warning = pp