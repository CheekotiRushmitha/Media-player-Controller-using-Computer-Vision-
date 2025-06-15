import cv2
import mediapipe as mp
import pyautogui
import time

# Disable the PyAutoGUI fail-safe
pyautogui.FAILSAFE = False

# Function to count the number of fingers for a single hand
def count_fingers(lst):
    cnt = 0
    thresh = (lst.landmark[0].y * 100 - lst.landmark[9].y * 100) / 2

    if (lst.landmark[5].y * 100 - lst.landmark[8].y * 100) > thresh:
        cnt += 1
    if (lst.landmark[9].y * 100 - lst.landmark[12].y * 100) > thresh:
        cnt += 1
    if (lst.landmark[13].y * 100 - lst.landmark[16].y * 100) > thresh:
        cnt += 1
    if (lst.landmark[17].y * 100 - lst.landmark[20].y * 100) > thresh:
        cnt += 1
    if (lst.landmark[5].x * 100 - lst.landmark[4].x * 100) > 6:
        cnt += 1

    return cnt

cap = cv2.VideoCapture(0)

drawing = mp.solutions.drawing_utils
hands = mp.solutions.hands
hand_obj = hands.Hands(max_num_hands=2)

start_init = False
prev = -1

while True:
    end_time = time.time()
    _, frm = cap.read()
    frm = cv2.flip(frm, 1)

    res = hand_obj.process(cv2.cvtColor(frm, cv2.COLOR_BGR2RGB))

    if res.multi_hand_landmarks:
        total_fingers = 0

        for hand_landmarks in res.multi_hand_landmarks:
            cnt = count_fingers(hand_landmarks)
            total_fingers += cnt
            drawing.draw_landmarks(frm, hand_landmarks, hands.HAND_CONNECTIONS)

        if prev != total_fingers:
            if not start_init:
                start_time = time.time()
                start_init = True
            elif (end_time - start_time) > 0.2:
                if total_fingers == 1:
                    pyautogui.press("right")
                elif total_fingers == 2:
                    pyautogui.press("left")
                elif total_fingers == 3:
                    pyautogui.press("up")
                elif total_fingers == 4:
                    pyautogui.press("down")
                elif total_fingers == 5:
                    pyautogui.press("space")
                elif total_fingers == 6:
                    pyautogui.press("esc")
                elif total_fingers == 7:
                    pyautogui.press("c")  # Assuming 'c' toggles subtitles on
                elif total_fingers == 8:
                    pyautogui.press("c")  # Assuming 'c' toggles subtitles off
                elif total_fingers == 9:
                    pyautogui.press("f")
                elif total_fingers == 10:
                    pyautogui.press("i")  # Example action for 10 fingers
                    
                prev = total_fingers
                start_init = False

    cv2.imshow("window", frm)

    # Custom fail-safe mechanism
    if cv2.waitKey(1) == 27:  # Press the 'Esc' key to exit
        cv2.destroyAllWindows()
        cap.release()
        break
