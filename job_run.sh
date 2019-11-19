#!/bin/bash

if [ $# != 5 ];then
    echo "Usage: $0 <n-th> <n> <p> <human network mode> <infiltration mode>"
    echo "human network mode=normal/rewire"
    echo "infiltration mode=random/prefer"
    exit 0
fi


nth=$1
n=$2
m=3
p=$3
percent_bots=0.1
mu=none
alpha=15
run_times=5
track_memes_after=10000
max_memes_track=100000
h_mode=$4
i_mode=$5

#wire=(0.001 0.005 0.01 0.05 0.1 0.3 0.5 0.8 1.0)
#phi=(1 2 3 4 5 6 7 8 9 10)
wire=(0.1 0.3 0.5)
phi=(5)

### need change ###
logs_dir="${i_mode}/logs"
coupled_gmls_dir="${i_mode}/coupled_gmls"
if [ "$h_mode" = "normal" ]; then
    networkFile="gmls/directedHighCluster_${n}_${m}_${p}.gml"
    result_dir="${i_mode}/push_model_results_p${p}_n${n}_${nth}"
elif [ "$h_mode" = "rewire" ]; then
    networkFile="gmls/directedHighCluster_${n}_${m}_${p}_rewire.gml"
    result_dir="${i_mode}/push_model_results_p${p}_n${n}_rewire_${nth}"
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
            coupled_gml="${coupled_gmls_dir}/directedHighCluster_${n}_${m}_${p}_${percent_bots}_${w}_${h}_${alpha}_${mu}_coupled_rewire.gml"
        else
            echo "error, not support human network mode: $h_mode"
            exit 1
        fi

        cat /dev/null > ${logs_dir}/job_n${n}_m${m}_p${p}_per${percent_bots}_wire${w}_phi${h}_alpha${alpha}_mu${mu}.log
        # you can normally run without a cluster environment
        # python push_model.py $n $m $p $percent_bots $w $h $alpha $mu $run_times $track_memes_after $max_memes_track $networkFile $coupled_gml $result_dir $i_mode > ${logs_dir}/job_n${n}_m${m}_p${p}_per${percent_bots}_wire${w}_phi${h}_alpha${alpha}_mu${mu}.log
        # comment out this, if you want to save time and happend to have a suitable cluster environment
        qsub -l nodes=1:ppn=1,vmem=30gb,walltime=10:00:00 -d $PWD -m n -F "$n $m $p $percent_bots $w $h $alpha $mu $run_times $track_memes_after $max_memes_track $networkFile $coupled_gml $result_dir $i_mode" push_model.py -j oe -o ${logs_dir}/job_n${n}_m${m}_p${p}_per${percent_bots}_wire${w}_phi${h}_alpha${alpha}_mu${mu}.log 2>&1 &
        echo "end simulate w-$w h-$h"
    done
done
