from sklearn import datasets
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from sklearn_evaluation import plot

# generate data
X, y = datasets.make_classification(
    n_samples=2000, n_features=6, n_informative=4, class_sep=0.1
)

# split data into train and test
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

est = RandomForestClassifier()
est.fit(X_train, y_train)

# y_pred = est.predict(X_test)
y_score = est.predict_proba(X_test)
y_true = y_test

# plot precision recall curve
pr = plot.PrecisionRecall.from_raw_data(y_true, y_score)
