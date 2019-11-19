#!/bin/bash

if [ $# != 3 ];then
    echo "Usage: $0 <n> <p> <human network mode>"
    echo "human network mode=normal/rewire"
    exit 0
fi


n=$1
p=$2
h_mode=$3
i_mode=$4

### need change ###
logs_dir="relative/logs_plot"
if [ "$h_mode" = "normal" ]; then
    save_dir="relative/result_images_p${p}_n${n}"
    random_data_dir="random/result_datas_p${p}_n${n}"
    prefer_data_dir="prefer/result_datas_p${p}_n${n}"
elif [ "$h_mode" = "rewire" ]; then
    save_dir="relative/result_images_p${p}_n${n}_rewire"
    random_data_dir="random/result_datas_p${p}_n${n}_rewire"
    prefer_data_dir="prefer/result_datas_p${p}_n${n}_rewire"
else
    echo "error, not support human network mode: $h_mode"
    exit 1
fi
plot_scripts_dir="plot_scripts"
### end need change ###

mkdir -p $logs_dir
mkdir -p $save_dir


echo "merge data"
python merge.py "${random_data_dir}/kendall_datas_no_zero_*.pkl"
python merge.py "${random_data_dir}/kendall_datas_zero_*.pkl"
python merge.py "${random_data_dir}/avg_quality_datas_no_zero_*.pkl"
python merge.py "${random_data_dir}/avg_quality_datas_zero_*.pkl"
python merge.py "${random_data_dir}/diversity_datas_no_zero_*.pkl"
python merge.py "${random_data_dir}/diversity_datas_zero_*.pkl"
python merge.py "${random_data_dir}/bad_meme_selected_datas_*.pkl"
python merge.py "${random_data_dir}/low_high_datas_*.pkl"
python merge.py "${random_data_dir}/gini_datas_*.pkl"

python merge.py "${prefer_data_dir}/kendall_datas_no_zero_*.pkl"
python merge.py "${prefer_data_dir}/kendall_datas_zero_*.pkl"
python merge.py "${prefer_data_dir}/avg_quality_datas_no_zero_*.pkl"
python merge.py "${prefer_data_dir}/avg_quality_datas_zero_*.pkl"
python merge.py "${prefer_data_dir}/diversity_datas_no_zero_*.pkl"
python merge.py "${prefer_data_dir}/diversity_datas_zero_*.pkl"
python merge.py "${prefer_data_dir}/bad_meme_selected_datas_*.pkl"
python merge.py "${prefer_data_dir}/low_high_datas_*.pkl"
python merge.py "${prefer_data_dir}/gini_datas_*.pkl"

echo "plot relative average quality"
wire="0.001,0.005,0.01,0.05,0.1,0.3,0.5,0.8,1.0"
phi="1,5,10"
echo "---->nozero"
python ${plot_scripts_dir}/plot_avg_quality_final_nodescreen_relative.py $wire $phi nozero $random_data_dir $prefer_data_dir $save_dir > $logs_dir/plot_bad_meme_sel_distr_${p}_nozero.log
echo "---->zero"
python ${plot_scripts_dir}/plot_avg_quality_final_nodescreen_relative.py $wire $phi zero $random_data_dir $prefer_data_dir $save_dir > $logs_dir/plot_bad_meme_sel_distr_${p}_zero.log
