from main.detect_blur import detect_blur_fft
import numpy as np
import cv2
import argparse
import os

argparse = argparse.ArgumentParser()

argparse.add_argument(
    "-i", "--images", type=str, help="path to input directory of images"
)

argparse.add_argument(
    "-t",
    "--threshold",
    type=float,
    default=20,
    help="threshold value for the blur to be found",
)

argparse.add_argument(
    "--vis",
    action='store_true', default=False,
    help="If present, visualizing intermediary steps"
)

argparse.add_argument(
    "--test",
    action='store_true', default=False,
    help="If present, progressively blur the image"
)

argparse.add_argument(
    "--remove",
    action='store_true', default=False,
    help="If present, remove any detected blurry image."
)

args = argparse.parse_args()

data_path = os.path.join(os.getcwd(), "{}".format(args.images))

for root, sub_dirs, files in os.walk(data_path):
    for file in sorted(files):
        orig = cv2.imread(os.path.join(root, file))
        h, w, r = orig.shape
        orig = cv2.resize(orig, (h, 500))
        gray = cv2.cvtColor(orig, cv2.COLOR_BGR2GRAY)

        mean, blurry = detect_blur_fft(
            gray, size=60, threshold=args.threshold, vis=args.vis
        )
        text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
        text = text.format(mean)
        print("Info: ", file, text)
        if args.remove and blurry:
            print("Info: Removed ", file)
            os.remove(os.path.join(root, file))

        # image = np.dstack([gray] * 3)
        # color = (0, 0, 255) if blurry else (0, 255, 0)
        # text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
        # text = text.format(mean)
        # cv2.putText(image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
        # print("Info: ", file, text)
        #
        # cv2.imshow("Output", image)
        # cv2.waitKey(0)

        if args.test:
            for radius in range(1, 30, 2):
                image = gray.copy()

                if radius > 0:
                    image = cv2.GaussianBlur(image, (radius, radius), 0)

                    (mean, blurry) = detect_blur_fft(image, size=60, threshold=args.threshold, vis=args.vis)

                    image = np.dstack([image] * 3)
                    color = (0, 0, 255) if blurry else (0, 255, 0)
                    text = "Blurry ({:.4f})" if blurry else "Not Blurry ({:.4f})"
                    text = text.format(mean)
                    cv2.putText(image, text, (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.7, color, 2)
                    print("Info: ", text)

                    cv2.imshow("Output", image)
                    cv2.waitKey(0)
