'''
Script for merging the annotations from various homology and ab-initio tools, into .gff and .faa files.

'''

#!/usr/bin/env python

import subprocess,os,sys

'''
This function merges the predicted CRISPR repeats to the ncRNA .gff file produced by the Gene Prediction group.

'''
def pilercr_merger(input_directory_path,pilercr_file,output_directory_path):

	#Creating input file path
	input_file=input_directory_path + pilercr_file

	#Creating output file path
	mod_pilercr_file_name=pilercr_file.replace("_crispr",".gff3")
	output_file=output_directory_path+mod_pilercr_file_name

	dict1={}	#Dictionary stores the crispr array details for each contig tested.

	
	#Parsing the CRISPR input file
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
			if in_file[line_count].startswith("SUMMARY BY POSITION")==True:
				break
			line_count=line_count+1				
	
	
	#Writing to the .gff output files
	with open(output_file,"a+") as op:
		for keys in dict1.keys():
			line_split=dict1[keys].split("\t")
			op.write(line_split[0]+"\t"+"pilercr"+"\t"+"CRISPR array"+"\t"+line_split[1]+"\t"+line_split[2]+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+line_split[3])				


'''
This function merges the predicted Transmembrane proteins to the .faa and .gff files produced by the Gene Prediction group.

'''
def tmhmm_merger(input_directory_path,tmhmm_file,output_directory_path_gff,output_directory_path_faa):
	
	#Creating input file path
	input_file=input_directory_path + tmhmm_file
	csv=input_file.split("_")
	#Creating output file path for .gff file
	mod_tmhmm_file_name=tmhmm_file.replace("tmhmm","union.gff")
	output_file_gff=output_directory_path_gff+mod_tmhmm_file_name
	
	#Creating output file path for .faa file
	mod_tmhmm_file_name=tmhmm_file.replace("tmhmm","union.faa")
	output_file_faa=output_directory_path_faa+mod_tmhmm_file_name
	
	dict_gff={}
	dict_faa={}
	#Parsing the TM protein input file
	with open(input_file,"r") as inp:
		for line in inp:
			line=line.rstrip()
			col=line.split("\t")
			header=col[0]
			pred_hel_split=col[4].split("=")
			pred_hel=pred_hel_split[1]
			top=col[5]
			if int(pred_hel)!=0:
				dict_faa[header]= "Transmembrane Protein: Predicted Helices="+pred_hel+", Topology:"+top
				

	with open("TMHMM_results.csv","a+") as re:
		re.write(input_file+","+str(len(dict_faa))+"\n")			


	#Writing to .faa output files
	with open(output_file_faa,"r") as op:
		faa=op.readlines()
	command="rm "+output_file_faa
	os.system(command)
	line_count=0
	while(line_count<len(faa)):
		if faa[line_count].startswith(">")==True:
			head=faa[line_count].split()
			head[0]=head[0].replace(">","")
			if head[0] in dict_faa.keys():
				with open(output_file_faa,"a+") as wp:
					line=faa[line_count].rstrip()
					wp.write(line+"	"+dict_faa[head[0]]+"\n")
			else:
				with open(output_file_faa,"a+") as wp:
                                        wp.write(faa[line_count])
		else:
			with open(output_file_faa,"a+") as wp:
                                        wp.write(faa[line_count])
		line_count=line_count+1

	#Writing to .gff output files
	with open(output_file_gff,"r") as op:
		gff=op.readlines()
	command="rm " +output_file_gff
	os.system(command)
	line_count=0
	while(line_count<len(gff)):
		col=gff[line_count].split("\t")
		head=col[0].split()
		start=int(col[3])-1
		stop=col[4]
		final_head=head[0]+":"+str(start)+"-"+stop
		
		if final_head in dict_faa.keys():
			line=gff[line_count].rstrip()
			with open(output_file_gff,"a+") as wp:
				wp.write(line+dict_faa[final_head]+"\n")
		else:
			with open(output_file_gff,"a+") as wp:
				wp.write(gff[line_count])
		line_count=line_count+1
				
			
				











def main():
	inputpath=sys.argv[1]
	outputpath_gff=sys.argv[2]
	outputpath_faa=sys.argv[3]
	files=os.listdir(inputpath)

	#Checking if input files exist in the directory
	if len(files) == 0:
                print("No files present in the directory.")
	for name in files:
		print("Writing file for "+name+"\n")
	
		#Merging PilerCr results.
		#pilercr=pilercr_merger(inputpath,name,outputpath)
		
		#Merdging tmhmm results
		tmhmm=tmhmm_merger(inputpath,name,outputpath_gff,outputpath_faa)

if __name__ == "__main__":
	main() 

