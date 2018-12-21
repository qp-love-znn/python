#!python
#-*-coding:utf-8

import sys
import re
import os

class Pipeline:
	
	def __init__(self):
		pass

	def read_config(self,config):
		opt = {}
		with open(config) as tmp:
			for line in tmp:
				line = line.strip()
				if line.startswith("#"):
					continue
				if line.startswith("threads"):
					nthreads = line.split("=")[1].strip()
					if nthreads:
						opt["threads"] = nthreads
					else :
						opt["threads"] = "4"
						print "warning : you have not set the argument threads"
				if line.startswith("project"):
					project = line.split("=")[1].strip()
					if project :
						opt["project"] = project
					else:
						opt["project"] = "GDRxxxx"
						print "warning : you have not set the Project ID"
				if line.startswith("reference"):
					reference = line.split("=")[1].strip()
					if reference :
						opt["reference"] = reference
					else :
						print "warning : you have not set the reference"
				if line.startswith("species"):
					species = line.split("=")[1].strip()
					if not species :
						print "warning : you have not set the species"
						sys.exit()
					if len(species.split()) > 1 :
						print "error : the species is wrong,For example :Homo sapiens must set as Homo_sapiens"
						sys.exit()
					opt["species"] = species
				if line.startswith("shortname") :
					shortname = line.split("=")[1].strip()
					if shortname :
						opt["shortname"] = shortname
					else :
						print "error : you have not set the shortname"
				if line.startswith("ref_path"):
					ref_path = line.split("=")[1].strip()
					self.check_file(ref_path)
					opt["ref_path"] = ref_path
				if line.startswith("ref_prefix"):
					ref_prefix = line.split("=")[1].strip()
					self.check_file(ref_path+"/"+ref_prefix+".fa")
					self.check_file(ref_path+"/"+ref_prefix+".genepred")
					self.check_file(ref_path+"/"+ref_prefix+".bgl")
					opt["ref_prefix"] = ref_prefix
				if line.startswith("ref_annot"):
					self.ref_annot = line.split("=")[1].strip()
					self.check_file(ref_annot+".annot")
					self.check_file(ref_annot+".kopath")
					self.check_file(ref_annot+".Annot.txt")
					opt["ref_annot"] = ref_annot
				if line.startswith("tran2sym2gene"):
					tran2sym2gene = line.split("=")[1].strip()
					self.check_file(tran2sym2gene)
					opt["tran2sym2gene"] = tran2sym2gene
				if line.startswith("circ_info"):
					circ_info = line.split("=")[1].strip()
					check_file(circ_info)
					opt["circ_info"] = circ_info
				if line.startswith("riboseq"):
					riboseq = line.split("=")[1].strip()
					if riboseq:
						opt["riboseq"] = riboseq
					else :
						print "warning : you have not set the argument riboseq (yes or none)"
		for args in ["threads","project","reference","species","shortname","ref_path","ref_prefix","ref_annot","tran2sym2gene","circ_info","riboseq"] :
			if args not in opt:
				print "error : the argument %s is not found, please check you conf\nexample : conf" % args
				sys.exit()
			else :
				continue
		return opt

	def check_file(self,filename):
		if os.path.exists(filename):
			print "=> %s : OK" % filename
		else:
			print "error : %s is not exist, please check!" % filename
			sys.exit()

import gzip
from itertools import izip			

class Deal_reads():
	def __init__(self):
		pass

	def get_out_reads(self,reads1,reads2,pca,out):
		ty = pca.strip().split(",")
		with gzip.open(reads1,'r') as r1,gzip.open(reads2,'r') as r2,open(out+"_1.fq",'w') as f1,open(out+"_2.fq",'w') as f2:
			arr1 = []
			arr2 = []
			for line1,line2 in izip(r1,r2):
				line1 = line1.strip()
				line2 = line2.strip()
				if line1.startswith("@") and line2.startswith("@"):
					if len(arr1) == 4:
						pp1 = arr1[1][0:8]
						pp2 = arr2[1][0:8]
						re = pp1+"-"+pp2
						pc1 = arr1[1][8:]
						pc2 = arr2[1][8:]
						qua1 = arr1[-1][8:]
						qua2 = arr2[-1][8:]
						if re in ty:
							f1.write(arr1[0]+"\n"+pc1+"\n+\n"+qua1+"\n")
							f2.write(arr2[0]+"\n"+pc2+"\n+\n"+qua2+"\n")
					arr1 = []
					arr2 = []
					arr1.append(line1)
					arr2.append(line2)
				else :
					arr1.append(line1)
					arr2.append(line2)
		os.system("gzip -f %s_1.fq" % out)
		os.system("gzip -f %s_2.fq" % out)
