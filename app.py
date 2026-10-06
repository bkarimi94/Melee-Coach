import os
import tempfile

import streamlit as st

from src.analysis.openings import (
    analyze_opk
)
from src.match_summary import (
    create_match_summary
)
from src.replay_parser import (
    load_replay
)


st.title("Melee Coach")

st.write(
    "Upload a Slippi replay to view "
    "match information and gameplay "
    "statistics."
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

            temp_path = (
                temp_file.name
            )

        game = load_replay(
            temp_path,
            skip_frames=False
        )

        summary = create_match_summary(
            game
        )

        player_1_opk = analyze_opk(
            game,
            0
        )

        player_2_opk = analyze_opk(
            game,
            1
        )


        st.success(
            "Replay analyzed successfully!"
        )


        st.subheader(
            "Match Summary"
        )

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


        st.subheader(
            "Openings Per Kill"
        )


        st.write(
            f"### "
            f"{summary['player_1_name']} "
            f"({summary['player_1_character']})"
        )

        st.write(
            f"**Openings:** "
            f"{player_1_opk['openings']}"
        )

        st.write(
            f"**Kills:** "
            f"{player_1_opk['kills']}"
        )

        if player_1_opk["opk"] is None:
            st.write(
                "**Openings Per Kill:** N/A"
            )

            st.info(
                "OPK cannot be calculated "
                "because this player did not "
                "record a kill."
            )

        else:
            st.write(
                "**Openings Per Kill:** "
                f"{player_1_opk['opk']:.2f}"
            )

            st.info(
                f"{summary['player_1_name']} "
                f"required an average of "
                f"{player_1_opk['opk']:.2f} "
                f"openings for each kill."
            )


        st.write("---")


        st.write(
            f"### "
            f"{summary['player_2_name']} "
            f"({summary['player_2_character']})"
        )

        st.write(
            f"**Openings:** "
            f"{player_2_opk['openings']}"
        )

        st.write(
            f"**Kills:** "
            f"{player_2_opk['kills']}"
        )

        if player_2_opk["opk"] is None:
            st.write(
                "**Openings Per Kill:** N/A"
            )

            st.info(
                "OPK cannot be calculated "
                "because this player did not "
                "record a kill."
            )

        else:
            st.write(
                "**Openings Per Kill:** "
                f"{player_2_opk['opk']:.2f}"
            )

            st.info(
                f"{summary['player_2_name']} "
                f"required an average of "
                f"{player_2_opk['opk']:.2f} "
                f"openings for each kill."
            )


    except Exception as error:
        st.error(
            f"Unable to analyze replay: "
            f"{error}"
        )


    finally:
        if (
            temp_path is not None
            and os.path.exists(
                temp_path
            )
        ):
            os.remove(
                temp_path
            )