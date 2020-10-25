# RiskInDroid

> A tool for quantitative risk analysis of Android applications based on machine
> learning techniques.

[![Codacy](https://app.codacy.com/project/badge/Grade/13be50b318c74ac88fba3e13bd620f9c)](https://www.codacy.com/gh/ClaudiuGeorgiu/RiskInDroid)
[![Actions Status](https://github.com/ClaudiuGeorgiu/RiskInDroid/workflows/Build/badge.svg)](https://github.com/ClaudiuGeorgiu/RiskInDroid/actions?query=workflow%3ABuild)
[![Docker Hub](https://img.shields.io/docker/cloud/build/claudiugeorgiu/riskindroid)](https://hub.docker.com/r/claudiugeorgiu/riskindroid)
[![Python Version](https://img.shields.io/badge/Python-3.5%2B-green.svg?logo=python&logoColor=white)](https://www.python.org/downloads/)
[![License](https://img.shields.io/badge/license-MIT-blue.svg)](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/LICENSE)



**RiskInDroid** (**Ri**sk **In**dex for An**droid**) is a tool for quantitative risk
analysis of Android applications written in Java (used to check the permissions of the
apps) and Python (used to compute a risk value based on apps' permissions). The tool
uses classification techniques through *scikit-learn*, a machine learning library for
Python, in order to generate a numeric risk value between 0 and 100 for a given app.
In particular, the following classifiers of *scikit-learn* are used in **RiskInDroid**
(this list is chosen after extensive empirical assessments):
* Support Vector Machines (SVM)
* Multinomial Naive Bayes (MNB)
* Gradient Boosting (GB)
* Logistic Regression (LR)

Unlike other tools, **RiskInDroid** does not take into consideration only the
permissions declared into the app manifest, but carries out reverse engineering on
the apps to retrieve the bytecode and then infers (through static analysis) which
permissions are actually used and which not, extracting in this way 4 sets of
permissions for every analyzed app:
* Declared permissions - extracted from the app manifest
* Exploited permissions - declared and actually used in the bytecode
* Ghost permissions - not declared but with usages in the bytecode
* Useless permissions - declared but never used in the bytecode

From the above sets of permissions (and considering only the official list of Android
permissions), feature vectors (made by `0`s and `1`s) are built and given to the
classifiers, which then compute a risk value. The precision and the reliability of
**RiskInDroid** have been empirically tested on a dataset made of more than 6K malware
samples and 112K apps.

`NOTE:` the data collection and the experiments took place in late 2016.



## ❱ Publication

More details about **RiskInDroid** can be found in the paper
"[RiskInDroid: Machine Learning-based Risk Analysis on Android](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/docs/paper/RiskInDroid.pdf)"
([official pubblication link](https://link.springer.com/chapter/10.1007/978-3-319-58469-0_36)).
You can cite the paper as follows:

> A. Merlo, G.C. Georgiu. "RiskInDroid: Machine Learning-based Risk Analysis on Android",
> in *Proceedings of the 32nd International Conference on ICT Systems Security and
> Privacy Protection* ([IFIP-SEC 2017](http://www.ifipsec.org/)).

```BibTeX
@Inbook{RiskInDroid,
  author="Merlo, Alessio and Georgiu, Gabriel Claudiu",
  editor="De Capitani di Vimercati, Sabrina and Martinelli, Fabio",
  title="RiskInDroid: Machine Learning-Based Risk Analysis on Android",
  bookTitle="ICT Systems Security and Privacy Protection: 32nd IFIP TC 11 International Conference, SEC 2017, Rome, Italy, May 29-31, 2017, Proceedings",
  year="2017",
  publisher="Springer International Publishing",
  pages="538--552",
  isbn="978-3-319-58469-0",
  doi="10.1007/978-3-319-58469-0_36",
  url="https://doi.org/10.1007/978-3-319-58469-0_36"
}
```



## ❱ Demo

You can browse the full experimental results through a web interface and calculate the
risk of new applications (by uploading the `.apk` file). Below you can see a brief
demo of RiskInDroid:

![Web](https://raw.githubusercontent.com/ClaudiuGeorgiu/RiskInDroid/master/docs/demo/web.gif)



## ❱ Installation & Usage

There are two ways of getting a working copy of RiskInDroid on your own computer:
either by [using Docker](#docker-image) or by
[using directly the source code](#from-source) in a `Python 3` environment. In both
cases, the first thing to do is to get a local copy of this repository, so open up a
terminal in the directory where you want to save the project and clone the repository:

```Shell
$ git clone https://github.com/ClaudiuGeorgiu/RiskInDroid.git
```

### Docker image

----------------------------------------------------------------------------------------

#### Prerequisites

This is the suggested way of installing RiskInDroid, since the only requirement
is to have a recent version of Docker installed:

```Shell
$ docker --version             
Docker version 19.03.0, build aeac949
```

#### Official Docker Hub image

The [official RiskInDroid Docker image](https://hub.docker.com/r/claudiugeorgiu/riskindroid)
is available on Docker Hub (automatically built from this repository):

```Shell
$ # Download the Docker image.
$ docker pull claudiugeorgiu/riskindroid
$ # Give it a shorter name.
$ docker tag claudiugeorgiu/riskindroid riskindroid
```

#### Install

If you downloaded the official image from Docker Hub, you are ready to use the tool,
otherwise execute the following command in the previously created `RiskInDroid/`
directory (the folder containing the `Dockerfile`) in order to build the Docker image:

```Shell
$ # Make sure to run the command in RiskInDroid/ directory.
$ # It will take some time to download and install all the dependencies.
$ docker build -t riskindroid .
```

#### Start RiskInDroid

RiskInDroid is now ready to be used, run the following command to start the web
interface of the tool:

```Shell
$ docker run --rm -p 8080:80 riskindroid

$ # Navigate to http://localhost:8080/ to use RiskInDroid.
```

If you need to keep a persistent copy of the uploaded applications, mount
`/var/www/app/upload/` directory from the container to the host (e.g., add
`-v "${PWD}":"/var/www/app/upload/"` parameter to the above command to save
the uploaded applications in the current directory).

### From source

----------------------------------------------------------------------------------------

#### Prerequisites

To use RiskInDroid you need `Python 3` (at least `3.5`), `Java` (at least version `8`)
and a tool to extract the content of `RiskInDroid/app/database/permission_db.7z`
archive (e.g., `p7zip-full` can be used for this task in Ubuntu). Note: although
possible, the installation of some of the Python libraries is not straightforward
on Windows, the usage of a Linux distribution such as Ubuntu is advised.

#### Install

Run the following commands in the main directory of the project (`RiskInDroid/`)
to install the needed dependencies:

```Shell
$ # Make sure to run the commands in RiskInDroid/ directory.

$ # Extract permission_db.db from app/database/permission_db.7z archive and put 
$ # it into app/database/ directory.

$ # The usage of a virtual environment is highly recommended, e.g., virtualenv.
$ # If not using virtualenv (https://virtualenv.pypa.io/), skip the next 2 lines.
$ virtualenv -p python3 venv
$ source venv/bin/activate

$ # Install RiskInDroid's requirements.
$ python3 -m pip install -r requirements.txt
```

#### Start RiskInDroid

RiskInDroid is now ready to be used, run the following command to start the web
interface of the tool:

```Shell
$ # Make sure to run the command in RiskInDroid/ directory.
$ python3 app/app.py

$ # Navigate to http://localhost:5000/ to use RiskInDroid.
```

`NOTE:` the repository already contains the pre-trained models for the used
classifiers, if you want to train the models again (e.g., to use a newer version of
*scikit-learn*) just delete the contents of `app/models/` directory. The models will
be recreated from the source data the next time an application is analyzed.



## ❱ Contributing

Questions, bug reports and pull requests are welcome on GitHub at
[https://github.com/ClaudiuGeorgiu/RiskInDroid](https://github.com/ClaudiuGeorgiu/RiskInDroid).



## ❱ License

With the exception of
[PermissionChecker.jar](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/app/PermissionChecker.jar),
you are free to use this code under the
[MIT License](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/LICENSE).

[PermissionChecker.jar](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/app/PermissionChecker.jar)
belongs to [Talos srls](http://www.talos-sec.com/) and you can use it "AS IS" with
RiskInDroid, for research purposes only.
