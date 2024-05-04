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
import seaborn as sns
import matplotlib.pyplot as plt
from IPython.display import Markdown, display


class DataSetInformation:
    def __init__(self, df):
        """
        Initialize the DataSetInformation object with a pandas DataFrame.

        Parameters:
        df (pandas.DataFrame): The DataFrame to be summarized.
        """
        self.df = df

    def dataframe_summary(self, col_metadata=None):
        """
        Display a comprehensive summary of the DataFrame.

        This method provides a detailed summary including the shape of the DataFrame,
        information about each column (data types, count of null values), and the
        count of duplicated rows. If provided, descriptions for each column are
        also displayed.

        Parameters:
        col_metadata (dict, optional): A dictionary with column names as keys and
                                       their descriptions as values. If provided,
                                       these descriptions are included in the summary.

        Returns:
        None: This method displays the summary directly and does not return anything.

        Example Usage:
        >>> df = pd.read_csv("your_dataset.csv")
        >>> col_metadata = {
        >>>     'column1': 'Description for column1',
        >>>     'column2': 'Description for column2',
        >>>     # ... other columns
        >>> }
        >>> info = DataSetInformation(df)
        >>> info.dataframe_summary(col_metadata)
        """

        # Helper function to display Markdown text
        def print_md(text):
            display(Markdown(text))

        # Set display options for long descriptions
        pd.set_option("display.max_colwidth", None)

        # Shape of DataFrame
        print_md("### Shape:")
        display(self.df.shape)

        # Column names with data types and null values
        print_md("### Columns and Metadata:")
        columns_df = pd.DataFrame(
            {
                "Data Type": [str(t) for t in self.df.dtypes],
                "Null Values": self.df.isna().sum(),
                "Precentage of Nulls": [
                    "{:.1f}".format(val)
                    for val in ((self.df.isna().sum() / self.df.shape[0]) * 100)
                ],
            }
        )
        if col_metadata:
            columns_df["Description"] = self.df.columns.map(col_metadata).fillna(
                "No description available"
            )

        styled_df = columns_df.style.set_properties(**{"text-align": "left"})
        styled_df.set_table_styles(
            [dict(selector="th", props=[("text-align", "left")])]
        )
        display(styled_df)

        # Reset display options to default (optional)
        pd.reset_option("display.max_colwidth")

        # Sum of duplicated rows
        print_md("### Duplicated Rows:")
        display(
            pd.DataFrame(
                [self.df.duplicated().sum()],
                columns=["Duplicated Rows Count"],
                index=["Total"],
            )
        )

    def categorical_summary(self):
        """
        Display a summary of categorical columns in the DataFrame.

        This method provides:
        - A summary DataFrame with the number of unique values for each categorical column,
          the most frequent value, and its percentage.
        - For columns with fewer than 20 unique values, it displays:
          - A list of unique values.
          - The value counts and percentage distribution for each unique value.

        Returns:
        None: This method displays the summary directly and does not return anything.

        Example Usage:
        >>> df = pd.read_csv("your_dataset.csv")
        >>> info = DataSetInformation(df)
        >>> info.categorical_summary()
        """

        # Helper function to display Markdown text
        def print_md(text):
            display(Markdown(text))

        # Identify categorical columns
        categorical_columns = self.df.select_dtypes(
            include=["object", "category"]
        ).columns

        # Prepare summary data for all categorical columns
        summary_data = []
        for col in categorical_columns:
            unique_count = self.df[col].nunique()
            top_value = self.df[col].value_counts().idxmax()
            top_percentage = (
                self.df[col].value_counts().max() / self.df[col].count()
            ) * 100
            summary_data.append(
                {
                    "Column": col,
                    "Unique Values Count": unique_count,
                    "Top Value": top_value,
                    "Top Value Percentage": f"{top_percentage:.2f}%",
                }
            )

        summary_df = pd.DataFrame(summary_data)

        # Display the summary DataFrame for all categorical columns
        print_md("### Categorical Columns Summary:")
        display(
            summary_df.style.set_properties(**{"text-align": "left"}).set_table_styles(
                [dict(selector="th", props=[("text-align", "left")])]
            )
        )

        # Detailed information for each categorical column with less than 20 unique values
        for col in categorical_columns:
            unique_count = self.df[col].nunique()

            if unique_count < 20:
                print_md(f"### Column: {col}")

                # Display value counts and percentage distribution for each unique value
                print_md("#### Value Counts and Percentage Distribution:")
                value_counts = self.df[col].value_counts().reset_index()
                value_counts.columns = ["Value", "Count"]
                value_counts["Percentage"] = (
                    value_counts["Count"] / value_counts["Count"].sum()
                ) * 100
                display(value_counts.style.set_properties(**{"text-align": "left"}))

                display(Markdown("---"))

    def numerical_summary(self):
        """
        Display a summary of numerical columns in the DataFrame.

        This method provides:
        - A summary DataFrame with statistical measures (mean, median, mode,
          standard deviation, variance, range, minimum, and maximum) for each
          numerical column.
        - A correlation matrix for the numerical columns.
        - A heatmap visualization of the correlation matrix.

        Returns:
        None: This method displays the summary directly and does not return anything.

        Example Usage:
        >>> df = pd.read_csv("your_dataset.csv")
        >>> info = DataSetInformation(df)
        >>> info.numerical_summary()
        """

        # Helper function to display Markdown text
        def print_md(text):
            display(Markdown(text))

        # Identify numerical columns
        numerical_columns = self.df.select_dtypes(include=["number"]).columns

        # Create a DataFrame for statistical summary
        stats_summary = pd.DataFrame()
        for col in numerical_columns:
            stats = {
                "Mean": self.df[col].mean(),
                "Median": self.df[col].median(),
                "Mode": self.df[col].mode()[0],
                "Std Dev": self.df[col].std(),
                "Variance": self.df[col].var(),
                "Range": self.df[col].max() - self.df[col].min(),
                "Min": self.df[col].min(),
                "Max": self.df[col].max(),
            }
            stats_summary[col] = pd.Series(stats)

        # Display the statistical summary DataFrame
        print_md("### Numerical Columns Statistical Summary:")
        display(stats_summary)

        # Correlation Matrix
        correlation_matrix = self.df[numerical_columns].corr()

        # Display the correlation matrix
        print_md("### Correlation Matrix:")
        display(correlation_matrix)

        # Heatmap of the Correlation Matrix
        print_md("### Correlation Matrix Heatmap:")
        plt.figure(figsize=(10, 8))
        sns.heatmap(
            correlation_matrix, annot=True, cmap="coolwarm", fmt=".2f", linewidths=0.5
        )
        plt.show()
