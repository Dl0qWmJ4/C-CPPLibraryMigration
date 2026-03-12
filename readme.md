# Replication Package for 'Analyzing C/C++ Library Migrations at the Package-level: Targets and Rationals across Seven Package Management Tools'

This is the replication package for our paper *Analyzing C/C++ Library Migrations at the Package-level: Targets and Rationals across Seven Package Management Tools*. It can be used to replicate all four research questions in the paper using our preprocessed and manually labeled data.
We also publicize this package on [Zenodo](https://zenodo.org/records/17571861) for long-term preservation.

## Introduction

Reusing third-party libraries is a common practice in modern software development. However, these libraries sometimes fail to meet a project’s requirements, 
leading developers to replace them with alternative libraries, i.e., *library migration*.
Library migration is a tricky task without straightforward solutions. To mitigate the problem, substantial efforts have been
devoted to understanding the phenomenon and recommending alternative packages, especially for languages providing a **central package hosting platform**, such as Python (PyPI), JavaScript (npm), and Java (Maven). 
Despite the widespread use and critical role of C/C++, especially in operating system (OS) and graphics development, library migration is rarely investigated in the
C/C++ ecosystem where dependency management practices are **fragmented and complicated**. 
The lack of attention to C/C++ hinders the formulation of best practices, methods and tools for effective migration decisions and dependency management in C/C++ projects. This study aims to bridge the gap.

In particular, we ask the following research questions:

- **RQ1:** How common do C/C++ migrations occur?
- **RQ2:** In which domains do C/C++ migrations occur?
- **RQ3:** What is the distribution of C/C++ migration targets chosen by developers?
- **RQ4:** Why do developers conduct C/C++ migrations?

Through the analysis of dependency configuration files from seven representative package management tools used in C/C++ projects and the application of a precise rule-based migration mining algorithm, we have established the first C/C++ library migration dataset, comprising 2,171 migrations and 717 migration rules. By analyzing this dataset (including manual labeling, data analysis, and data visualization), and comparing it with existing migration datasets, we conduct a comparative study on the prevalence, domains, target libraries, and rationales of migrations in C/C++ and three other popular languages with central package hosting platforms. 

All automated processing is implemented using Python in an Anaconda environment, and all manual labeling is conducted using Microsoft Excel. 
We hope the scripts and dataset in this replication package will be useful for further studies in library migration and related fields.

## Replication Package Setup

```shell script
conda create -n CPPLM python=3.10
conda activate CPPLM
python -m pip install -r requirements.txt
conda install -n CPPLM ipykernel --update-deps --force-reinstall
```

Then, activate the CPPLM environment and run `jupyter lab` in the repository folder for replication.

## Dataset Overview


| PMTs         | Projects             |                     |          |        | Dep Changes    | Migrations |           |       |
|:-------------|---------------------:|--------------------:|---------:|------:|----------------:|-----------:|----------:|------:|
|              | Total                | Active Months*      | Commits* | Files* | Commits         | Commits    | Instances | Rules |
| Conan        | 552                  | 27                  | 164      | 107    | 2,200           | 224        | 266       | 104   |
| Vcpkg        | 241                  | 40                  | 343      | 175    | 2,703           | 92         | 96        | 53    |
| Meson        | 500                  | 90                  | 1,348    | 291    | 1,960           | 253        | 279       | 105   |
| Xmake        | 121                  | 26                  | 231      | 158    | 364             | 5          | 6         | 5     |
| Pkg-config   | 29                   | 31                  | 407      | 583    | 81              | 0          | 0         | 0     |
| Gitsubmodule | 11,067               | 48                  | 415      | 161    | 18,927          | 113        | 123       | 86    |
| Deb          | 7,433                | 113                 | 379      | 263    | 18,968          | 1,050      | 1,421     | 364   |
| Total        | 19,943               | 64                  | 408      | 197    | 45,133          | 1,737      | 2,191     | 717   |

* Columns marked with * show medians across projects.

## Replicating Results
After setting up the replication package, you should have a Jupyter Lab server instance running at http://localhost:8888. In Jupyter Lab, you will see the entire Git repository folder, which includes four notebooks: rq1_prevalence.ipynb, rq2_domains.ipynb, rq3_targets.ipynb, and rq4_reasons.ipynb. These notebooks correspond to the four research questions (RQs) in our paper. You can view the plots and numbers used in our paper directly in the cells' output. For each notebook, start a Python kernel and run all cells to replicate the results. The outputs should look identical or similar to the plots in the paper if everything is functioning properly.

Our migration dataset and the existing datasets we use are located in the dataset folder, where each file is named `{language}_migration.csv`. Our manually labeled reasons for C/C++ are in the file `c_reason.csv`. The keywords we used to identify reasons are: "because", "since", "so", "so that", "for", "due to", "thanks to", "reason", "as a result of", "cause", "can", "advantage", "improve", "avoid", "easy", "better", "slow", "faster", "deprecate", "outdate", "old", "new", "out of", and "bug". The file `c_project.csv` contains the number of C/C++ projects for different package management tools for each year and is used to generate plots for RQ1.
