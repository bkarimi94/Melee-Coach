# Melee Coach

Melee Coach is a gameplay analysis application for *Super Smash Bros. Melee* that uses Slippi replay files to analyze player performance and provide feedback on areas for improvement.

The program will read `.slp` replay files, extract gameplay information, calculate useful statistics, and generate recommendations based on measurable gameplay patterns. The project will initially focus on general gameplay analysis and a limited amount of character-specific feedback.

## Project Goals

* Import and parse Slippi `.slp` replay files
* Extract basic match information such as players, characters, stage, and game duration
* Calculate useful gameplay statistics
* Identify measurable gameplay habits and areas for improvement
* Generate rule-based coaching feedback
* Provide character-specific analysis for selected characters
* Display results through a simple user interface
* Support analysis of multiple replay files

## Development Environment

The project will primarily be developed using:

* Python
* Visual Studio Code
* peppi-py
* pandas
* NumPy
* Streamlit
* pytest
* GitHub

## Planned Architecture

The application will be divided into several major components:

### Replay Parser

Reads Slippi `.slp` replay files and converts the replay data into information that can be used by the rest of the application.

### Gameplay Analyzer

Processes the replay information and calculates statistics related to areas such as technical execution, offense, defense, and punish efficiency.

### Feedback Engine

Uses predefined rules to convert gameplay statistics and observations into useful recommendations for the player.

### Character Analysis

Provides additional feedback based on the specific character being played.

### User Interface

Allows the user to upload Slippi replay files and view the resulting statistics and recommendations through a Streamlit interface.

## Initial Scope

The first version of Melee Coach will focus on objective and statistically measurable gameplay behaviors rather than attempting to determine the optimal decision in every situation.

General analysis will be available for replay files, while more detailed character-specific analysis will initially be limited to a smaller number of characters.

## Current Status

The project is currently in the early development and setup stage as part of a semester-long Software Engineering course project for CPSC 362.

## Current Progress

Melee Coach currently supports:

- Uploading Slippi `.slp` replay files
- Parsing replay data with peppi-py
- Identifying players, characters, stage, stocks, and timer
- Displaying a match summary through Streamlit
- Loading frame-by-frame gameplay data
- Handling duplicate rollback frames by using the final recorded frame version
- Detecting gameplay openings/conversions
- Calculating Openings Per Kill (OPK)
- Displaying OPK statistics in the Streamlit interface
- Running automated tests with pytest

## Openings Per Kill

Openings Per Kill (OPK) is the first gameplay-analysis
metric implemented in Melee Coach.

The statistic is calculated as:

`OPK = Openings / Kills`

A lower OPK means that fewer offensive openings were required,
on average, to take a stock.

The OPK implementation was validated against statistics generated
by the Slippi JavaScript SDK using the same replay file.

For the validation replay:

- Falco: 9 openings, 2 kills, OPK = 4.50
- Fox: 11 openings, 4 kills, OPK = 2.75

The Melee Coach results matched the Slippi reference statistics.

## Next Development Goals

Planned next steps include:

- Validate OPK using additional replay files
- Add additional gameplay statistics
- Develop initial coaching-feedback rules
- Add character-specific analysis
- Support analysis across multiple replay files