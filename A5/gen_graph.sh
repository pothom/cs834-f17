#!/bin/bash

dot initial_graph.dot -Tpng > init.png
for i in {1..5}
do
dot HITS_graph_iter_$i.dot -Tpng > HITS_it$i.png

done

PR=$(ls PR_graph_iter*)
for g in $PR
do 
dot $g -Tpng >${g//dot/png}
done
