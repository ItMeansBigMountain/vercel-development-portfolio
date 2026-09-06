#### we want our models to learn "general rules"
#### overfitting is when the data is memorized too well by the ai model




# ML Pipeline
- Data Ingestion
- Feature Engineering
- Model Selection & Training
- Model Deployment



 
## Data Ingestion
- Gathering the Data Set 
    - API 
    - Spread Sheet
 
    **today divided by yesterdy**
    ```
    df['Asset1'] / df["Asset1"].shift(1)
    ```

    **today subtracted by tomorrow**
    ```
    df['Asset1'] - df["Asset1"].shift(-1)
    ```


## Feature Engineering
- Numerical
- Categorical
- Datetime
- Mixed

- We would like to transform all text columns into numerical representations
    - Label Encoding : Increments columns [i++ 1,2,3,4,5,6,7,8,9...]
    - 



## Model Selection & Training
- pick the right family of models




Convert  all datapoints into numbers


## types of algos
- Clustering
- Regression
- Dimention Reduction
- Classification


### Data Relation to Algo Type
- quatative data --> regression
- catagorized data  --> classification
- probability data  --> clustering
- patterns data ---> dimentionality reduction


#### Binary classification
- true or false / 0 or 1 

#### Multi-Class classification
- features that can have number combonations farther than binary 

#### Regression classification
- persicse data over time





# Confusion Matrix
- Square Chart where each quadrant can help evaluate the prediction score of the train/test ml model
    - Accuracy = (Total Correct / Total Prediction)
    - Precision = True Positives / (True Positive + False Positives)
    - Recall =  True Positives / (True Positive + False Negatives)
    - F1 Score = 2 * (Precision * Recall) / (Precision + Recall)


true positive - outcome where the model correctly predicts the positive class. 
true negative - outcome where the model correctly predicts the negative class.

false positive is an outcome where the model incorrectly predicts the positive class. 
false negative is an outcome where the model incorrectly predicts the negative class.



# ROC 
- curve of Correct guesses (accuracies)
- want most area underneath the curve

    - basically want ROC as a stright line


    - [OverFitting]:
        - ROC is useful as an overfitting check when comparing train vs test
        - If overfitting then ROC is towards the bottom




# Regression
- MAE = mean absolute error
- MAPE - mean absolute percentage error
- MMSE - mean squared error
- RMSE - root mean squared error



### Feature Preformance (classification and regression )
- which feature is pulling most weight




# Model Deployment
- run on local machine
- deploy model to the cloud






# Interperating Data
- you dont want column names to be text
- the reason why is that machine learning uses numbers to find patters and cannot distinguish from strings like it can with integers/floats






# OneHot Encoding
- taking text columns and turning them into numbers
    - the computer needs all titles as numbers to find relations