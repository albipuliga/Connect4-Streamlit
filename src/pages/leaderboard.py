import streamlit as st

"""
Python Dictionaries:
    Accessing and setting a value: O(1) on average. Python dictionaries are implemented as hash tables, which allow for fast access and assignment.
    Deleting an element: O(1) on average.
    Checking if a key is in the dictionary: O(1) on average.

Pandas DataFrames:
    Accessing a value: O(1) if you're accessing by label using loc or at.
    Setting a value: O(1) if you're setting by label using loc or at.
    Deleting a row or column: O(n) where n is the number of rows or columns respectively. This is because pandas has to create a new DataFrame with the row or column removed.
    Searching for a value: O(n) where n is the number of elements in the DataFrame.
"""

def leaderboard(users):
    """
    Display a leaderboard table with styled formatting.

    Parameters:
        users (pandas.DataFrame): The DataFrame containing user data.

    Returns:
        None
    """
    # Apply styling to the table
    styles = [
        dict(selector="th", props=[("font-size", "20px"), ("text-align", "center")]),
        dict(selector="td", props=[("font-size", "18px"), ("text-align", "center")]),
        dict(selector="caption", props=[("caption-side", "bottom")]),
    ]
    styled_table = users.style.set_table_styles(styles)
    st.write(styled_table)


leaderboard(st.session_state.users_df)
