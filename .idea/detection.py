from keras.models import model_from_json
import cv2
import numpy as np

json_file = open('model_final.json', 'r')
loaded_model_json = json_file.read()
json_file.close()
loaded_model = model_from_json(loaded_model_json)
# load weights into new model
loaded_model.load_weights("model_final.h5")
aakash = []


def detector(inp_file):
    img = cv2.imread(inp_file, cv2.IMREAD_GRAYSCALE)

    if img is not None:
        # images.append(img)
        img = ~img
        ret, thresh = cv2.threshold(img, 127, 255, cv2.THRESH_BINARY)
        ctrs, ret = cv2.findContours(
            thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        cnt = sorted(ctrs, key=lambda ctr: cv2.boundingRect(ctr)[0])
        w = int(28)
        h = int(28)
        train_data = []
        rects = []
        for c in cnt:
            x, y, w, h = cv2.boundingRect(c)
            rect = [x, y, w, h]
            rects.append(rect)
        bool_rect = []
        for r in rects:
            l = []
            for rec in rects:
                flag = 0
                if rec != r:
                    if r[0] < (rec[0]+rec[2]+10) and rec[0] < (r[0]+r[2]+10) and r[1] < (rec[1]+rec[3]+10) and rec[1] < (r[1]+r[3]+10):
                        flag = 1
                    l.append(flag)
                if rec == r:
                    l.append(0)
            bool_rect.append(l)
        dump_rect = []
        for i in range(0, len(cnt)):
            for j in range(0, len(cnt)):
                if bool_rect[i][j] == 1:
                    area1 = rects[i][2]*rects[i][3]
                    area2 = rects[j][2]*rects[j][3]
                    if (area1 == min(area1, area2)):
                        dump_rect.append(rects[i])
        final_rect = [i for i in rects if i not in dump_rect]
        for r in final_rect:
            x = r[0]
            y = r[1]
            w = r[2]
            h = r[3]
            im_crop = thresh[y:y+h+10, x:x+w+10]

            im_resize = cv2.resize(im_crop, (28, 28))

            im_resize = np.reshape(im_resize, (28, 28, 1))
            train_data.append(im_resize)


    char_string = ""

    for i in range(len(train_data)):
        train_data[i] = np.array(train_data[i])
        train_data[i] = train_data[i].reshape(1, 28, 28, 1)
    #     result=loaded_model.predict_classes(train_data[i])
        result = np.argmax(loaded_model.predict(train_data[i]), axis=-1)
        aakash.append(result[0])
        if (result[0] == 10):
            char_string = char_string + '-'
        if (result[0] == 11):
            char_string = char_string + '+'

        if (result[0] == 12):
            char_string = char_string + '/'

        if (result[0] == 23):
            char_string = char_string + "*"

        if (result[0] == 15):
            char_string = char_string + "("

        if (result[0] == 16):
            char_string = char_string + ")"

        if (result[0] == 13):
            char_string = char_string + "**"

        if (result[0] == 17):
            char_string = char_string + "pi"

        # if (result[0] == 18):
        #     char_string = char_string + "//"

        if (result[0] == 19):
            char_string = char_string + ">"

        if (result[0] == 20):
            char_string = char_string + "<"

        # if (result[0] == 13):
        #     char_string = char_string + "="

        if (result[0] == 21):
            char_string = char_string + "sqrt"

        if (result[0] == 0):
            char_string = char_string + '0'
        if (result[0] == 1):
            char_string = char_string + '1'
        if (result[0] == 2):
            char_string = char_string + '2'
        if (result[0] == 3):
            char_string = char_string + '3'
        if (result[0] == 4):
            char_string = char_string + '4'
        if (result[0] == 5):
            char_string = char_string+ '5'
        if (result[0] == 6):
            char_string = char_string+ '6'
        if (result[0] == 7):
            char_string = char_string+ '7'
        if (result[0] == 8):
            char_string = char_string+ '8'
        if (result[0] == 9):
            char_string = char_string+ '9'

    return(char_string)

def detector_result():
    import os
    ranjan_final = []
    image_num = 1
    while os.path.isfile(f"static/digits/digit{image_num}.png"):
        try:
            # print(f"digits/digit{image_num}.png")
            charact = detector(f"static/digits/digit{image_num}.png")
            # print(charact[0])
            ranjan_final.append(charact[0:4])
        except:
            print("Error")
            ranjan_final.append("Error")
        finally:
            image_num += 1

    print(ranjan_final)
    # print(aakash)


    return ranjan_final
