# Copyright (c) 2024 AuspicesAI
#
# This file is part of ScytheEx.
#
# ScytheEx is free software: you can redistribute it and/or modify
# it under the terms of the Apache License 2.0 as published by
# the Apache Software Foundation, either version 2 of the License, or any later version.
#
# ScytheEx is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# Apache License 2.0 for more details.
#
# You should have received a copy of the Apache License 2.0
# along with ScytheEx. If not, see <http://www.apache.org/licenses/LICENSE-2.0>.

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
import numpy as np


class Plotting:
    def __init__(self, df):
        """
        Initialize the Plotting object with a pandas DataFrame.

        Parameters:
        df (pandas.DataFrame): The DataFrame for which the plots are to be generated.
        """
        self.df = df

    def draw_categorical_plots(self):
        """
        Draws combined plots for all categorical columns in the DataFrame.

        This method generates individual count plots for each categorical column
        and arranges them in a grid layout, with up to three plots per row.

        Returns:
        None: This method displays the plot directly and does not return anything.

        Example Usage:
        >>> df = pd.read_csv("your_dataset.csv")
        >>> plotter = Plotting(df)
        >>> plotter.draw_categorical_plots()
        """
        # Identify categorical columns
        categorical_columns = self.df.select_dtypes(
            include=["object", "category"]
        ).columns

        # Determine the number of rows and columns needed for subplots
        n_cols = 3
        n_rows = math.ceil(len(categorical_columns) / n_cols)

        if len(categorical_columns) == 0:
            print("No categorical columns to plot.")
            return

        # Set up the matplotlib figure
        fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(20, 5 * n_rows))

        # Flatten axes array if more than one row
        if n_rows > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        # Generate plots for each categorical column
        for i, col in enumerate(categorical_columns):
            sns.countplot(x=col, data=self.df, ax=axes[i])
            axes[i].set_title(f"Count Plot for {col}")
            axes[i].set_xlabel("")
            axes[i].set_ylabel("Count")

        # Hide any unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].axis("off")

        plt.tight_layout()
        plt.show()

    def draw_numerical_plots(self):
        """
        Draws combined plots for all numerical columns in the DataFrame.

        This method generates individual histograms for each numerical column
        and arranges them in a grid layout, with up to three plots per row.

        Returns:
        None: This method displays the plot directly and does not return anything.

        Example Usage:
        >>> df = pd.read_csv("your_dataset.csv")
        >>> plotter = Plotting(df)
        >>> plotter.draw_numerical_plots()
        """
        # Identify numerical columns
        numerical_columns = self.df.select_dtypes(include=["number"]).columns

        # Determine the number of rows and columns needed for subplots
        n_cols = 3
        n_rows = math.ceil(len(numerical_columns) / n_cols)

        if len(numerical_columns) == 0:
            print("No numerical columns to plot.")
            return

        # Set up the matplotlib figure
        fig, axes = plt.subplots(nrows=n_rows, ncols=n_cols, figsize=(20, 5 * n_rows))

        # Flatten axes array if more than one row
        if n_rows > 1:
            axes = axes.flatten()
        else:
            axes = [axes]

        # Generate histograms for each numerical column
        for i, col in enumerate(numerical_columns):
            sns.histplot(self.df[col], ax=axes[i], kde=True)
            axes[i].set_title(f"Histogram for {col}")
            axes[i].set_xlabel(col)
            axes[i].set_ylabel("Frequency")

        # Hide any unused subplots
        for j in range(i + 1, len(axes)):
            axes[j].axis("off")

        plt.tight_layout()
        plt.show()

    def plot_algorithm_comparison(self, algorithm_scores):
        """
        Plots a multiclass bar chart comparing different algorithms based on various scores.
        Each algorithm is represented by a different color.

        Parameters:
        - algorithm_scores (dict): A dictionary where keys are algorithm names and values are dictionaries
          containing score names as keys and scores as values.

        Example Usage:
        >>> scores = {
        >>>     'Algorithm1': {'Accuracy': 0.95, 'Precision': 0.90, 'Recall': 0.92},
        >>>     'Algorithm2': {'Accuracy': 0.93, 'Precision': 0.88, 'Recall': 0.91}
        >>> }
        >>> plotter = Plotting()
        >>> plotter.plot_algorithm_comparison(scores)
        """
        # Extract score names
        score_labels = list(next(iter(algorithm_scores.values())).keys())
        algorithms = list(algorithm_scores.keys())

        # Number of bars for each algorithm
        n_bars = len(score_labels)

        # Set up the figure and axes
        fig, ax = plt.subplots(figsize=(10, 6))

        # Create a bar plot for each algorithm
        for i, algorithm in enumerate(algorithms):
            scores = [algorithm_scores[algorithm][score] for score in score_labels]
            ax.bar(
                [x + i * 0.2 for x in range(n_bars)], scores, width=0.2, label=algorithm
            )

        # Set the labels and title
        ax.set_xticks([x + 0.1 for x in range(n_bars)])
        ax.set_xticklabels(score_labels)
        ax.set_ylabel("Scores")
        ax.set_xlabel("Metrics")
        ax.set_title("Algorithm Performance Comparison")
        ax.legend()

        plt.show()


# Example usage
# df = pd.read_csv("your_dataset.csv")
# plotter = Plotting(df)
# plotter.draw_categorical_plots()
