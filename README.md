# Information-Pollution-by-Social-Bots

Information-Pollution-by-Social-Bots is the code for paper [Information Pollution by Social Bots](https://arxiv.org/pdf/1907.06130.pdf).

## Environment

Our code is based on **Python 2.7**, and you can install the necessary packages by `pip install -r requirements.txt`.

## Usage

- Simulate

```bash
./job_run.sh <n-th> <p> <human network mode> <bot network mode>
```

- Calculate

```bash
./calc_run.sh <n-th> <p> <human network mode> <bot network mode>
```

- Plot

```bash
./plot_run <p> <human network mode> <bot network mode>
```

**n-th:** *1, 2, ..., n*, means n-th simulation

**p:** *0.0, 0.5, 1.0*, means human network trial probabilty

**human network mode:** *normal/rewire*, means human network mode

**bot network mode:** *random/prefer*, means bot network mode

## Attention

- Our results in this [paper](https://arxiv.org/pdf/1907.06130.pdf) are based on at least 6-times simulations. If you want to get thoses results, you'd better follow the instruction in `job_run.sh` and run it on a cluster environment, since it will consume **huge memory** and **many time**.

- There are exist some params with default value (get same results in the paper) in the scirpts, you may need change them if you want to try something else.
