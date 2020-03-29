import csv
from os import listdir
from shutil import copyfile

for na in ['n','a']:
    matching = {}

    for filename in listdir('./input/ku_union_f'+na+'a'):
        if filename[0] == 'C':
            filename = './input/ku_union_f'+na+'a/'+filename
            with open(filename) as fnaa_file:
                for line in fnaa_file:
                    if line[0] == '>':
                        in_matching = line.split()[0]
                        matching[in_matching] = filename

    copyfile('./output/cdhit/f'+na+'a_rep_seq.f'+na+'a',
             './output/cdhit/f'+na+'a_cluster_membership.txt')

    with open('./output/cdhit/f'+na+'a_cluster_membership.txt','r') as clstr:
        c_lines = clstr.readlines()
        w_lines = []

        for c_line in c_lines:
            if c_line[0] == '>':
                c_line = c_line.split()
                w_lines.append(matching[c_line[0]] + '\n')

    with open('./output/cdhit/f'+na+'a_cluster_membership.txt','w') as clstr:
        clstr.writelines(w_lines)
