#!/usr/bin/python
#-*-coding:utf-8-*-

import sys
import re
import os
sys.path.append("/Bio/User/qipeng/python/self_class")
from Pipeline import Deal_reads

if __name__ == "__main__" :
	import sys
	import gzip
	import os
	from itertools import izip
#	from collections import Counter
	if len(sys.argv) != 5 :
		print "Usage : python filter_rawdata.py <reads1> <reads2> <pca><outprefix>\n"
		sys.exit()
	self = Deal_reads()
	self.get_out_reads(sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4])
