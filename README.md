# Log Analyzer

#### Video Demo: [HERE](https://youtu.be/9gDYw6kk3kI?si=qiW9Y83mHvrHV5xf)

## Description

Log Analyzer is a command-line Python project designed to read, parse, and analyze log files in order to understand what’s happening inside a system, application, server, or network. Logs are commonly used to track events such as user actions, warnings, and errors. However, log files are often long and difficult to read manually. This project solves that problem by reading each log entry, extracting useful information, and generating a clear summary report that highlights the most important insights.

---

## How the program works

The program runs from the command line and expects only one argument, which is the log file name. If the user provides more than one argument or does not provide any argument, the program exits with an appropriate error message. It also safely handles cases where the file does not exist to prevent the program from crashing.

### Program workflow

#### Parsing the log file
Each line is checked using a regular expression to make sure it matches the expected format. If the line is valid, the program extracts important fields such as date, time, level, user, action, code, and message. This step converts raw text into structured data that can be analyzed later.

#### Filtering invalid lines
Lines that do not follow the required format are ignored. This helps keep the analysis accurate and prevents incorrect data from affecting the final results.

#### Analyzing the data
After parsing, the program analyzes the information by counting:

- The number of INFO, WARNING, and ERROR records
- How often each error message appears
- How often each warning message appears
- User activity to determine the most active user

#### Generating the report
Finally, the results are written to a file called `report.txt`, which contains a clear and organized summary of the analysis.

---

## File structure

- **project.py** — Main program containing parsing, analysis, and reporting logic.
- **sample.log** — Sample log file used for testing and demonstration.
- **test_project.py** — Unit tests for validating program behavior.
- **report.txt** — Output file generated after running the program.
- **README.md** — Project documentation.

---

## Log format rules

A valid log line should follow this format:

`YYYY-MM-DD HH:MM:SS LEVEL key=value ...`

Supported levels are INFO, WARNING, and ERROR.

INFO entries must include a user field. Values can be quoted if needed, and any line that does not match the format is ignored.

---

## Design choices

- I used a generator in the parsing step to avoid loading the whole file into memory.
- Regular expressions are used to validate and extract data from each line.
- The program is divided into separate functions for parsing, analysis, and reporting to keep the code organized and easier to maintain.
- Dictionaries are used to count messages and user activity efficiently.

---

## Future improvements

Right now the project supports only three log levels and assumes a fixed log format. In the future, I could improve it by adding more analysis features, such as using timestamps to generate time-based statistics (for example, activity per hour or peak usage times). Other possible improvements include handling ties for the most active user and adding more command-line options.
