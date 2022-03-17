import cv2
import numpy as np
import sys

def  onMouse(event, x, y, flag, param):
    global select_point_num 
    global img

    if event == 4 and select_point_num <4:
        print(x, y, select_point_num) 

        # 已选择的点加 1
        select_point_num = select_point_num + 1

        # 将选择好的点添加到相应的数组当中
        point = (x,y)
        cv2.circle(img, point, 2, (0, 255, 0), 2)#修改最后一个参数

        # 划线
        if len(star_points) >= 1:
            # 取出最后一个点
            last_point = star_points[len(star_points)-1]
            # 划线
            cv2.line(img, point, last_point, (155, 155, 155), 2)

        if len(star_points) == 3:
            # 取出开始的一个点
            last_point = star_points[0]
            # 划线
            cv2.line(img, point, last_point, (155, 155, 155), 2)

        # 更新图片
        cv2.imshow(window, img)
        star_points.append(point)
        if len(star_points) == 4:
            rectify_that_part_of_photo()


def  rectify_that_part_of_photo():
    global star_points
    global opened_pic_file

   # 打开一份备份img
    img_copy = cv2.imread(opened_pic_file)
    cv2.namedWindow("result_img", 0);


    origin_selected_conors = []
    rigin_selected_lu = (star_points[0][0],star_points[0][1])
    rigin_selected_ru = (star_points[1][0],star_points[1][1])
    rigin_selected_ld = (star_points[3][0],star_points[3][1])
    rigin_selected_rd = (star_points[2][0],star_points[2][1])

    # 添加到 origin_selected_conors
    origin_selected_conors.append(rigin_selected_lu)
    origin_selected_conors.append(rigin_selected_ru)
    origin_selected_conors.append(rigin_selected_rd)
    origin_selected_conors.append(rigin_selected_ld)

    # 变换过后图像展示在 一个 宽为 show_width 长为 show_height的长方形窗口
    show_window_conors = []
    show_window_lu = (0, 0)
    show_window_ru = (show_width-1, 0)
    show_window_ld = (0, show_height-1)
    show_window_rd = (show_width-1, show_height-1)

    # 添加到 show_window_conors中
    show_window_conors.append(show_window_lu)
    show_window_conors.append(show_window_ru)
    show_window_conors.append(show_window_rd)
    show_window_conors.append(show_window_ld)

    # 获得transform 函数
    transform = cv2.getPerspectiveTransform(np.array(show_window_conors, dtype=np.float32), np.array(origin_selected_conors, dtype=np.float32))

    # 
    transfered_pos = np.zeros([show_width, show_height, 2])
    for x in range(show_width):
        for y in range(show_height):
            temp_pos = np.dot(transform, np.array([x, y, 1]).T)
            transed_x = temp_pos[0]/temp_pos[2]
            transed_y = temp_pos[1]/temp_pos[2]
            transfered_pos[x][y] = (int(transed_x), int(transed_y))

    # 生成 一个空的彩色图像
    result_img = np.zeros((show_height, show_width, 3), np.uint8)
    print(result_img.shape) 

    for x in range(show_width):
        for y in range(show_height):
            result_img[y][x] = img_copy[transfered_pos[x][y][1]][transfered_pos[x][y][0]]

    cv2.imshow("result_img", result_img);

if __name__ == '__main__':
    # 获取用户的输入
    # opened_pic_file 输入的图片地址和文件名
    if len(sys.argv) != 2:
        print("please input the filename!!!") 
        exit(0)
    else:
        opened_pic_file = sys.argv[1]


    img = cv2.imread(opened_pic_file)
    img2 = []

    cv2.namedWindow("window", cv2.WINDOW_NORMAL)

    cv2.imshow("window", img)

    # 2. 给用户注册鼠标点击事件
    cv2.setMouseCallback("window", onMouse, None);

    # 监听用户的输入，如果用户按了esc按键，那么就将window给销毁
    key = cv2.waitKey(0)
    if key == 27:
        cv2.destroyWindow("window")
