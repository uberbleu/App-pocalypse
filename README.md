# App-pocalypse

## Intro
The Google Play Store is a massive marketplace for Android apps, with millions of applications available for download. App developers are continuously trying to engage users and retain them for as long as possible. 

However, app churn, defined as apps no longer being updated is an issue for the Play Store with lower-quality apps being available for download.
Understanding the factors that contribute to app churn and predicting the likelihood of an app being abandoned can help developers make data-driven decisions to improve their apps and marketing strategies.

Full notebook: https://colab.research.google.com/drive/1F1idziDdlQQxq0SZk5c0iUIYI4PjrQee?usp=sharing

## 1. Problem Definition
In a statement, can we identify the key factors contributing to app churn on the Google Play Store and predict which apps are at risk of being abandoned, to help developers improve retention and app longevity?

## 2. Data
Full data: https://drive.google.com/file/d/1w_rDg_DBWKd_e_A95myluWKqIAec2LE3/view?usp=sharing

## 3. Evaluation
Using Survival Analysis and Cox Proportional Hazards Regression can we identify at least two differences between free and paid apps?

## 4. Features
* App Name: Name of the application.
* Category: The category or genre of the app (e.g., Games, Productivity).
* Rating: Average user rating, typically on a scale from 1 to 5.
* Number of Reviews: Total number of user reviews submitted for the app.
* Size: Size of the app in megabytes (MB).
* Number of Installs: Total number of times the app has been installed.
* Type (Free or Paid): Indicates whether the app is free or paid.
* Price: The cost of the app, if it is paid.
* Content Rating: The age-appropriateness rating for the app (e.g., Everyone, Teen).
* Genres: Specific genres the app falls under (e.g., Action, Puzzle).
* Last Updated: The date the app was last updated.
* Current Version: The current version of the app available.
* Android Version: Minimum required Android version for the app to run.

##  Summary
Cox Proportional Hazards Model:
* After preparing the data (including encoding categorical variables and splitting it into training and testing sets), a Cox Proportional Hazards model was fit to the training data.
* The model provided insights into the factors influencing app churn, allowing for the identification of significant predictors.
* The model was validated using the Concordance Index (C-index), which evaluated the model’s predictive accuracy on the test set.
* The proportional hazards assumption was checked to ensure the model's validity.

## Conclusion
1. Paid apps are more likely to survive (receive updates): The survival analysis shows that paid apps tend to have a longer lifespan in terms of receiving updates compared to free apps.

2. App ratings impact churn: Higher-rated apps are less likely to churn, suggesting that well-rated apps have higher chances of being continuously updated.

3. Significant variables failing the proportional hazards test:
* App Size: This variable showed a non-linear relationship with churn (p-value = 0.0007), indicating that its effect on app churn may not be constant over time. Adjustments such as binning or adding interaction terms are recommended.
* Number of Installs: This variable also failed the proportional hazards assumption (p-value = 0.0048), indicating a complex relationship between the number of installs and churn that requires further exploration.
* App Type (Paid vs. Free): The Type of app (Paid or Free) failed the test (p-value = 0.0093). Further refinement, such as stratifying by app type, is suggested for better model fit.

## Retrospective
## 1. Have we met our goal?
We successfully identified at least two key differences between free and paid apps. Paid apps are more likely to receive updates and have a longer lifespan compared to free apps. 

Additionally, the proportional hazards test showed that app type significantly influences churn, with paid apps being less prone to abandonment.

## 2. What did we learn from our experience?
From this experience, we learned that paid apps generally have better survival rates compared to free apps, as they are updated more frequently. 
We also discovered that factors like app size and the number of installs play a significant role in predicting app churn. 
This analysis highlights the importance of maintaining app updates to retain users and improve app longevity.

## 3. What are some future improvements?
Future improvements to this project could include incorporating more features such as user engagement metrics or developer reputation to better predict app churn. 
Additionally, exploring non-linear relationships and interactions between variables like app size and installs may enhance model accuracy. Finally, testing the model on a larger, more diverse dataset could improve its generalizability across different app categories.
