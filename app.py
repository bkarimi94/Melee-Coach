import os
import tempfile

import streamlit as st

from src.replay_parser import load_replay
from src.match_summary import create_match_summary


st.title("Melee Coach")

st.write(
    "Upload a Slippi replay to view "
    "basic information about the match."
)

uploaded_file = st.file_uploader(
    "Choose a Slippi replay",
    type=["slp"]
)


if uploaded_file is not None:

    temp_path = None

    try:

        with tempfile.NamedTemporaryFile(
            suffix=".slp",
            delete=False
        ) as temp_file:

            temp_file.write(
                uploaded_file.getvalue()
            )

            temp_path = temp_file.name

        game = load_replay(temp_path)

        summary = create_match_summary(game)

        st.success(
            "Replay analyzed successfully!"
        )

        st.subheader("Match Summary")

        st.write(
            f"**Player 1:** "
            f"{summary['player_1_name']} "
            f"({summary['player_1_character']})"
        )

        st.write(
            f"**Player 2:** "
            f"{summary['player_2_name']} "
            f"({summary['player_2_character']})"
        )

        st.write(
            f"**Stage:** "
            f"{summary['stage']}"
        )

        st.write(
            f"**Starting stocks:** "
            f"{summary['starting_stocks']}"
        )

        st.write(
            f"**Timer:** "
            f"{summary['timer_seconds']} seconds"
        )

    except Exception as error:

        st.error(
            f"Unable to analyze replay: {error}"
        )

    finally:

        if (
            temp_path is not None
            and os.path.exists(temp_path)
        ):
            os.remove(temp_path)