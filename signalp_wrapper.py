#!/usr/bin/env python3
'''
Wrapper script for SignalP 5.0, an ab-initio tool for detecting signal peptides in bacterial proteomes.

SignalP requires contig fasta files as input. We will be using the contig files generated by the Genome Assembly group.

WARNING: Using "gene" sequences will not give the desired results.
this is an important script
36-96939
'''

import subprocess,os,sys

def signalp_runner(input_directory_path,faa_file,output_directory_path):
        #Creating file path
	input_file=input_directory_path + faa_file

        #Creating a subdirectory in the output directory
        #output_subdir=output_directory_path
	
	#print(output_directory_path + " CREATEDDDDDDDDDDD.")
	
        try:
            print("SignalP 5.0 "+faa_file)
            os.system("signalp -fasta " + input_file + " -org gram- -format short -gff3")
	
	    #cwd = os.getcwd()
            #location_of_files = input_directory_path + "*.gff3" 
	    #subprocess.call("mv %s %s" % (location_of_files, output_directory_path), shell=True)
	    #os.replace("*.gff","output_directory_path")
            #pilercr_output=subprocess.check_output(["pilercr", "-in", input_file, "-out",output_file, "-noinfo", "-quiet"])

        except subprocess.CalledProcessError as err:
            print("Error running SignalP. Check the input files")
            print("Error thrown: "+err.output)
            return False

        print("Completed running SignalP")
        return True
	
	#location_of_files = input_directory_path + "*.gff3" 
	#subprocess.call("mv %s %s" % (location_of_files, output_directory_path), shell=True)
def main():
        inputpath=sys.argv[1] # input directory of files
        outputpath=sys.argv[2] # input subdirectory path to create
        files=os.listdir(inputpath)

        if len(files) == 0:
            print("No files present in the directory.")
        for name in files:
            signalp = signalp_runner(inputpath,name,outputpath) # input_directory_path,faa_file,output_directory_path
            #pilercr=signalp_runner(inputpath,name,outputpath)

if __name__ == "__main__":
        main()
