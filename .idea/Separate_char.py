import cv2
import os
import numpy as np


def separate_dig():
    im = cv2.imread("./static/Images/" + "/equation.png")
    gray_image = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

    # cv2.imwrite("./Images/" + 'gray_image.png', gray_image)

    def dfs(a, b):
        # Iterative
        ymin = b
        ymax = b
        stack = []
        stack.append((a, b))
        while len(stack):
            x = stack[-1][0]
            y = stack[-1][1]

            if ymax < y:
                ymax = y

            stack.pop()

            if gray_image[x][y] > 123:
                continue
            else:
                gray_image[x][y] = 255
                output_image[x][y] = 0
                for i in range(-1, 2):
                    for j in range(-1, 2):
                        if i + x >= 0 and i + x < gray_image.shape[0] and y + j >= 0 and y + j < gray_image.shape[1]:
                            stack.append((x + i, y + j))

        return (ymax - ymin)

    flag = 0
    write_flag = False
    output_image = np.full((gray_image.shape[0], gray_image.shape[1]), 255)

    j = 0
    while j < gray_image.shape[1]:
        i = 0
        while i < gray_image.shape[0]:

            if gray_image[i][j] <= 123:
                write_flag = True

                yjump = dfs(i, j)
                max_jump = int(yjump * 0.5)
                if max_jump != 0:  # And symbol is not square root -> Has to be dealt seperately
                    j += max_jump
                    i = -1

            i += 1
        j += 1

        if write_flag:
            write_flag = False
            flag += 1
            cv2.imwrite("./static/digits/" + 'digit' + str(flag) + '.png', output_image)
            output_image = np.full((gray_image.shape[0], gray_image.shape[1]), 255)


    folder_path = './static/Images/'

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        if os.path.isfile(file_path):
            os.remove(file_path)

    return True
