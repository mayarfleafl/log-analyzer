import sys
import re


def main():
    if len(sys.argv) < 2:
        sys.exit("Too few command-line arguments")

    if len(sys.argv) > 2:
        sys.exit("Too many command-line arguments")

    try:
        file = sys.argv[1]
        fun1 = parsing(file)
        fun2 = analyzer(fun1)
        report(fun2, file)
    except FileNotFoundError:
        sys.exit(f"Could not read {file}")


def parse_perLine(line):

    match = re.search(
        r"^(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2}) (INFO|WARNING|ERROR)", line)

    if not match:
        return None

    rest = line[match.end():]
    matches = re.findall(r"(\w+)=(\".*?\"|\S+)", rest.lstrip())

    if not matches:
        return None

    date, time, level = match.groups()
    user = None
    code = None
    action = None
    msg = None

    for key, value in matches:
        if key == "user":
            user = value

        if key == "code":
            code = value

        if key == "action":
            action = value

        if key == "msg":
            msg = value

    if level == "INFO" and user is None:
        return None

    vars = [date, time, level, user, code, action, msg]
    return vars


def parsing(file):
    with open(file) as f:
        for line in f:
            result = parse_perLine(line)
            if result:
                [date, time, level, user, code, action, msg] = result
                parsed = {
                    "date": date,
                    "time": time,
                    "level": level,
                    "user": user,
                    "code": code,
                    "action": action,
                    "msg": msg
                }
                yield parsed


def analyzer(items):
    E = W = I = 0
    ERROR_msgs = {}
    WARNING_msgs = {}
    users_count = {}
    for item in items:
        if item["level"] == "ERROR":
            E += 1
            if item["msg"]:
                if item["msg"] in ERROR_msgs:
                    ERROR_msgs[item["msg"]] += 1
                else:
                    ERROR_msgs[item["msg"]] = 1

        elif item["level"] == "INFO":
            I += 1
            if item["user"]:
                if item["user"] in users_count:
                    users_count[item["user"]] += 1
                else:
                    users_count[item["user"]] = 1

        elif item["level"] == "WARNING":
            W += 1
            if item["msg"]:
                if item["msg"] in WARNING_msgs:
                    WARNING_msgs[item["msg"]] += 1
                else:
                    WARNING_msgs[item["msg"]] = 1

                if item["user"]:
                    if item["user"] in users_count:
                        users_count[item["user"]] += 1
                    else:
                        users_count[item["user"]] = 1

    return {"no_E": E, "no_W": W, "no_I": I, "error_msgs": ERROR_msgs, "warning_msgs": WARNING_msgs, "no_users": users_count}


def report(analyzed, file):

    with open(file) as f1:
        no_lines = sum(1 for _ in f1)

    with open("report.txt", "w") as f2:

        f2.write(f"LOG ANALYSIS REPORT\n*******************\n")
        f2.write(f"\nTotal Lines: {no_lines}")
        f2.write(
            f"\nInvalid Lines: {no_lines - (analyzed['no_I'] + analyzed['no_E'] + analyzed['no_W'])}\n")
        f2.write(
            f"\nLevel:\nINFO: {analyzed['no_I']}\nERROR: {analyzed['no_E']}\nWARNING: {analyzed['no_W']}\n")
        f2.write(f"\nTop 3 Errors:\n")

        i = 0
        for item1 in sorted(analyzed['error_msgs'].items(), key=lambda item1: item1[1], reverse=True):
            f2.write(f"{item1[0].strip('\"')}: {item1[1]}\n")
            i += 1
            if i == 3:
                break

        f2.write(f"\nTop 3 Warnings:\n")
        i = 0
        for item2 in sorted(analyzed['warning_msgs'].items(), key=lambda item2: item2[1], reverse=True):
            f2.write(f"{item2[0].strip('\"')}: {item2[1]}\n")
            i += 1
            if i == 3:
                break

        if analyzed["no_users"]:
            user1, maxNum = max(
                analyzed["no_users"].items(), key=lambda item: item[1])
            f2.write(
                f"\nMost active user:\nUser {user1} ({maxNum} actions)")

        else:
            empty = "No user data"
            f2.write(f"\nMost active user:\nUser ({empty})")


if __name__ == "__main__":
    main()
