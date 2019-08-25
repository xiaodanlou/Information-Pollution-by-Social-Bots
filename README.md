# Information-Pollution-by-Social-Bots

This repository contains code to reproduce the results in the paper [*Information Pollution by Social Bots*](https://arxiv.org/abs/1907.06130).

## Environment

Our code is based on **Python 2.7**, and you can install the necessary packages by `pip install -r requirements.txt`.

## Usage

- **Simulations**

`bash job_run.sh <n> <p> <human network mode> <infiltration mode>`

- **Calculations**

`bash calc_run.sh <n-th> <p> <human network mode> <infiltration mode>`

- **Plots**

`bash plot_run <p> <human network mode> <infiltration mode>`

***n:*** n-th simulation (integer)

***p:*** random-walk model triadic closure probability for human network (see paper);

***human network mode:*** human network mode (see paper); values are *normal* or *rewire*

***infiltration mode:*** means whether bots connect with humans at random or with preference for hubs; values are *random* or *prefer*

## File descriptions

- **create_human_network.py:** This file is to create a human social network using a directed variant of the random-walk growth model. It also includes the codes of generating a control group network with an additional rewiring mechanism.

- **push_model.py:** This file is  tosimulate the propagation process of meme in social networks.

- **merge.py:** Merge the statistics data from multiple simulations of push model and calculate the average results.

### files in calc_scrips

- **calc_scritps/calc_avg_quality_final_nodescreen.py:** Calculate the average quality of news feeds in human network.

- **calc_scritps/calc_diversity_final_nodescreen.py:**  Calculate the average diversity of news feeds in human network.

- **calc_scritps/calc_kendall.py:** Calculate the kendall \tau of tracked memes.

- **calc_scritps/calc_low_high.py:** Calculate the popularities of memes in high quality and low quality.

- **calc_scritps/calc_bad_meme_sel_distr.py:** Calculate the number of low-quality memes posted by bots and by humans.

### files in plot_scrips

- **plot_scripts/plot_distr_and_heatmap.py:** Plot the distributions and the heatmap of average quality, average diversity and kendall under different params.

- **plot_scripts/plot_bad_meme_sel_distr.py:** Plot the relationship between human and bot sharing of low-quality memes and its exponents

- **plot_scripts/plot_low_and_high_popularity_distr.py:** Plot the popularity distributions of high quality memes and low quality memes under different params.

- **plot_scripts/plot_avg_quality_final_nodescreen_relative.py:** Plot the relative average quality of prefer and random mode under different params.

## Notes

- Our results in this [paper](https://arxiv.org/pdf/1907.06130.pdf) are based on at least 10-times simulations. If you want to get thoses results, you'd better follow the instruction in `job_run.sh` and run it on a cluster environment, since it will consume **huge memory** and **many time**.

- There are exist some params with default value (get same results in the paper) in the scirpts (`job_run.sh`, `calc_run.sh`, `plot_run.sh`), you may need change them if you want to try something else.
