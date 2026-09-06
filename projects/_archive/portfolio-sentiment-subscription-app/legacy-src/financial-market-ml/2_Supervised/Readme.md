## Introduction

This project aims to build a machine learning pipeline for predicting Bitcoin price movements. The pipeline consists of data preprocessing, feature selection, and model evaluation. This README provides a detailed overview of each notebook and the bigger picture of how they work together.

---

## TL;DRs for Each Notebook and the Bigger Picture

### 1-Data-Preprocessing.ipynb
#### TL;DR
- Sets the stage by cleansing and enhancing raw Bitcoin price data. Introduces new features that make the subsequent machine learning tasks more effective.

### 1.5-Optional-Hidden-Markov-Models-Column.ipynb
#### TL;DR
- Optional step that adds a Hidden Markov Model-based column, capturing regime changes in Bitcoin prices. Useful for more nuanced modeling.

### 2-XG-Boost-Feature-Selection.ipynb
#### TL;DR
- Drills down to identify the most impactful features using XGBoost. Sets the stage for focused and efficient machine learning in the next steps.

### 3- XGBOOST-Binary-Classification-Model-Evaluation.ipynb
#### TL;DR
- The final act that brings all pieces together. Utilizes the preprocessed data and selected features to build and rigorously evaluate an XGBoost-based binary classification model.

### Bigger Picture
#### TL;DR
- The notebooks collectively offer a robust machine learning pipeline. From data wrangling in the first notebook to model evaluation in the last, each step is carefully designed to contribute to a reliable predictive model.

---

## 1-Data-Preprocessing.ipynb Overview

### Sections in the Notebook

1. **Data Extraction & Returns Overview**: Loads the initial Bitcoin price data and calculates daily returns.
2. **Feature Engineering - Expansion**: Introduces new features calculated from existing ones to improve model performance.
3. **Indicators**: Adds technical indicators commonly used in financial analysis.
4. **Time Intervals**: Aggregates data over different time intervals (e.g., weekly, monthly).
5. **More on Feature Engineering**: Any additional techniques to refine the dataset.

### Key Notes

| Section                         | Role in AI                                | Value                                            | Benefit                                                      |
|---------------------------------|------------------------------------------|--------------------------------------------------|---------------------------------------------------------------|
| Data Extraction & Returns Overview | Initial dataset setup                   | Foundation for all subsequent steps             | Enables initial data understanding and pre-processing         |
| Feature Engineering - Expansion   | Adds calculated features                | Adds interpretability and potential performance  | Tailors the dataset for better ML performance                 |
| Indicators                        | Adds statistical features               | Encapsulates market behavior                     | Adds depth to the dataset, making it more informative         |
| Time Intervals                    | Time-series adjustments                 | Captures temporal patterns                       | Enables the model to account for time-based trends            |
| More on Feature Engineering       | Further feature manipulations           | Adds complexity and richness to the dataset      | Unveils deeper patterns and relations for the model to learn  |

```python
# Code Snippet for Data Import
import pandas as pd
data = pd.read_csv('BTC-USD.csv')

# Code for Feature Engineering
data['new_feature'] = data['existing_feature'] * 2
```

---

## 2-XG-Boost-Feature-Selection.ipynb Overview

### Sections in the Notebook

1. **Import Preprocessed Data**: Loads the data prepared in the first notebook.
2. **Specify Prediction Target**: Adds a column to serve as the prediction target.
3. **Train-Test Split**: Separates data into training and testing sets for model validation.
4. **Feature Selection Using XGBoost**: Utilizes XGBoost to identify the most important features for the predictive model.

### Key Notes

| Section                  | Role in AI                        | Value                                            | Benefit                                                      |
|--------------------------|----------------------------------|--------------------------------------------------|---------------------------------------------------------------|
| Import Preprocessed Data | Data continuity                  | Consistency across notebooks                     | Ensures that the work in the first notebook is fully leveraged |
| Specify Prediction Target| Goal definition                  | Sets the prediction target for the model         | Directs the model's learning process                          |
| Train-Test Split         | Model validation setup           | Creates training and testing sets                | Enables unbiased model performance evaluation                 |
| Feature Selection Using XGBoost | Feature Importance Evaluation | Identifies impactful features                    | Focuses the model on the most relevant data, improving efficiency |

```python
# Code for Feature Selection
from xgboost import XGBClassifier
model = XGBClassifier()
model.fit(X_train, y_train)

# Code for Train-Test Split
from sklearn.model_selection import train_test_split
X_train, X_test, y_train, y_test = train_test_split(X, y)
```

---

## 3- XGBOOST-Binary-Classification-Model-Evaluation.ipynb Overview

### Sections in the Notebook

1. **Import Libraries and Data**: Sets up the environment and loads the dataset.
2. **

Model Building**: Constructs the XGBoost binary classification model based on preprocessed data and selected features.
3. **Model Evaluation**: Evaluates the model's performance using various metrics like precision, recall, and F1-score.

### Key Notes

| Section                  | Role in AI                        | Value                                            | Benefit                                                      |
|--------------------------|----------------------------------|--------------------------------------------------|---------------------------------------------------------------|
| Import Libraries and Data| Setup                            | Prepares for model building and evaluation       | Sets the stage for subsequent steps                           |
| Model Building           | Model construction               | Actualizes the predictive model                  | Translates the data and feature selection into predictions     |
| Model Evaluation         | Performance assessment           | Quantifies the model's effectiveness             | Provides actionable insights for model refinement             |

```python
# Code for Model Building
model = XGBClassifier(params)
model.fit(X_train, y_train)

# Code for Model Evaluation
from sklearn.metrics import classification_report
print(classification_report(y_test, y_pred))
```

---

## Future Work

- **Automate the Pipeline**: Create a script to run all notebooks in sequence, streamlining the process.
- **Additional Data Sources**: Incorporate additional data like social sentiment or economic indicators.
- **Hyperparameter Tuning**: More extensive hyperparameter tuning for the XGBoost model.
- **Deployment**: Once the model is satisfactory, deploy it to a real-world scenario.

---

## Step-by-Step Guide to Replicate the Work

1. **Data Setup**: Download historical Bitcoin USD data and place it in the `data/` directory.
2. **Run Notebooks in Order**: Start with `1-Data-Preprocessing.ipynb`, followed by `2-XG-Boost-Feature-Selection.ipynb`, and finally `3- XGBOOST-Binary-Classification-Model-Evaluation.ipynb`.
3. **Review and Modify**: Go through each notebook, understand the code, and modify any parameters if necessary.
4. **Execute Scripts**: Optionally, run `stratmanager.py` to execute the pipeline in one go.
5. **Evaluation**: Examine the model performance metrics in the last notebook and refine as needed.

By following these steps, you'll create a robust machine learning model capable of predicting Bitcoin price movements. This README serves as a comprehensive guide to understand and replicate the work even years later.