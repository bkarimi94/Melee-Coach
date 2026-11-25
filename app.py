"""Streamlit interface for Melee Coach replay statistics."""

import os
import tempfile

import pandas as pd
import streamlit as st

from src.batch_analysis import analyze_one_replay, flatten_match_results


@st.cache_data(show_spinner=False)
def analyze_uploaded_file(file_bytes, original_name):
    """Analyze an uploaded replay once and cache the result for UI changes."""
    temp_path = None
    try:
        with tempfile.NamedTemporaryFile(suffix=".slp", delete=False) as temp_file:
            temp_file.write(file_bytes)
            temp_path = temp_file.name
        result = analyze_one_replay(temp_path)
        result["filename"] = original_name
        return result
    finally:
        if temp_path is not None and os.path.exists(temp_path):
            os.remove(temp_path)


def show_player(player):
    """Display three core gameplay metrics and coaching notes for one player."""
    st.markdown(f"#### {player['name']} ({player['character']})")
    opk = player["opk"]
    neutral = player["neutral"]
    damage = player["damage"]
    ratio = neutral["neutral_win_ratio"]
    opk_text = "N/A" if opk["opk"] is None else f"{opk['opk']:.2f}"
    neutral_text = "N/A" if ratio is None else f"{ratio * 100:.1f}%"
    damage_value = damage["average_damage"]
    damage_text = "N/A" if damage_value is None else f"{damage_value:.1f}%"

    col1, col2, col3 = st.columns(3)
    col1.metric("Openings per Kill", opk_text)
    col2.metric("Neutral Win Rate", neutral_text)
    col3.metric("Avg. Damage per Opening", damage_text)
    st.write(f"Openings: {opk['openings']} | Kills: {opk['kills']}")
    st.write(
        f"Neutral Wins: {neutral['neutral_wins']} | "
        f"Neutral Losses: {neutral['neutral_losses']} | "
        f"Counter-attacks: {neutral['counter_attacks']} | "
        f"Trades: {neutral['trades']}"
    )
    st.markdown("**Coaching observations**")
    for note in player["feedback"]:
        st.write(f"- {note}")


def main():
    """Show upload, batch analysis, downloadable data, and per-match details."""
    st.set_page_config(page_title="Melee Coach", page_icon="🎮", layout="wide")
    st.title("Melee Coach")
    st.write(
        "Upload one or more Slippi `.slp` replays to explore gameplay "
        "statistics and simple coaching observations."
    )
    st.caption(
        "Current support: two-player singles. Opening damage is an estimate; "
        "validate classifications against Slippi before relying on them."
    )

    uploaded_files = st.file_uploader(
        "Choose Slippi replay files", type=["slp"], accept_multiple_files=True
    )
    if not uploaded_files:
        st.info("Start by uploading at least one .slp file.")
        return

    matches = []
    with st.spinner("Analyzing replay files..."):
        for uploaded in uploaded_files:
            try:
                matches.append(analyze_uploaded_file(uploaded.getvalue(), uploaded.name))
            except Exception as error:
                st.error(f"Could not analyze {uploaded.name}: {error}")

    if not matches:
        st.warning("No replays could be analyzed.")
        return

    st.success(f"Successfully analyzed {len(matches)} replay(s).")
    rows = flatten_match_results(matches)
    data = pd.DataFrame(rows)

    st.subheader("All Replay Statistics")
    st.dataframe(data, use_container_width=True, hide_index=True)
    st.download_button(
        "Download statistics as CSV",
        data=data.to_csv(index=False).encode("utf-8"),
        file_name="melee_coach_statistics.csv",
        mime="text/csv",
    )

    if len(matches) > 1:
        st.subheader("Progress Across Replays")
        player_names = sorted(data["Player"].dropna().unique().tolist())
        selected_player = st.selectbox("Choose a player", player_names)
        player_rows = data[data["Player"] == selected_player].copy()
        if len(player_rows) > 1:
            player_rows["Replay Number"] = range(1, len(player_rows) + 1)
            st.caption("Replays are shown in the order you uploaded them.")
            st.write("**Neutral Win Rate (%)**")
            st.line_chart(player_rows.set_index("Replay Number")[["Neutral Win Rate (%)"]])
            st.write("**Openings per Kill** (lower generally means fewer openings needed)")
            st.line_chart(player_rows.set_index("Replay Number")[["OPK"]])
        else:
            st.info("Upload multiple replays with the same player name to view a trend.")

    st.subheader("Individual Match Details")
    for match in matches:
        with st.expander(match["filename"], expanded=len(matches) == 1):
            summary = match["summary"]
            st.write(
                f"Stage: **{summary['stage']}** | "
                f"Starting stocks: **{summary['starting_stocks']}** | "
                f"Timer: **{summary['timer_seconds']} seconds**"
            )
            for player in match["players"]:
                show_player(player)
                st.divider()


if __name__ == "__main__":
    main()