#!/usr/bin/python3
from ububot.Vision.Analysis import draw_lines
from itertools import chain
import cv2

def get_sections(img, threshold=80, precision=10):
    lines = None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = cv2.threshold(img, threshold, 255, cv2.THRESH_BINARY)[1]

    return _sections(img, precision)

def get_stops(sections, threshold=30):
    return {relative_y: [line for line in section if line[1] - line[0] > threshold] for relative_y, section in sections.items()}

def get_paths(sections):
    sorted_sections = sorted(sections.items(), reverse=True)
    paths = []
    closed = []
    for line in sorted_sections[0][1]:
        paths.append([[sorted_sections[0][0], line]])
    for relative_y, section in sorted_sections[1:]:
        new_paths = []
        open_paths = set()
        for line in section:
            _midpoint = midpoint(*line)
            for index_path in range(len(paths)):
                if _is_between(_midpoint, *paths[index_path][-1][1]):
                    new_paths.append(paths[index_path] + [[relative_y, line]])
                    open_paths.add(index_path)
        for index_path in range(len(paths)):
            if index_path not in open_paths:
                closed.append(paths[index_path])
        paths = new_paths
        if len(paths) == 0:
            break
    closed.extend(paths)
    return closed

def draw_sections(img, sections=None, color=(0, 255, 0)):
    if sections is None:
        sections = get_sections(img)
        if sections is None:
            return
    lines = []
    for relative_y, section in sections.items():
        y = int(img.shape[0] * (relative_y + 50) / 100) - 1
        lines.extend([[[int(line[0] * img.shape[1] / 100), y,
                        int(line[1] * img.shape[1] / 100), y]] for line in section])
    draw_lines(img, lines, color)


def draw_paths(img, paths=None, color=(0, 0, 255)):
    for path in paths:
        previous = None
        for relative_y, line in path:
            y = int(img.shape[0] * (relative_y + 50) / 100) - 1
            x = int(img.shape[1] * midpoint(*line) / 100) 
            if previous is not None:
                cv2.line(img, previous, (x, y), color, 2)
            previous = (x, y)

def draw_line(img, x0, y0, x1, y1, color, relative=True):
    if relative:
        x0 = int(img.shape[1] * x0 / 100) 
        x1 = int(img.shape[1] * x1 / 100)
        y0 = int(img.shape[0] * y0 / 100) - 1
        y1 = int(img.shape[0] * y1 / 100) - 1
    cv2.line(img, (x0, y0), (x1, y1), color, 2)

def draw_all(img, precision=10, path_color=(0, 0, 255), stop_color=(255, 255, 0)):
    sections = get_sections(img, precision=precision)
    draw_paths(img, get_paths(sections), color=path_color)
    draw_sections(img, sections, color=stop_color)

def midpoint(x1, x2):
    return (x1 + x2) / 2

def _is_between(x, x1, x2):
    return x1 <= x <= x2

def _sections(img, precision, min_size=5, soft_threshold=5):
    sections = {}
    for relative_y in chain(range(0, 51, precision), range(-precision, -50, -precision)):
        y = int(img.shape[0] * (relative_y + 50) / 100) - 1
        max_gap = soft_threshold * img.shape[1] / 100
        min_line_size = min_size * img.shape[1] / 100
        
        lines = []
        current_line = None
        def add_line(line):
            if len(lines) > 0 and line[0] - lines[-1][1] <= soft_threshold:
                lines[-1][1] = current_line[1]
            elif line[1] - line[0] >= min_line_size:
                lines.append(line)
        for x in range(img.shape[1]):
            is_black = not img[y][x]
            if current_line is None:
                if is_black:
                    current_line = [x, x]
            elif x - current_line[1] > max_gap:
                add_line(current_line)
                current_line = None
            elif is_black:
                current_line[1] = x
        
        if current_line is not None:
            add_line(current_line)

        sections[relative_y] = [(line[0] * 100 / img.shape[1], line[1] * 100 / img.shape[1]) for line in lines]
    return sections