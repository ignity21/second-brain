# MachineLearning 层级重组

Status: Complete

总任务见 `2026-10-22-v2-category-restructure.md`。现状：90 个文件，深度 7，检查脚本 74 条问题；`ML Foundations` 一套索引与内容笔记 `Machine Learning Fundamentals` 的整行链接标题并行，几乎每篇两个父节点。

用户 2026-10-22 确认目标结构、改名，空占位笔记（Anomaly Detection、BFGS、Conjugate Gradient、DBSCAN、Gini Criteria、HCA、L-BFGS、PCA、Recommender System、Reinforcement Learning）保留并挂进树。

目标结构：

```
Machine Learning
├─ ML Foundations
│   ├─ Machine Learning Overview（← Machine Learning Fundamentals 改名）
│   ├─ Supervised Learning → Binary / Multi-class / Multi-label Classification
│   ├─ Unsupervised Learning
│   ├─ Reinforcement Learning, Recommender System
│   └─ Types of Machine Learning Systems（← ML System 改名）
├─ Machine Learning Algorithms
│   ├─ Linear Models and Regression
│   │   ├─ Linear Regression → Normal Equation
│   │   ├─ Polynomial Regression, Logistic Regression, Softmax Regression
│   │   └─ Regularization → Regularized Linear / Logistic Regression, Ridge, Lasso, Elastic Net
│   ├─ Decision Tree → Gini Criteria; Tree Ensembles → Random Forest
│   ├─ K-Nearest Neighbors → K-Neighbors Regression
│   ├─ Neural Network → Activation Functions, Roundoff Errors（改名加上下文）
│   └─ Unsupervised Learning Models → K-Means, DBSCAN, HCA, PCA, Anomaly Detection
├─ Optimization in Machine Learning（← Optimization and Neural Networks 改名）
│   ├─ Cost Function → Loss Function
│   ├─ Gradient Descent → Learning Rate, Early Stopping
│   ├─ Stochastic / Mini-batch Gradient Descent, Adam Algorithm
│   └─ Advanced Optimization → Conjugate Gradient, BFGS, L-BFGS
├─ Features in Machine Learning（← Feature and Model Selection 改名）
│   └─ Feature Engineering, Feature Selection, Feature Scaling, Normalizer
├─ Model Evaluation and Selection（← Model Evaluation 改名）
│   ├─ Classification Metrics, Precision and Recall, Regression Metrics → R-squared
│   ├─ Cross-validation, Hyperparameter Tuning, Evaluating Multiple Models
│   ├─ ML Diagnostic → Bias/Variance, ML Error Analysis
│   └─ Overfitting/Underfitting → Learning Curve
├─ ML Project and Workflow
│   ├─ ML Project → ML Project Checklist, ML Project Example
│   └─ ML Development, Modeling and Predicting, ML Data Sources
└─ ML Libraries and Tools（← Machine Learning Libraries 改名）→ Scikit-Learn, OpenManus
```

撤销（只有导航、无独立内容；均无 ML 外入链）：Machine Learning Concepts、ML Algos、Classification Models、Tree and Ensemble Models、Neighbor-based Models、Neural Network Models、Gradient Descent Algorithms、ML Resources、AI Tools、AI Tools and Resources。

## Checklist

- [x] 用户确认目标结构、改名、空笔记处理
- [x] 撤销 10 个索引 / 枢纽节点，重写根索引与各中间索引
- [x] 内容笔记：整行链接标题只连直接子节点，其余改正文引用；去掉 `- links ::`、自链接、指向祖先的链接
- [x] 互链只留一个方向：Regularization → Overfitting、Learning Curve 归 Overfitting、K-Means → Normalizer
- [x] Supervised Learning 删掉注释掉的 4 个悬空 ID 链接
- [x] 改名与 TOC 更新
- [x] 验证：检查脚本、入链、TOC、行内标记、file 链接、org-roam-db-sync

Result: 深度 7→5，问题 74→24，剩余 24 条均为允许的「笔记兼父节点」（正文引用 Linear Regression、Gradient Descent 等兼作父节点的内容笔记，或这类笔记只有一个子节点）；唯一主父节点，无互链、无指向祖先的引用，无悬空 ID。撤销 10 个导航节点；4 个索引改名并改文件名（`ml_optimization.org`、`ml_features.org`、`model_evaluation_and_selection.org`、`ml_libraries_and_tools.org`）；内容笔记改名 Machine Learning Overview、Types of Machine Learning Systems、Roundoff Errors in Loss Computation，均保留 ID。Overview 的 Math Prerequisites 改为一句正文；ML Project 对 DataScience 索引 Data Cleaning 的引用改为纯文本。Linear Regression、Gradient Descent、Overview 标题数降到 5 个以下，去掉 TOC；Supervised Learning 改用 TOC_2。2026-10-22 用临时 daemon 对真实 DB 执行 `org-roam-db-sync`（293 节点，无悬空 ID 链接）。
