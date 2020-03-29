'''
Script for creating .gff files from homology results

'''

#!/usr/bin/env python

import subprocess,os,sys

'''
This function reads in the VFDB results

'''
def vfdb(input_file_path):
	
	vfdic={}
	
	#Parsing the VFDB results:
	with open(input_file_path,"r") as vfin:
		for line in vfin:
			col=line.split("\t")
			node=col[0].split()
			vir=col[1]
			if node[0] not in vfdic.keys():
				vfdic[node[0]]=[vir]
	return(vfdic)

'''
This function reads in the CARD results
'''
def card(input_file_path):
	
	cardic={}
	
	#Parsing the CARD results:
	with open(input_file_path,"r") as cardin:
		
		#Skipping the first line
		cardin.readline()
		for line in cardin:
			col=line.split("\t")
			node=col[0].split()
			antbio=col[14]
			mech=col[15]
			amr_gene_family=col[16]
			if node[0] not in cardic.keys():
				cardic[node[0]]=[antbio,mech,amr_gene_family]
	return cardic
'''
This function relates homology results to their clusters
'''
def cluster(cluster_input,dictionary,retype):
	
	#Reading the centroids of each cluster
	centroid=[]
	clustdic={}
	with open(cluster_input,"r") as clustin:
		clust=clustin.readlines()
		line=0
		while(line<len(clust)-1):
			if clust[line].startswith(".")==False:
				line=line+1
				while(clust[line].startswith(".")==True and line<len(clust)-1):
					clust[line]=clust[line].rstrip()
					col=clust[line].split("/")
					node=col[4]
					if node.endswith("...*") ==True:
						name=node.replace("...*","")
						centroid.append(name)
						clustdic[name]=[clust[line]]
					else:
						text=node.split("...")
						clustdic[centroid[-1]].append(clust[line])
					line=line+1

	for key in dictionary.keys():
		if key in clustdic.keys():
			mem=clustdic[key]
			for item in mem:
				node=item.split("/")
				file_name="./tmp/"+node[3]
				out_ext="_"+retype+".gff"
				output_file=file_name.replace(".faa",out_ext)
				col=node[4].split(":")
				name=col[0]
				pos=col[1].split("-")
				start=int(pos[0])-1
				stop=pos[1].split("...")
				list1=dictionary[key]
				details=",".join(list1)
				with open(output_file,"a+") as ot:
					ot.write(name+"\t"+"."+"\t"+"."+"\t"+str(start)+"\t"+stop[0]+"\t"+"."+"\t"+"."+"\t"+"."+"\t"+details+"\n")
					
				
def main():
	vfdb_input=sys.argv[1]
	card_input=sys.argv[2]
	cluster_input=sys.argv[3]
	vf_name="vf"
	card_name="card"
	vfdic=vfdb(vfdb_input)
	cluster(cluster_input,vfdic,vf_name)
	cardic=card(card_input)
	cluster(cluster_input,cardic,card_name)
if __name__ == "__main__":
	main()

