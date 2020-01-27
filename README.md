# Functional Annotation Tools 

## Intuition
We will be dividing functional annotation tools into clustering, homology-based, and ab
initio-based tools.

## TODO
1. Finalize/Add tools for groups defined in "Grouping Software"
2. Start looking at the tools for clustering (limit to 3)
3. Pick tools for cluster
   - CD-HIT (2019)
     - word counting instead of pairwise sequence alignments
     - https://github.com/weizhongli/cdhit
   - SpCLUST 
     - no prior knowledge about input seqs, better at divergent sequences
     - https://github.com/johnymatar/SpCLUST
   - SUMACLUST 
     - pairwise similarities, sort by abundance, clusters similar to CD-HIT
     - reported significantly fewer OTUs and lower alpha diversities than UCLUST (ref 3)
     - https://git.metabarcoding.org/obitools/sumaclust/wikis/home
   - TreeCluster 
     - generates more consistent clusters, improves effectiveness of downstream applications
     - https://github.com/niemasd/TreeCluster
   - UCLUST (2019)
     - threshold similarity score determines cluster membership
     - https://www.drive5.com/usearch/download_academic_site.html

## References
1. A comparison of methods for clustering 16s rrna sequences into otus 
2. SpCLUST: Towards a fast and reliable clustering for potentially divergent biological sequences 
3. Open-Source Sequence Clustering Methods Improve the State Of the Art
