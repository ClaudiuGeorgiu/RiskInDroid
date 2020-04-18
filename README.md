# RiskInDroid

> A tool for quantitative risk analysis of Android apps based on machine
> learning techniques.

[![Codacy](https://api.codacy.com/project/badge/Grade/13be50b318c74ac88fba3e13bd620f9c)](https://www.codacy.com/app/ClaudiuGeorgiu/RiskInDroid)
[![Python version](http://img.shields.io/badge/Python-3.5.2-green.svg)](http://www.python.org/download/releases/3.5.2/)
[![scikit-learn version](http://img.shields.io/badge/scikit--learn-0.18-blue.svg)](http://scikit-learn.org/)



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



## ❱ Publication

More details about **RiskInDroid** can be found in the paper
"[RiskInDroid: Machine Learning-based Risk Analysis on Android](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/RiskInDroid_paper.pdf)"
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

If you want to quickly see the tool in action, visit
[https://www.riskindroid.com](https://www.riskindroid.com) to browse the full
experimental results and calculate the risk of other apps, otherwise continue reading
for instructions on how to install it on your own computer. Below you can see a
screenshot of the live demo of RiskInDroid:

![Screenshot](https://raw.githubusercontent.com/ClaudiuGeorgiu/RiskInDroid/master/screenshot.png)



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
otherwise execute the following commands in the previously created `RiskInDroid/`
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

The live demo at [https://www.riskindroid.com](https://www.riskindroid.com) is also a
Docker container deployed with the following command:

```Shell
$ docker run \
    -d --restart=always \
    -p 80:80 -p 443:443 \
    -v "${PWD}/app/upload":/var/www/app/upload/ \
    riskindroid
```

### From source

----------------------------------------------------------------------------------------

#### Prerequisites

To use RiskInDroid you need `Python 3` (at least `3.5`), `Java 8` and a tool to extract
the content of `RiskInDroid/app/database/permission_db.7z` archive (e.g., `p7zip-full`
can be used for this task in Ubuntu). Note: although possible, the installation of some
of the Python libraries is not straightforward on Windows, the usage of a Linux
distribution such as Ubuntu is advised.

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
