import os
import tempfile

import streamlit as st

from src.analysis.neutral import (
    analyze_neutral,
)

from src.analysis.openings import (
    analyze_opk,
)

from src.feedback import (
    build_player_feedback,
)

from src.match_summary import (
    create_match_summary,
)

from src.replay_parser import (
    load_replay,
)


def display_player_analysis(
    player_name,
    character,
    opk_results,
    neutral_results
):
    """
    Display gameplay statistics and
    descriptive feedback for one player.
    """

    st.write(
        f"### {player_name} "
        f"({character})"
    )

    st.write(
        "**Openings Per Kill**"
    )

    st.write(
        f"**Openings:** "
        f"{opk_results['openings']}"
    )

    st.write(
        f"**Kills:** "
        f"{opk_results['kills']}"
    )

    if opk_results["opk"] is None:
        st.write(
            "**Openings Per Kill:** N/A"
        )

    else:
        st.write(
            "**Openings Per Kill:** "
            f"{opk_results['opk']:.2f}"
        )


    st.write(
        "**Neutral Game**"
    )

    st.write(
        f"**Neutral Wins:** "
        f"{neutral_results['neutral_wins']}"
    )

    st.write(
        f"**Neutral Losses:** "
        f"{neutral_results['neutral_losses']}"
    )

    st.write(
        "**Total Neutral Interactions:** "
        f"{neutral_results['neutral_opportunities']}"
    )

    neutral_win_ratio = (
        neutral_results[
            "neutral_win_ratio"
        ]
    )

    if neutral_win_ratio is None:
        st.write(
            "**Neutral Win Rate:** N/A"
        )

    else:
        neutral_percentage = (
            neutral_win_ratio
            * 100
        )

        st.write(
            "**Neutral Win Rate:** "
            f"{neutral_percentage:.2f}%"
        )


    feedback = (
        build_player_feedback(
            player_name,
            opk_results,
            neutral_results
        )
    )

    st.write(
        "**Analysis Notes:**"
    )

    for message in feedback:
        st.write(
            f"- {message}"
        )


st.title(
    "Melee Coach"
)

st.write(
    "Upload a Slippi replay to view "
    "match information, gameplay "
    "statistics, and analysis."
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

        summary = (
            create_match_summary(
                game
            )
        )


        player_1_opk = (
            analyze_opk(
                game,
                0
            )
        )

        player_2_opk = (
            analyze_opk(
                game,
                1
            )
        )


        player_1_neutral = (
            analyze_neutral(
                game,
                0
            )
        )

        player_2_neutral = (
            analyze_neutral(
                game,
                1
            )
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
            f"{summary['timer_seconds']} "
            f"seconds"
        )


        st.subheader(
            "Gameplay Statistics"
        )


        display_player_analysis(
            summary[
                "player_1_name"
            ],

            summary[
                "player_1_character"
            ],

            player_1_opk,
            player_1_neutral
        )


        st.write(
            "---"
        )


        display_player_analysis(
            summary[
                "player_2_name"
            ],

            summary[
                "player_2_character"
            ],

            player_2_opk,
            player_2_neutral
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