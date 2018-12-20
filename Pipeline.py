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
