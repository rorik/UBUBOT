#!/usr/bin/python3
from itertools import chain
import cv2
import numpy as np
import operator


def get_lines(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)
    minLineLength = 100
    maxLineGap = 20
    lines = cv2.HoughLinesP(edges, 1, np.pi/180, 90, minLineLength, maxLineGap)
    return lines


def get_contours(img):
    imgray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    ret, thresh = cv2.threshold(imgray, 127, 255, 0)
    im2, contours, hierarchy = cv2.findContours(
        thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    return contours


def get_sections(img, precision=10):
    lines = None
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    img = _to_binary(img)

    return _sections(img, precision)


def draw_lines(img, lines=None, color=(0, 255, 0)):
    if lines is None:
        lines = get_lines(img)
        if lines is None:
            return
    for line in lines:
        for x1, y1, x2, y2 in line:
            cv2.line(img, (x1, y1), (x2, y2), color, 2)


def draw_contours(img, contours=None, color=(0, 255, 0)):
    if contours is None:
        contours = get_contours(img)
        if contours is None:
            return
    cv2.drawContours(img, contours, -1, color, 3)


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


def _sections(img, precision):
    sections = {}
    for relative_y in chain(range(0, 51, precision), range(-precision, -50, -precision)):
        y = int(img.shape[0] * (relative_y + 50) / 100) - 1
        max_index = img.shape[1] - 1

        intersections = [index for index in range(img.shape[1]) if
                         index == 0 or index == max_index or (not img[y][index]) != (not img[y][index - 1])]

        if img[y][intersections[0]] > 0:
            intersections = intersections[1:]
        if len(intersections) % 2 == 1:
            intersections = intersections[:-1]

        sections[relative_y] = [((intersections[i] * 100) / img.shape[1], (intersections[i + 1] * 100) / img.shape[1]) for i in
                                range(0, len(intersections), 2)]
    return sections


def _find_local_extrema(hist, op=operator.lt):
    hist_len = len(hist)
    last_index = hist_len - 1
    unfiltered_extrema = [index for index in range(hist_len) if (index == 0 and op(hist[0], hist[1])) or (
        index == last_index and op(hist[last_index], hist[last_index - 1])) or (
        index > 0 and index < last_index and op(hist[index], hist[index - 1]) and op(
            hist[index], hist[index + 1]))]
    return [unfiltered_extrema[index] for index in range(len(unfiltered_extrema)) if
            index == 0 or unfiltered_extrema[index - 1] + 1 != unfiltered_extrema[index]]


def _to_binary(img):

    def find_extrema(histogram):
        initial_maxima = _find_local_extrema(
            histogram, operator.ge)
        extrema_threshold = 0
        maxima = []
        while len(maxima) < 2:
            extrema_threshold += .05
            if extrema_threshold >= 1.0:
                return 1
            tmp_maxima = [
                index for index in initial_maxima if histogram[index] > extrema_threshold]
            maxima = [tmp_maxima[x] for x in range(len(tmp_maxima)) if
                      x == 0 or (tmp_maxima[x - 1] + 20) < tmp_maxima[x]]

        minima = [index for index in _find_local_extrema(histogram, operator.le) if
                  histogram[index] < extrema_threshold]
        possible_minima = [index for index in minima if index >
                           maxima[0] and index < maxima[1]]
        return min(possible_minima)

    def erode_and_dilate(image):
        kernel = np.ones((3, 3), np.uint8)
        img_erode = cv2.erode(image, kernel, iterations=2)
        img_dilate = cv2.dilate(img_erode, kernel, iterations=3)
        return img_dilate

    hist = np.histogram(img.ravel(), 256, [0, 256])[0]
    hist = hist.astype(float) / max(hist)

    return cv2.threshold(erode_and_dilate(cv2.threshold(img, find_extrema(hist) + 6, 255, cv2.THRESH_BINARY)[1]), 10, 255, cv2.THRESH_BINARY)[1]
