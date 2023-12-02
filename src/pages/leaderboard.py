import streamlit as st


def leaderboard(users):
    # Apply styling to the table
    styles = [
        dict(selector="th", props=[("font-size", "20px"), ("text-align", "center")]),
        dict(selector="td", props=[("font-size", "18px"), ("text-align", "center")]),
        dict(selector="caption", props=[("caption-side", "bottom")]),
    ]
    styled_table = users.style.set_table_styles(styles)
    st.write(styled_table)


leaderboard(st.session_state.users_df)
