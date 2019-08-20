#!/bin/bash

if [ "-h" == $1 ];then
    echo "Usage: $0 <n-th run> <p> <human network mode> <bot network mode>"
    echo "human network mode=normal/rewire"
    echo "bot network mode=random/prefer"
    exit 1
fi

if [ $# != 4 ];then
    echo "missing paramaters"
    exit 1
fi

nth=$1
p=$2
n=10000
m=3
h_mode=$3
b_mode=$4

### may need change ###
logs_dir="${mode}/logs_calc"
if [ "$h_mode" = "normal" ]; then
    save_dir="${b_mode}/${p}_result_datas_n${n}"
    networkFile="gmls/directedHighCluster_${n}_${m}_${p}.gml"
    data_dir="${b_mode}/push_model_results_p_${p}_n${n}_${nth}"
elif [ "$h_mode" = "rewire" ]; then
    save_dir="${b_mode}/${p}_result_datas_rewire2_n${n}"
    networkFile="gmls/directedHighCluster_${n}_${m}_${p}_rewire2.gml"
    data_dir="${b_mode}/push_model_results_p_${p}_n${n}_rewire2_${nth}"
else
    echo "error, not support human network mode: $h_mode"
    exit 1
fi
calc_scripts_dir="calc_scripts"
### end need change ###

mkdir -p $logs_dir
mkdir -p $save_dir


echo "calc gml"
echo "---->not rewire2"
python ${calc_scripts_dir}/calc_gml.py $p $nth 0 $data_dir $save_dir > $logs_dir/calc_gml_not_rewire2_${p}_${nth}.log
echo "---->rewire2"
python ${calc_scripts_dir}/calc_gml.py $p $nth 1 $data_dir $save_dir > $logs_dir/calc_diversity_rewire2_${p}_${nth}.log


echo "calc kendall"
echo "may take a while, please wait..."
echo "---->nozero"
python ${calc_scripts_dir}/calc_kendall.py $p $nth nozero $data_dir $save_dir > $logs_dir/calc_kendall_no_zero_${p}_${nth}.log
echo "---->zero"
python ${calc_scripts_dir}/calc_kendall.py $p $nth zero $data_dir $save_dir > $logs_dir/calc_kendall_zero_${p}_${nth}.log


echo "calc low&high"
echo "may take a while, please wait..."
python ${calc_scripts_dir}/calc_low_high.py > $logs_dir/calc_low_high_${p}_${nth}.log


echo "calc avg_quality"
echo "---->nozero"
python ${calc_scripts_dir}/calc_avg_quality_final_nodescreen.py $p $nth normal nozero $data_dir $save_dir > $logs_dir/calc_avg_quality_no_zero_${p}_${nth}.log
echo "---->zero"
python ${calc_scripts_dir}/calc_avg_quality_final_nodescreen.py $p $nth normal zero $data_dir $save_dir > $logs_dir/calc_avg_quality_zero_${p}_${nth}.log


echo "calc diversity"
echo "---->nozero"
python ${calc_scripts_dir}/calc_diversity_final_nodescreen.py $p $nth normal nozero $data_dir $save_dir > $logs_dir/calc_diversity_no_zero_${p}_${nth}.log
echo "---->zero"
python ${calc_scripts_dir}/calc_diversity_final_nodescreen.py $p $nth normal zero $data_dir $save_dir > $logs_dir/calc_diversity_zero_${p}_${nth}.log


echo "calc bad meme dist"
echo "may take a while, please wait..."
python ${calc_scripts_dir}/calc_bad_meme_sel_distr.py $p $nth $data_dir $save_dir > $logs_dir/calc_bad_meme_sel_${p}_${nth}.log
