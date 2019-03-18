#!/usr/bin/python3
from itertools import chain
import numpy as np
import cv2


def get_stops(sections, threshold=30):
    return {relative_y: [line for line in section if line[1] - line[0] > threshold] for relative_y, section in sections.items()}

def get_paths(sections, threshold=30):
    sorted_sections = sorted(sections.items(), reverse=True)
    paths = []
    closed = []
    for line in sorted_sections[0][1]:
        paths.append([[sorted_sections[0][0], line]])
    for relative_y, section in sorted_sections[1:]:
        new_paths = []
        open_paths = set()
        for line in section:
            midpoint = _midpoint(*line)
            for index_path in range(len(paths)):
                if _is_between(midpoint, *paths[index_path][-1][1]):
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


def draw_paths(img, paths=None, color=(0, 0, 255)):
    for path in paths:
        previous = None
        for relative_y, line in path:
            y = int(img.shape[0] * (relative_y + 50) / 100) - 1
            x = int(img.shape[1] * _midpoint(*line) / 100) 
            if previous is not None:
                cv2.line(img, previous, (x, y), color, 2)
            previous = (x, y)


def _midpoint(x1, x2):
    return (x1 + x2) / 2

def _is_between(x, x1, x2):
    return x1 <= x <= x2
