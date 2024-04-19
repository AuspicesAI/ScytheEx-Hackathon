import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from sklearn.base import is_classifier, is_regressor


class MachineLearning:
    def __init__(self):
        pass

    def select_best_features(self, X, y, model, feature_selector):
        """
        Evaluates and selects the best features for the given machine learning model,
        based on the performance metric (F1 score for classification or R2 score for regression).

        This method iteratively applies a feature selection strategy to the dataset, fits
        the specified machine learning model, and evaluates its performance. It tracks
        performance metrics for each number of features used and identifies the optimal
        number of features that yield the best performance score. Additionally, it returns
        the names of the best features along with the fitted feature selector for the best model.

        Parameters:
        - X (pd.DataFrame): The input features DataFrame.
        - y (pd.Series): The target variable Series.
        - model (sklearn estimator): An instance of a scikit-learn regression or classification model.
        - feature_selector (function): A function that returns a feature selector object from
          scikit-learn (e.g., SelectKBest). The object must have fit_transform and get_support methods.

        Returns:
        - int: The optimal number of features yielding the best performance score.
        - pd.DataFrame: A DataFrame containing the performance metrics for each number of features.
        - list: The names of the best features selected by the feature selection method.
        - selector: The fitted feature selector object for the best model.

        Note:
        This method should be run before calling any plotting functions, as it generates
        the results required for plotting.

        Example Usage:
        >>> ml = MachineLearning()
        >>> from sklearn.linear_model import LinearRegression
        >>> from sklearn.feature_selection import SelectKBest, f_regression
        >>> model = LinearRegression()
        >>> feature_selector = lambda k: SelectKBest(f_regression, k=k)
        >>> best_features, results, best_feature_names, best_selector = ml.select_best_features(X, y, model, feature_selector)
        >>> print("Best number of features:", best_features)
        >>> print("Best features:", best_feature_names)
        """

        self.model = model  # Save the model instance for later use in plot title
        best_selector = None

        # Lists to store metrics
        if is_classifier(model):
            metrics = ["Accuracy", "Precision", "Recall", "F1 Score"]
        elif is_regressor(model):
            metrics = ["MAE", "MSE", "RMSE", "R2"]
        else:
            raise ValueError("Model must be either a classifier or a regressor.")

        metrics_lists = {metric: [] for metric in metrics}

        best_features_names = None
        best_score = -float("inf")  # Initialize with a very low score

        # Splitting the dataset into training and testing sets
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.3, random_state=0
        )

        # Loop over the features
        for i in range(1, len(X.columns) + 1):
            # Feature selection
            selector = feature_selector(k=i)
            selector.fit(X_train, y_train)
            X_train_selected = selector.transform(X_train)
            X_test_selected = selector.transform(X_test)

            # Model training and prediction
            model.fit(X_train_selected, y_train)
            y_pred = model.predict(X_test_selected)

            if is_classifier(model):
                metrics_lists["Accuracy"].append(accuracy_score(y_test, y_pred))
                metrics_lists["Precision"].append(
                    precision_score(y_test, y_pred, average="weighted", zero_division=0)
                )
                metrics_lists["Recall"].append(
                    recall_score(y_test, y_pred, average="weighted", zero_division=0)
                )
                metrics_lists["F1 Score"].append(
                    f1_score(y_test, y_pred, average="weighted")
                )

            elif is_regressor(model):
                metrics_lists["MAE"].append(mean_absolute_error(y_test, y_pred))
                metrics_lists["MSE"].append(mean_squared_error(y_test, y_pred))
                metrics_lists["RMSE"].append(
                    mean_squared_error(y_test, y_pred, squared=False)
                )
                metrics_lists["R2"].append(r2_score(y_test, y_pred))

            current_metric = metrics_lists["R2" if is_regressor(model) else "Accuracy"][
                -1
            ]

            if current_metric > best_score:
                best_score = current_metric
                best_features_names = X.columns[selector.get_support()]
                best_selector = selector

            # Check if this is the best model so far and save feature names
        results = pd.DataFrame(metrics_lists)
        best_features = (
            results["R2" if is_regressor(model) else "Accuracy"].idxmax() + 1
        )
        self.results = pd.DataFrame(metrics_lists)

        return best_features, results, best_features_names, best_selector

    def plot_accuracy_vs_features(self, save_path=None):
        """
        Plots the model performance (F1 score for classification or R2 score for regression)
        against the number of features used.

        This method should be run after the select_best_features method. It uses the results
        from select_best_features to create the plot.

        Note: The method automatically detects the model type (classification or regression)
        based on the metrics available in the results and plots the relevant metric.

        Parameters:
        - save_path (str, optional): Absolute path to save the plot. If None, the plot
          is not saved to a file.

        Returns:
        None: This method displays the plot directly and does not return anything.

        Example Usage:
        >>> ml = MachineLearning()
        >>> ml.plot_accuracy_vs_features(save_path='/absolute/path/to/save/plot.png')
        """
        if not hasattr(self, "results"):
            print("Please run select_best_features method first.")
            return

        model_name = self.model.__class__.__name__

        if "F1 Score" in self.results.columns:
            metric = "F1 Score"
            title = f"{model_name} F1 Score vs. Number of Features"
        elif "R2" in self.results.columns:
            metric = "R2"
            title = f"{model_name} R2 Score vs. Number of Features"
        else:
            print("No appropriate metric found for plotting.")
            return

        plt.figure(figsize=(10, 6))
        plt.plot(
            range(1, len(self.results) + 1),
            self.results[metric],
            marker="o",
            linestyle="-",
        )
        plt.title(title)
        plt.xlabel("Number of Features")
        plt.ylabel(metric)
        plt.grid(True)

        if save_path:
            plt.savefig(save_path, format="png", bbox_inches="tight")
            print(f"Plot saved to {save_path}")

        plt.show()

    def evaluate_model(self, X, y, test_size, iterations_number, model):
        """
        Evaluates the given model over multiple train-test splits and computes
        average performance metrics, which are different for classifiers and regressors.

        Parameters:
        - X (pd.DataFrame): The input features DataFrame.
        - y (pd.Series): The target variable Series.
        - test_size (float): The proportion of the dataset to include in the test split.
        - iterations_number (int): The number of iterations to repeat the train-test split and evaluation.
        - model (sklearn estimator): An instance of a scikit-learn regression or classification model.

        Returns:
        - dict: Average performance metrics over all iterations, rounded to three decimal places.
        - model: The model fitted in the last iteration.

        Example Usage:
        >>> ml = MachineLearning()
        >>> model = KNeighborsRegressor(n_neighbors=3) # or any classifier
        >>> average_metrics, final_model = ml.evaluate_model(X, y, 0.3, 30, model)
        >>> print(average_metrics)
        """

        metrics_lists = (
            {"MAE": [], "MSE": [], "RMSE": [], "R2": []}
            if is_regressor(model)
            else {"Accuracy": [], "Precision": [], "Recall": [], "F1 Score": []}
        )

        for i in range(iterations_number):
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=test_size, random_state=i
            )

            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)

            if is_regressor(model):
                metrics_lists["MAE"].append(mean_absolute_error(y_test, y_pred))
                metrics_lists["MSE"].append(mean_squared_error(y_test, y_pred))
                metrics_lists["RMSE"].append(
                    mean_squared_error(y_test, y_pred, squared=False)
                )
                metrics_lists["R2"].append(r2_score(y_test, y_pred))
            elif is_classifier(model):
                metrics_lists["Accuracy"].append(accuracy_score(y_test, y_pred))
                metrics_lists["Precision"].append(
                    precision_score(y_test, y_pred, average="weighted", zero_division=0)
                )
                metrics_lists["Recall"].append(
                    recall_score(y_test, y_pred, average="weighted", zero_division=0)
                )
                metrics_lists["F1 Score"].append(
                    f1_score(y_test, y_pred, average="weighted")
                )

            print(f"\r#{i + 1} Iteration is done", end="")
        print()
        # Calculate mean and round off
        average_metrics = {
            metric: round(pd.Series(values).mean(), 3)
            for metric, values in metrics_lists.items()
        }
        self.iteration_metrics = pd.DataFrame(metrics_lists)

        return self.iteration_metrics, average_metrics, model

    def plot_iteration_metrics(self):
        """
        Plots boxplots for the metrics recorded in each iteration by the evaluate_model method.

        Requires that evaluate_model method has been run beforehand to generate iteration metrics.

        Example Usage:
        >>> ml = MachineLearning()
        >>> model = KNeighborsRegressor(n_neighbors=3)
        >>> _, _, iteration_metrics = ml.evaluate_model(X, y, 0.3, 30, model)
        >>> ml.plot_iteration_metrics()
        """
        if not hasattr(self, "iteration_metrics"):
            print("Please run evaluate_model method first.")
            return

        self.iteration_metrics.plot(kind="box", figsize=(10, 6))
        plt.title("Performance Metrics over Iterations")
        plt.ylabel("Score")
        plt.xlabel("Metrics")
        plt.show()
