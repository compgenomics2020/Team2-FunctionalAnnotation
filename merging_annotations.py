'''
Script for merging the annotations from various homology and ab-initio tools, into .gff and .faa files.
'''

#!/usr/bin/env python

import subprocess,os,sys

#This function merges the predicted CRISPR repeats to the ncRNA .gff file produced by the Gene Prediction group.

def pilercr_merger(input_directory_path,pilercr_file,output_directory_path):

	#Creating input file path
	input_file=input_directory_path + pilercr_file

	#Creating output file path
	mod_pilercr_file_name=pilercr_file.replace("_crispr",".gff3")
	output_file=output_directory_path+mod_pilercr_file_name

	dict1={}	#Dictionary stores the crispr array details for each contig tested.

	with open(input_file,"r") as inp:
		in_file=inp.readlines()
		line_count=0	#Counter for the lines in input file.
		count=0	#Counter for number of crispr arrays predicted.
		while(line_count<len(in_file)):
			if in_file[line_count].startswith(">")==True:
				in_file[line_count]=in_file[line_count].rstrip()
				header=in_file[line_count].replace(">","")
				count=count+1
				if count not in dict1.keys():
					dict1[count]=header
			if in_file[line_count].startswith("SUMMARY BY SIMILARITY")==True:
				line_count=line_count+6
				count1=0	#Counter to match the number of arrays found to the ones reported in the "Summary by similarity"
				while in_file[line_count].startswith("SUMMARY BY POSITION")!=True:
					if count1<count:
						count1=count1+1
						crisp_array=in_file[line_count].split()
						arr_num=int(crisp_array[0])		
						start_pos=crisp_array[2]
						end_pos=int(start_pos)+int(crisp_array[3])+1
						head=dict1[arr_num]
						dict1[arr_num]=head+"\t"+start_pos+"\t"+str(end_pos)+"\t"+"Copies:"+crisp_array[4]+";Repeat_length:"+crisp_array[5]+";Spacer_Length:"+crisp_array[6]+";Repeat_Consensus:"+crisp_array[8]+"\n"
					line_count=line_count+2		
			 in_file[line_count].startswith("SUMMARY BY POSITION")==True:
				break
			line_count=line_count+1				
	print(dict1)
	with open(output_file,"a+") as op:
		for keys in dict1.keys():
			line_split=dict1[keys].split("\t")
			op.write(line_split[0]+"\t"+"pilercr"+"\t"+"CRISPR array"+"\t"+line_split[1]+"\t"+line_split[2]+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+line_split[3])				

def main():
	inputpath=sys.argv[1]
	outputpath=sys.argv[2]
	files=os.listdir(inputpath)

	#Checking if input files exist in the directory
	if len(files) == 0:
                print("No files present in the directory.")
	for name in files:
		print("Writing file for "+name+"\n")

		#Merging PilerCr results.
		pilercr=pilercr_merger(inputpath,name,outputpath)

if __name__ == "__main__":
	main() 

