import numpy as np
import cv2 as cv
# from matplotlib import pyplot as plt


def padder(image):
    # input: numpy array image
    # returns: a numpy array image (canvas), where the image is projected onto a black canvas
    # the image ontop of the canvas is centered vertically, and shifted to the left 1/4

    h, w, c = image.shape

    canvas = np.zeros((h * 2, w * 2, 3), dtype=np.uint8)

    x_offset = round(w/8)
    y_offset = round(h / 2)

    canvas[y_offset:y_offset+image.shape[0], x_offset:x_offset+image.shape[1]] = image
    return canvas



def xor_images(img1, img2):

    img1_gray = cv.cvtColor(img1, cv.COLOR_BGR2GRAY)
    img2_gray = cv.cvtColor(img2, cv.COLOR_BGR2GRAY)
    img_intersection = cv.bitwise_and(img1_gray, img2_gray)

    # cv.imshow("intersection", img_intersection)

    img_xor = cv.bitwise_or(img1, img2)

    print('Starting')
    for i, row in enumerate(np.nditer(img_intersection, flags=['external_loop'], order='F')):
        print(i)
        row_list = list(row)
        index_first_non_zero = next((i for i, val in enumerate(row_list) if val != 0), None)
        if(index_first_non_zero == None):
            continue
        index_first_non_zero_backwards = next((i for i, val in enumerate(row_list[::-1]) if val != 0), None)

        print("setting..")
        index_last_non_zero = len(row_list) - index_first_non_zero_backwards
        img_xor[index_first_non_zero:index_last_non_zero, i] = [0, 0, 0]
    return img_xor

def smooth_blend(img1, img2):
    
    # compute the intersection of img1 and img2
    # blend the intersection
    # add the XOR of the images back
    blended_intersection = cv.addWeighted(img1, 0.5, img2, 0.5, 2.0)

    # cv.imshow("intersection", blended_intersection)

    xor = xor_images(img1, img2)

    # cv.imshow("xor", xor)


    # Add the blended intersection and the XOR of the images back
    result = cv.add(blended_intersection, xor)
    # cv.imshow("result", result)

    # cv.imwrite("result.png", result)

    cv.waitKey(0)

    return result


def stitch(img1, img2):

    # img2 will act as our 'destination' or 'canvas' that img2 will be projected onto
    # we need to pad img1
    print("STITCHING!")
    img2 = padder(img2)
    cv.imwrite('left_padded.png', img2)
    # find the keypoints and descriptors with SIFT
    detector = cv.AKAZE_create()
    kp1, des1 = detector.detectAndCompute(img1, None)
    kp2, des2 = detector.detectAndCompute(img2, None)

    bf = cv.BFMatcher(cv.NORM_HAMMING, crossCheck=True)

    matches = bf.match(des1,des2)
    matches = sorted(matches, key = lambda x:x.distance)

    img3 = cv.drawMatches(img1,kp1,img2,kp2,matches[:10],None,flags=cv.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS)
    cv.imwrite("matches.png", img3)

    src_pts = np.float32([ kp1[matches[m].queryIdx].pt for m in range(0, 20) ]).reshape(-1,1,2)
    dst_pts = np.float32([ kp2[matches[m].trainIdx].pt for m in range(0, 20) ]).reshape(-1,1,2)

    h, status = cv.findHomography(src_pts, dst_pts)

    imgWarp = cv.warpPerspective(img1, h, (img2.shape[1], img2.shape[0])) # mapping to DESTINATION domain
    cv.imwrite('warp.png', imgWarp)
    # smooth = smooth_blend(img2, imgWarp)

    merged = cv.bitwise_or(img2, imgWarp) #https://docs.opencv.org/3.4/d2/de8/group__core__array.html#gab85523db362a4e26ff0c703793a719b4
    return merged

def hello_flask():
    return "Hello flask!"

if __name__ == "__main__":

    img1 = cv.imread('q2/right.jpg',1)
    img2 = cv.imread('q2/left.jpg',1)

    # cv.imshow("test", img1)
    # cv.waitKey(0)

    result = stitch(img1, img2)