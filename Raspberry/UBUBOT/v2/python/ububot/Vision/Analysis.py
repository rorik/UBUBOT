#!/usr/bin/python3
import cv2
import numpy as np

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
