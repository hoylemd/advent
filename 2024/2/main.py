from argparse import ArgumentParser
from utils import logger, parse_input
from typing import Iterator


class Report:

    def __init__(self, number: int, levels: list):
        self.number = number
        self.levels = levels
        self.direction = None

    def is_safe(self) -> bool:
        prev = None

        for i, level in enumerate(self.levels):
            if prev is None:
                prev = level
                continue

            delta = level - prev
            if self.direction is None:
                self.direction = 1 if delta > 0 else -1

            normalized_delta = delta * self.direction
            if normalized_delta < 1 or normalized_delta > 3:
                # unsafe found!
                return False

            prev = level

        return True

    def __str__(self) -> str:
        return f"#{self.number}: {self.levels}"

    def subreports(self):
        for i in range(len(self.levels)):
            yield Report(self.number, self.levels[0:i] + self.levels[i + 1:])


def parse_line(line: str):
    return [int(l) for l in line.split()]


class Reports:

    def __init__(self, lines: Iterator[str], part: int = 1):
        self.part = part

        self.reports = [Report(i, parse_line(line)) for i, line in enumerate(lines)]

        self.safe_reports = []
        self.unsafe_reports = []

    def __str__(self):
        return f"{self.__class__.__name__}(part {self.part})"

    def sort_reports(self):
        for report in self.reports:
            if report.is_safe():
                self.safe_reports.append(report)
            else:
                self.unsafe_reports.append(report)


def count_safe(reports: Reports) -> int:
    reports.sort_reports()
    return len(reports.safe_reports)


def count_safe_and_safeish(reports: Reports) -> int:
    reports.sort_reports()

    safeish = []
    very_unsafe = []

    for report in reports.unsafe_reports:
        print(f"attempting to make {report} safe")
        for subreport in report.subreports():
            print(subreport)
            if subreport.is_safe():
                print('is safish!')
                safeish.append(subreport)
                break
        print(f"{report} is NOT safe")
        very_unsafe.append(report)

    return len(reports.safe_reports) + len(safeish)


def slowly_dampen_error(report):
    for i, level in enumerate(report.levels):
        subreport = Report(report.number, report.levels)
        print(f"slowsafe(): {subreport}")
        if subreport.is_safe():
            return subreport

    return None


arg_parser = ArgumentParser('python -m {{year}}.{{day}}.main', description="Advent of Code {{ year }} Day {{ day }}")
arg_parser.add_argument('input_path', help="Path to the input file")
arg_parser.add_argument('part', type=int, default=1, help="Which part of the challenge to apply.")

if __name__ == '__main__':
    argus = arg_parser.parse_args()

    lines = parse_input(argus.input_path)
    reports = Reports(lines, argus.part)
    if argus.part == 1:
        answer = count_safe(reports)
    else:
        answer = count_safe_and_safeish(reports)

    logger.debug('')

    print(f"answer:\n{answer}")
