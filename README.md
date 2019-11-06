# Information-Pollution-by-Social-Bots

This repository contains code to reproduce the results in the paper [*Information Pollution by Social Bots*](https://arxiv.org/abs/1907.06130).

## Environment

Our code is based on **Python 2.7**, and you can install the necessary packages by `pip install -r requirements.txt`.

## Usage

- **Simulations**

`bash job_run.sh <n> <p> <human network mode> <infiltration mode>`

- **Calculations**

`bash calc_run.sh <n> <p> <human network mode> <infiltration mode>`

- **Plots**

`bash plot_run <p> <human network mode> <infiltration mode>`

### Parameters

***n:*** n-th simulation (integer)

***p:*** random-walk model triadic closure probability for human network (see paper);

***human network mode:*** human network mode (see paper); values are *normal* or *rewire*

***infiltration mode:*** means whether bots connect with humans at random or with preference for hubs; values are *random* or *prefer*

## File descriptions

- **create_human_network.py:** This script is to create a human social network using a directed variant of the random-walk growth model. It also includes the code for generating a control group network with an additional rewiring mechanism.

- **push_model.py:** This script is to simulate the meme propagation process in a social networks.

- **merge.py:** Script to merge the statistical data from multiple simulations of the model and calculate the average results.

### Files in calc_scripts

- **calc_scripts/calc_avg_quality_final_nodescreen.py:** Calculate the average quality of news feeds in human network.

- **calc_scripts/calc_diversity_final_nodescreen.py:**  Calculate the average diversity of news feeds in human network.

- **calc_scripts/calc_kendall.py:** Calculate the kendall-tau correlation between popularity and quality of tracked memes.

- **calc_scripts/calc_low_high.py:** Calculate the popularity of high- and low-quality memes.

- **calc_scripts/calc_bad_meme_sel_distr.py:** Calculate the number of low-quality memes posted by bots and humans.

### Files in plot_scripts

- **plot_scripts/plot_distr_and_heatmap.py:** Plot the distributions and the heatmap of average quality, average diversity, and kendall-tau with different parameters.

- **plot_scripts/plot_bad_meme_sel_distr.py:** Plot the relationship between human and bot sharing of low-quality memes and its scaling exponent

- **plot_scripts/plot_low_and_high_popularity_distr.py:** Plot the popularity distributions of high-quality and low-quality memes with different parameters.

- **plot_scripts/plot_avg_quality_final_nodescreen_relative.py:** Plot the relative average quality of preferential and random mode with different parameters.

### Data files

- **2016_apv_distr_integer.txt:** Distribution of scrolling session depth, from [doi:10.1038/s41562-017-0132](http://doi.org/10.1038/s41562-017-0132)

- **twitter_mu_distribution.dat:** Distribution of the mu (retweet ratio) parameter, from [doi:10.1038/s41562-017-0132](http://doi.org/10.1038/s41562-017-0132)

## Notes

- Our results in the paper are based on averages across at least 10 simulation runs. If you want to reproduce thoses results,  follow the instruction in `job_run.sh`. We suggest running the simulations on a cluster environment, since they will need a lot of memory and CPU time. 

- Some parameters in the scirpts (`job_run.sh`, `calc_run.sh`, `plot_run.sh`) have default values to reproduce the results in the paper; you may need change them if you want to explore other scenarios.
