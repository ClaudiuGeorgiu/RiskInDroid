# RiskInDroid

> A tool for quantitative risk analysis of Android apps based on machine learning techniques.

[![Python version](http://img.shields.io/badge/Python-3.5.2-green.svg)](http://www.python.org/download/releases/3.5.2/)
[![scikit-learn version](http://img.shields.io/badge/scikit--learn-0.18-blue.svg)](http://scikit-learn.org/)

**RiskInDroid** (**Ri**sk **In**dex for An**droid**) is a tool for quantitative risk analysis of Android applications written in Java (used to check the permissions of the apps) and Python (used to compute a risk value based on apps' permissions). The tool uses classification techniques through *scikit-learn*, a machine learning library for Python, in order to generate a numeric risk value between 0 and 100 for a given app. In particular, the following classifiers of *scikit-learn* are used in **RiskInDroid** (this list is chosen after extensive empirical assessments):
* Support Vector Machines (SVM)
* Multinomial Naive Bayes (MNB)
* Gradient Boosting (GB)
* Logistic Regression (LR)

Unlike other tools, **RiskInDroid** doesn't consider only the permissions declared into apps' manifest, but carries out reverse engineering on the apps to retrieve the bytecode and then infers (through static analysis) which permissions are actually used and which not, extracting in this way 4 sets of permissions for every analyzed app:
* Declared permissions - extracted from app's manifest
* Exploited permissions - declared and actually used inside bytecode
* Ghost permissions - not declared but with usages inside bytecode
* Useless permissions - declared but never used inside bytecode

From the above sets of permissions (and considering only the official list of Android permissions), feature vectors (made by `0`s and `1`s) are built and given to the classifiers, which then compute a risk value. The precision and the reliability of **RiskInDroid** are empirically tested on a dataset made of more than 6K malware samples and 112K apps.

Further information can be found in this [paper](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/RiskInDroid_paper.pdf) ([citation](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/DESCRIPTION.md#citation)).

### Demo

If you want to quickly see the tool in action, you can visit [this link](http://46.101.119.244/) where you can browse the full experimental results and calculate the risk of other apps, otherwise continue reading for instructions on how to install it on your own computer. Below you can see a screenshot of **RiskInDroid**:

![Screenshot](screenshot.png)



## Usage

There are two ways of getting a working copy of **RiskInDroid** on your own computer: either by using Docker or by using a Python 3 environment. In both cases, the first thing to do is to get a local copy of this repository, so open up a terminal in the directory where you want to save the project and clone the repository:

```Shell
# This could take quite a lot of time since the repository contains a 25 MB compressed database
$ git clone https://github.com/ClaudiuGeorgiu/RiskInDroid.git
$ cd RiskInDroid
```

#### Using Docker

This is the suggested way of using **RiskInDroid**, since the only requirement is to have Docker installed. Make sure to execute the following commands in the previously created `RiskInDroid` directory (the folder containing the `Dockerfile`):

```Shell
# This will take some time, since a lot of things have to be downloaded
$ docker build -t riskindroid .
$ docker run -p 8080:80 riskindroid
# Now open http://localhost:8080/ in your browser
```

#### Using Python

This method was tested and works on Ubuntu 16.04. Python 3 and Java must be installed on your computer, optionally you can install `p7zip-full` in order to extract the database archive automatically, but this can also be done manually by using any other compatible tool to extract the content of `RiskInDroid/app/database/permission_db.7z` in the `RiskInDroid/app/database` directory. Make sure to execute the following commands in the previously created `RiskInDroid` directory:

```Shell
# If not using virtualenv (https://virtualenv.pypa.io/), skip the next 2 lines
$ virtualenv -p python3 venv
$ source venv/bin/activate

# Install RiskInDroid requirements
$ pip3 install -r requirements.txt

# Run RiskInDroid
$ python3 app/app.py
# Now open http://localhost:5000/ in your browser
```



## Contributing

Questions, bug reports and pull requests are welcome on GitHub at [https://github.com/ClaudiuGeorgiu/RiskInDroid](https://github.com/ClaudiuGeorgiu/RiskInDroid).



## License

With the exception of [PermissionChecker.jar](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/app/PermissionChecker.jar), you are free to use this code under the [MIT License](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/LICENSE).

[PermissionChecker.jar](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/app/PermissionChecker.jar) belongs to [Talos srls](http://www.talos-sec.com/) and you can use it "AS IS" with RiskInDroid, for research purposes only.
