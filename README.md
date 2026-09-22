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
