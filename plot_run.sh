#!/bin/bash

if [ $# != 4 ];then
    echo "Usage: $0 <n> <p> <human network mode> <infiltration mode>"
    echo "human network mode=normal/rewire"
    echo "infiltration mode=random/prefer"
    exit 1
fi


n=$1
p=$2
h_mode=$3
i_mode=$4

### need change ###
logs_dir="${i_mode}/logs_plot"
if [ "$h_mode" = "normal" ]; then
    save_dir="${i_mode}/result_images_p${p}_n${n}"
    data_dir="${i_mode}/result_datas_p${p}_n${n}"
elif [ "$h_mode" = "rewire" ]; then
    save_dir="${i_mode}/result_images_p${p}_n${n}_rewire"
    data_dir="${i_mode}/result_datas_p${p}_n${n}_rewire"
else
    echo "error, not support human network mode: $h_mode"
    exit 1
fi
plot_scripts_dir="plot_scripts"
### end need change ###

mkdir -p $logs_dir
mkdir -p $save_dir


echo "merge data"
python merge.py "${data_dir}/kendall_datas_no_zero_*.pkl"
python merge.py "${data_dir}/kendall_datas_zero_*.pkl"
python merge.py "${data_dir}/avg_quality_datas_no_zero_*.pkl"
python merge.py "${data_dir}/avg_quality_datas_zero_*.pkl"
python merge.py "${data_dir}/diversity_datas_no_zero_*.pkl"
python merge.py "${data_dir}/diversity_datas_zero_*.pkl"
python merge.py "${data_dir}/bad_meme_selected_datas_*.pkl"
python merge.py "${data_dir}/low_high_datas_*.pkl"


echo "plot low&high distr"
wire="0.001,0.005,0.01"
phi="1,10"
python ${plot_scripts_dir}/plot_low_and_high_popularity_distr.py $wire $phi $data_dir $save_dir > $logs_dir/plot_low_high_${p}.log


echo "plot distr&heatmap"
wire="0.001,0.005,0.01,0.05,0.1,0.3,0.5,0.8,1.0"
phi1="1,5,10"
phi2="1,2,3,4,5,6,7,8,9,10"
echo "---->nozero"
python ${plot_scripts_dir}/plot_distr_and_heatmap.py $wire $phi1 $phi2 $data_dir $save_dir > $logs_dir/plot_heatmap_${p}_normal_nozero.log
echo "---->zero"
python ${plot_scripts_dir}/plot_distr_and_heatmap.py $wire $phi1 $phi2 $data_dir $save_dir > $logs_dir/plot_heatmap_${p}_normal_zero.log


echo "plot bad meme selected distr"
wire="0.5"
phi="1,5,10"
python ${plot_scripts_dir}/plot_bad_meme_sel_distr.py $wire $phi $data_dir $save_dir > $logs_dir/plot_bad_meme_sel_distr_${p}.log


echo "plot relative average quality"
wire="0.001,0.005,0.01,0.05,0.1,0.3,0.5,0.8,1.0"
phi="1,5,10"
echo "---->nozero"
python ${plot_scripts_dir}/plot_avg_quality_final_nodescreen_relative.py $wire $phi nozero $data_dir $save_dir > $logs_dir/plot_bad_meme_sel_distr_${p}_nozero.log
echo "---->zero"
python ${plot_scripts_dir}/plot_avg_quality_final_nodescreen_relative.py $wire $phi zero $data_dir $save_dir > $logs_dir/plot_bad_meme_sel_distr_${p}_zero.log