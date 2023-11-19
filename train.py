import pandas as pd
from sklearn.model_selection import train_test_split as split
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.svm import SVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.ensemble import AdaBoostClassifier
from sklearn.metrics import accuracy_score
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.metrics import classification_report
import joblib

def run_model(model, alg_name):
   # build the model on training data
   model.fit(X_train, y_train)
 
   # make predictions for test data
   y_pred = model.predict(X_test)
   # calculate the accuracy score
   accuracy =  accuracy_score(y_test, y_pred)
   cm = confusion_matrix(y_test, y_pred)
   scoresDT3 = cross_val_score(model, X_test, y_test, cv=6)
   Cr = classification_report(y_test, y_pred)
   results.append((alg_name, accuracy, model))
   print("Model: ", alg_name)
   print("Accuracy on Test Set for {} = {:.2f}\n".format(alg_name,accuracy))
   print(Cr)
   print("{}: CrossVal Accuracy Mean: {:.2f} and Standard Deviation: {:.2f} \n".format(alg_name,scoresDT3.mean(), scoresDT3.std()))
   joblib.dump(model, "./streamlit_app/model.pkl")


if __name__=="__main__":
   df = pd.read_csv('new_data.csv')
   data = df.copy()
   y = data['popularity_level']
   X = data.drop(columns=['popularity','popularity_level'])
   X_train, X_test, y_train, y_test = split(X, y, test_size = 0.25, random_state = 42)

   results = []
   """
   model = DecisionTreeClassifier()
   run_model(model, "Decision Tree")

   model = SVC(kernel='poly', degree=3, C=1)
   run_model(model, "SVM Classifier")

   model = KNeighborsClassifier()
   run_model(model, "Nearest Neighbors Classifier")

   model = LogisticRegression(multi_class='multinomial' , solver='lbfgs', max_iter=100)
   run_model(model, "Logistic Regression")

   dt_b = DecisionTreeClassifier(max_depth=1, random_state=42)
   model = AdaBoostClassifier(base_estimator=dt_b)
   run_model(model, "Adaboost Classifier")
   """
   model = RandomForestClassifier(n_estimators=10)
   run_model(model, "Random Forest")
