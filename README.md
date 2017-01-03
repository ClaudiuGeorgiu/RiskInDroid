# RiskInDroid

> A tool for quantitative risk analysis of Android apps based on machine learning techniques.

[![Python version](http://img.shields.io/badge/Python-3.5.2-green.svg)](http://www.python.org/download/releases/3.5.2/)
[![scikit-learn version](http://img.shields.io/badge/scikit--learn-0.18-blue.svg)](http://scikit-learn.org/)

**RiskInDroid** (**Ri**sk **In**dex for An**droid**) is a tool for quantitative risk analysis of Android applications written in Java (used to check the permissions of the apps) and Python (used to compute a risk value based on apps' permissions). The tool uses classification techniques through *scikit-learn*, a machine learning library for Python, in order to generate a numeric risk value between 0 and 100 for a given app. In particular, the following classifiers of *scikit-learn* are used in **RiskInDroid** (this list is chosen after extensive empirical assessments):
* Support Vector Machines (SVM)
* Multinomial Naive Bayes (MNB)
* Gradient Boosting (GB)
* Logistic Regression (LR)

Unlike other tools, **RiskInDroid** doesn't consider only the permissions declared into apps' manifest, but carries out reverse engineering on the apps to retrieve the bytecode and then infers (through static analysis) which permissions are actually used and which not, extracting in this way 4 set of permissions for every analyzed app:
* Declared permissions - extracted from app's manifest
* Exploited permissions - declared and actually used inside bytecode
* Ghost permissions - not declared but with usages inside bytecode
* Useless permissions - declared but never used inside bytecode

From the above sets of permissions and considering only the official list of Android permissions, feature vectors (made by `0`s and `1`s) are built and given to the classifiers, which then compute a risk value. The precision and the reliability of **RiskInDroid** are empirically tested on a dataset made of more than 6K malware samples and 112K apps.



## License

With the exception of [PermissionChecker.jar](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/app/PermissionChecker.jar), you are free to use this code under the [MIT License](https://opensource.org/licenses/MIT).

[PermissionChecker.jar](https://github.com/ClaudiuGeorgiu/RiskInDroid/blob/master/app/PermissionChecker.jar) belongs to [Talos srls](http://www.talos-security.com/) and you can use it "AS IS" with RiskInDroid, for research purposes only.
