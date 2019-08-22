#!/bin/bash

if [ "-h" == $1 ];then
    echo "Usage: $0 <p> <human network mode> <bot network mode>"
    echo "human network mode=normal/rewire"
    echo "bot network mode=random/prefer"
    exit 1
fi

if [ $# != 3 ];then
    echo "missing paramaters"
    exit 1
fi

p=$1
h_mode=$2
b_mode=$3
n=10000

### need change ###
logs_dir="${b_mode}/logs_plot"
if [ "$h_mode" = "normal" ]; then
    save_dir="${b_mode}/result_images_p${p}_n${n}"
    data_dir="${b_mode}/result_datas_p${p}_n${n}"
elif [ "$h_mode" = "rewire" ]; then
    save_dir="${b_mode}/result_images_p${p}_n${n}_rewire2"
    data_dir="${b_mode}/result_datas_p${p}_n${n}_rewire2"
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
python ${plot_scripts_dir}/plot_low_and_high_quality_distr.py $data_dir $save_dir > $logs_dir/plot_low_high_${p}.log


echo "plot distr&heatmap"
echo "---->nozero"
python ${plot_scripts_dir}/plot_distr_and_heatmap.py $data_dir $save_dir > $logs_dir/plot_heatmap_${p}_normal_nozero.log
echo "---->zero"
python ${plot_scripts_dir}/plot_distr_and_heatmap.py $data_dir $save_dir > $logs_dir/plot_heatmap_${p}_normal_zero.log


echo "plot bad meme selected distr"
python ${plot_scripts_dir}/plot_bad_meme_sel_distr.py $data_dir $save_dir > $logs_dir/plot_bad_meme_sel_distr_${p}.log