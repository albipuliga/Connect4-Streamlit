import streamlit as st
import pandas as pd

# Assuming you have a dictionary of users and their win counts
users = {
    'user1': 5,
    'user2': 3,
    'user3': 7,
}

def leaderboard(users):
    st.title('Leaderboard')

    # Sort users by win count in descending order
    sorted_users = sorted(users.items(), key=lambda x: x[1], reverse=True)

    # Create a table to display the leaderboard
    table_data = [['Username', 'Wins']]
    for user, wins in sorted_users:
        table_data.append([user, wins])

    # Convert the table data to a pandas DataFrame
    df = pd.DataFrame(table_data[1:], columns=table_data[0])

    # Apply styling to the table
    styles = [
        dict(selector="th", props=[("font-size", "20px"), ("text-align", "center")]),
        dict(selector="td", props=[("font-size", "18px"), ("text-align", "center")]),
        dict(selector="caption", props=[("caption-side", "bottom")])
    ]
    styled_table = df.style.set_table_styles(styles)

    # Display the styled table
    st.write(styled_table)

# Call the function to display the leaderboard
leaderboard(users)