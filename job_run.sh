#!/bin/bash

if [ '-h' == $1 ];then
    echo "usage: $0 <n-th run> <p> <human network mode> <bot network mode>"
    echo "human network mode=normal/rewire"
    echo "bot network mode=random/prefer"
    exit 1
fi

if [ $# != 4 ];then
    echo "missing paramaters"
    exit 1
fi


nth=$1
n=10000
m=3
p=$2
percent_bots=0.1
mu=none
alpha=15
h_mode=$3
b_mode=$4

wire=(0.001 0.005 0.01 0.05 0.1 0.3 0.5 0.8 1.0)
phi=(1 2 3 4 5 6 7 8 9 10)

### need change ###
logs_dir="${b_mode}/logs"
coupled_gmls_dir="${b_mode}/coupled_gmls"
if [ "$h_mode" = "normal" ]; then
    networkFile="gmls/directedHighCluster_${n}_${m}_${p}.gml"
    result_dir="${b_mode}/push_model_results_p${p}_n${n}_${nth}"
elif [ "$h_mode" = "rewire" ]; then
    networkFile="gmls/directedHighCluster_${n}_${m}_${p}_rewire2.gml"
    result_dir="${b_mode}/push_model_results_p${p}_n${n}_rewire2_${nth}"
else
    echo "error, not support human network mode: $h_mode"
    exit 1
fi
### end need change ###

mkdir -p $logs_dir
mkdir -p $result_dir
mkdir -p $coupled_gmls_dir

for w in ${wire[@]}
do
    for h in ${phi[@]}
    do
        echo "start simulate w-$w h-$h, please wait..."
        if [ "$h_mode" = "normal" ]; then
            coupled_gml="${coupled_gmls_dir}/directedHighCluster_${n}_${m}_${p}_${percent_bots}_${w}_${h}_${alpha}_${mu}_coupled.gml"
        elif [ "$h_mode" = "rewire" ]; then
            coupled_gml="${coupled_gmls_dir}/directedHighCluster_${n}_${m}_${p}_${percent_bots}_${w}_${h}_${alpha}_${mu}_coupled_rewire2.gml"
        else
            echo "error, not support human network mode: $h_mode"
            exit 1
        fi

        cat /dev/null > ${logs_dir}/job_n${n}_m${m}_p${p}_per${percent_bots}_wire${w}_phi${h}_alpha${alpha}_mu${mu}.log
        # you can normally run without a cluster environment
        python push_model.py $n $m $p $percent_bots $w $h $alpha $mu $networkFile $coupled_gml $result_dir $b_mode > ${logs_dir}/job_n${n}_m${m}_p${p}_per${percent_bots}_wire${w}_phi${h}_alpha${alpha}_mu${mu}.log
        # comment out this, if you want to save time and happend to have a suitable cluster environment
        # qsub -l nodes=1:ppn=1,vmem=30gb,walltime=10:00:00 -d $PWD -m n -F "$n $m $p $percent_bots $w $h $alpha $mu $networkFile $coupled_gml $result_dir $b_mode" push_model.py -j oe -o ${logs_dir}/job_n${n}_m${m}_p${p}_per${percent_bots}_wire${w}_phi${h}_alpha${alpha}_mu${mu}.log 2>&1 &
        echo "end simulate w-$w h-$h"
    done
done
