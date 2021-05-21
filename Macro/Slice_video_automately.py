import os
from tqdm import tqdm
import cv2 # read video file


def slice_video(file_dir:str, save_dir:str, N:int):
    """This function slice video files in file_dir directory by N second.
    Sliced video files are saved in save_dir directory.
    :: file_dir :: Where original video files were saved.(비디오 파일이 저장된 경로)
    :: save_dir :: Where the sliced video files will be saved in.(잘라낸 비디오 파일을 저장할 경로)
    :: N :: Slicing time unit(seconds) (비디오 파일을 자를 시간 단위(예 : 1초, 2초))
    [[Warning]] The rest will not be saved.(비디오를 N초 단위로 자르고 남은 나머지는 저장되지 않습니다.) """

    file_list = os.listdir(file_dir)  # Original video file list

    for file in tqdm(file_list):
        file_path = os.path.join(file_dir, file)  # full path or original video file
        video_name = file.split('.')[0]  # The name of each video file in file_list dir

        cap = cv2.VideoCapture(file_path)

        total_frame = cap.get(cv2.CAP_PROP_FRAME_COUNT)  # Total frame of Video File
        fps = cap.get(cv2.CAP_PROP_FPS)
        W = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
        H = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

        if total_frame <= int(fps)*N:
            raise ValueError('Please reduce N. The length of the video file is too short to slice.')

        sliceno = 1
        frame_count = 0
        frame_count_per_sec = 0

        while cap.isOpened():
            grabbed, frame = cap.read()

            if not grabbed:
                # print('cap is not grabbed. Processing ends.')
                break

            if int(int(total_frame) - int(frame_count)) == total_frame % int(fps)*N:
                # print('The rest of video file is too small. Processing ends.')
                break

            save_path = os.path.join(save_dir, video_name + '_' + str(sliceno) + '.mp4')
            fourcc = cv2.VideoWriter_fourcc(*'DIVX')

            if frame_count_per_sec == 0:
                writer = cv2.VideoWriter(save_path, fourcc, fps, (W, H), True)

            frame_count += 1
            frame_count_per_sec += 1
            # cv2.imshow('This is output', frame)
            writer.write(frame)

            key = cv2.waitKey(int(1000 / fps))
            if key == 27:
                # print('Esc pressed. Processing ends.')
                break

            if frame_count_per_sec >= int(fps)*N:
                writer.release()
                frame_count_per_sec = 0
                sliceno += 1

        cap.release()
        # cv2.destroyAllWindows()

# Slicing & Saving Video Files
file_dir = input('비디오 파일이 저장된 전체 경로를 입력하세요(file_dir) : ')
save_dir = input('잘라낸 비디오 파일을 저장할 경로를 입력하세요(save_dir) : ')
N = input('몇 초 단위로 자르시겠습니까?(N) : ')

slice_video(file_dir, save_dir, int(N))