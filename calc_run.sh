#!/bin/bash

if [ $# != 5 ];then
    echo "Usage: $0 <n-th> <n> <p> <human network mode> <infiltration mode>"
    echo "human network mode=normal/rewire"
    echo "infiltration mode=random/prefer"
    exit 1
fi


nth=$1
n=$2
m=3
p=$3
percent_bots=0.1
mu=none
alpha=15
run_times=3
h_mode=$4
i_mode=$5
wire="0.001,0.005,0.01,0.05,0.1,0.3,0.5,0.8,1.0"
phi="1.0,2.0,3.0,4.0,5.0,6.0,7.0,8.0,9.0,10.0"

### may need change ###
logs_dir="${i_mode}/logs_calc"
coupled_gmls_dir="${i_mode}/coupled_gmls"
if [ "$h_mode" = "normal" ]; then
    save_dir="${i_mode}/result_datas_p${p}_n${n}"
    data_dir="${i_mode}/push_model_results_p${p}_n${n}_${nth}"
elif [ "$h_mode" = "rewire" ]; then
    save_dir="${i_mode}/result_datas_p${p}_n${n}_rewire"
    data_dir="${i_mode}/push_model_results_p${p}_n${n}_rewire_${nth}"
else
    echo "error, not support human network mode: $h_mode"
    exit 1
fi
calc_scripts_dir="calc_scripts"
### end need change ###

mkdir -p $logs_dir
mkdir -p $save_dir


echo "calc gml"
python ${calc_scripts_dir}/calc_gml.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu $run_times $data_dir $save_dir $coupled_gmls_dir > $logs_dir/calc_gml_${p}_${nth}.log


echo "calc kendall"
echo "may take a while, please wait..."
echo "---->nozero"
python ${calc_scripts_dir}/calc_kendall.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu nozero $data_dir $save_dir > $logs_dir/calc_kendall_no_zero_${p}_${nth}.log
echo "---->zero"
python ${calc_scripts_dir}/calc_kendall.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu zero $data_dir $save_dir > $logs_dir/calc_kendall_zero_${p}_${nth}.log


echo "calc low&high"
echo "may take a while, please wait..."
python ${calc_scripts_dir}/calc_low_high.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu $data_dir $save_dir > $logs_dir/calc_low_high_${p}_${nth}.log


echo "calc avg_quality"
echo "---->nozero"
python ${calc_scripts_dir}/calc_avg_quality_final_nodescreen.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu $run_times normal nozero $data_dir $save_dir > $logs_dir/calc_avg_quality_no_zero_${p}_${nth}.log
echo "---->zero"
python ${calc_scripts_dir}/calc_avg_quality_final_nodescreen.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu $run_times normal zero $data_dir $save_dir > $logs_dir/calc_avg_quality_zero_${p}_${nth}.log


echo "calc diversity"
echo "---->nozero"
python ${calc_scripts_dir}/calc_diversity_final_nodescreen.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu $run_times normal nozero $data_dir $save_dir > $logs_dir/calc_diversity_no_zero_${p}_${nth}.log
echo "---->zero"
python ${calc_scripts_dir}/calc_diversity_final_nodescreen.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu $run_times normal zero $data_dir $save_dir > $logs_dir/calc_diversity_zero_${p}_${nth}.log


echo "calc bad meme dist"
echo "may take a while, please wait..."
python ${calc_scripts_dir}/calc_bad_meme_sel_distr.py $nth $n $m $p $percent_bots $wire $phi $alpha $mu $data_dir $save_dir > $logs_dir/calc_bad_meme_sel_${p}_${nth}.log
