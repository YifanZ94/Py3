#Author : @cr0wst

import os
import pathlib
import cv2 as cv
import imutils
import numpy as np

TRAINING_IMAGE_PATH = 'images/train'

MIN_THRESHOLD = 50
MAX_THRESHOLD = 150

def main():
    cap = cv.VideoCapture(0)
    training_set = load_training_set()
    cv.namedWindow("Image")

    while True:
        __, frame = cap.read()
        process(frame, training_set)

        k = cv.waitKey(5) & 0xff

        if k == 27:
            break

    cap.release()
    cv.destroyAllWindows()

def process(frame, training_set):
    frame = imutils.resize(frame, 640)
    image = frame.copy()
    dilate = process_webcam_frame(image)
    contours = get_contours(dilate)

    for c in contours[:2]:   
        ((x, y), (w, h), a) = rect = cv.minAreaRect(c)
        box = cv.boxPoints(rect)
        box = np.int0(box)

        # sometimes w and h are reversed for turned images
        ar = w / float(h) if w > h > 0 else h / float(w)

        if 1.30 <= ar <= 1.42:
            cv.drawContours(image, [box], -1, (0, 255, 0), 3)
            cropped_image = crop_image(image, rect)
            if cropped_image.shape[0] > 0 and cropped_image.shape[1] > 0:
                cropped_image = process_card_image(cropped_image)
                cropped_image = resize_image(cropped_image)
                prediction, percentage = predict(training_set, cropped_image)
                cv.putText(image, prediction, (int(x - w / 2), int(y)), cv.FONT_HERSHEY_SIMPLEX, .75, 255, 4)
                cv.putText(image, str(f'{percentage * 100:.2f}' + '%'), (int(x - w / 2), int(y + 20)),
                            cv.FONT_HERSHEY_SIMPLEX, .50, 255, 2)
    cv.imshow("Image", np.hstack((image, cv.cvtColor(dilate, cv.COLOR_RGB2BGR))))

def crop_image(original_image, rect):
    ((x, y), (w, h), a) = rect

    # Rotate the image so that the rectangle is in the same rotation as the frame.
    shape = (original_image.shape[1], original_image.shape[0])
    matrix = cv.getRotationMatrix2D(center=(x, y), angle=a, scale=1)
    rotated_image = cv.warpAffine(src=original_image, M=matrix, dsize=shape)

    # Crop the image from the rotation
    cx = int(x - w / 2)
    cy = int(y - h / 2)
    return rotated_image[cy:int(cy + h), cx:int(cx + w)]

def resize_image(image):
    approx = np.array(
        [[0, 0], [0, image.shape[0]], [image.shape[1], image.shape[0]],
         [image.shape[1], 0]], np.float32)
    h = np.array([[0, 0], [0, 449], [449, 449], [449, 0]], np.float32)
    transform = cv.getPerspectiveTransform(np.float32(approx), h)
    return cv.warpPerspective(image, transform, (450, 450))

def get_contours(dilate):
    contours = cv.findContours(dilate.copy(), cv.RETR_LIST, cv.CHAIN_APPROX_SIMPLE)
    contours = imutils.grab_contours(contours)
    return sorted(contours, key=cv.contourArea, reverse=True)

def predict(training_set, test_image):
    differences = []
    for training_image in training_set:
        diff = cv.absdiff(test_image, training_image['image'])
        differences.append(np.sum(diff))

    match = training_set[np.argmin(differences)]

    index = np.argmin(differences)
    submatch = training_set[index]['image']
    diff = cv.absdiff(test_image, submatch)

    # Calculate how close we are to matching by dividing the number of black pixels
    # by the total number of pixels. Black pixels indicate a match between the two images.
    total_pixels = diff.shape[0] * diff.shape[1]
    black_pixels = cv.countNonZero(diff)
    percentage = (total_pixels - black_pixels) / total_pixels
    cv.imshow("Matched", np.hstack((test_image, submatch, diff)))

    return match['label'], percentage

def load_training_set():
    training_set = []
    image_paths = load_all_image_paths()

    for path in image_paths:
        label = pathlib.Path(path).parent.name
        image = cv.imread(path)
        image = process_card_image(image)
        contours = cv.findContours(image, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        contours = imutils.grab_contours(contours)
        contours = sorted(contours, key=cv.contourArea, reverse=True)[:1]

        card = contours[0]
        peri = cv.arcLength(card, True)
        approx = cv.approxPolyDP(card, 0.02 * peri, True)
        h = np.array([[0, 0], [0, 449], [449, 449], [449, 0]], np.float32)
        transform = cv.getPerspectiveTransform(np.float32(approx), h)
        warp = cv.warpPerspective(image, transform, (450, 450))

        # Save Original
        training_set.append(dict(label=label, image=warp.copy()))

        # Rotate 3 times and save each to allow for non-symmetric symbols
        m = cv.getRotationMatrix2D((warp.shape[1] / 2, warp.shape[0] / 2), 90, 1)

        warp = cv.warpAffine(warp.copy(), m, (warp.shape[1], warp.shape[0]))
        training_set.append(dict(label=label, image=warp.copy()))

        warp = cv.warpAffine(warp.copy(), m, (warp.shape[1], warp.shape[0]))
        training_set.append(dict(label=label, image=warp.copy()))

        warp = cv.warpAffine(warp.copy(), m, (warp.shape[1], warp.shape[0]))
        training_set.append(dict(label=label, image=warp.copy()))
    return training_set


def load_labels():
    labels = []
    for directory in os.listdir(TRAINING_IMAGE_PATH):
        if directory[0] != '.':
            labels.append(directory)

    return labels


def load_all_image_paths():
    all_image_paths = []
    for path, subdirs, files in os.walk(TRAINING_IMAGE_PATH):
        for name in files:
            if name[-3:] == 'jpg':
                all_image_paths.append(os.path.abspath(os.path.join(path, name)))

    return all_image_paths


def label_images(image_paths, labels):
    label_to_index = dict((name, index) for index, name in enumerate(labels))
    return [label_to_index[pathlib.Path(path).parent.name] for path in image_paths]


def process_webcam_frame(frame):
    kernel = np.ones((5, 5), np.uint8)
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    blur = cv.bilateralFilter(gray, 10, 15, 15)
    cv.imshow("blur", blur)
    edges = cv.Canny(blur, MIN_THRESHOLD, MAX_THRESHOLD, True)
    dilate = cv.dilate(edges, kernel, iterations=1)

    return dilate




def process_card_image(image):
    gray = cv.cvtColor(image.copy(), cv.COLOR_BGR2GRAY)
    _, thresh = cv.threshold(gray, 150, 255, cv.THRESH_BINARY)

    return thresh

main()