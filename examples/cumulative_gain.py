from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.datasets import load_breast_cancer as load_data
from sklearn_evaluation.plot import cumulative_gain

# load data
X, y = load_data(return_X_y=True)

# split data into train and test
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=123
)

model = LogisticRegression(random_state=101)
model = model.fit(X_train, y_train)
y_probas = model.predict_proba(X_test)

# plot cumulative gain curve
cumulative_gain(y_test, y_probas)
