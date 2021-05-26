from time import sleep
import pyautogui as pt
import random
import pyperclip
import zeus

smile_emoji_path = 'C:\\Users\\mouaa\\PycharmProjects\\Bot\\images\\smiley_paperclip.png'
green_circle_path = 'C:\\Users\\mouaa\\PycharmProjects\\Bot\\images\\green_circle.png'
audio_btn_path = 'C:\\Users\\mouaa\\PycharmProjects\\Bot\\images\\new_audio.png'


sleep(5)

position1 = pt.locateOnScreen(smile_emoji_path, confidence=.6)
x = position1[0]
y = position1[1]


# Get message

def get_message():
    print("calling get message")
    global x, y
    position = pt.locateOnScreen(smile_emoji_path, confidence=.7)
    x = position[0]
    y = position[1]
    pt.moveTo(x, y, duration=.02)
    pt.moveTo(x + 74, y - 49, duration=.02)
    pt.tripleClick()
    pt.rightClick()
    pt.moveRel(60, -380)
    pt.click()
    whatsapp_message = pyperclip.paste()
    pt.moveTo(x + 40, y - 54, duration=.02)
    pt.click()
    print("Received message is:", whatsapp_message)
    return whatsapp_message


# post response
def post_response(message):
    global x, y
    position = pt.locateOnScreen(smile_emoji_path, confidence=.6)
    x = position[0]
    y = position[1]
    pt.moveTo(x + 200, y + 15, duration=.02)
    pt.typewrite(message, interval=.02)
    pt.click()
    pt.typewrite('\n', interval=.02)


# get response
def process_response(message):
    answer = ''
    links = ['http', '.com', '.net', '.org']
    if any(x in message for x in links):
        answer = "Sorry, I can't open links for security reasons!"
    elif message == '' or message == ' ':
        answer = '^_^'
    else:
        answer = zeus.zeus_response(message)

    return answer

# checking for new messages
def check_for_messages():
    pt.moveTo(x + 74, y - 49, duration=.25)

    while True:
        try:
            if pt.pixelMatchesColor(int(x + 74), int(y - 49), (255, 255, 255), tolerance=20):
                audio_position = pt.locateOnScreen(audio_btn_path, confidence=.7)
                if audio_position is not None:
                    post_response("I don't process audio yet.")
                    print("audio received.")
                else:
                    print("New message is detected.")
                    message = get_message()
                    answer = process_response(message)
                    post_response(answer)
                    print("sent answer:", answer)

        except Exception as err:
            print("Error:", err)

        # continuously checks for the green circle on the screen and new messages
        try:
            position = pt.locateOnScreen(green_circle_path, region=(0, 0, 680, 1000), confidence=.7)
            if position is not None:
                pt.moveTo(position)
                pt.moveRel(-100, 0)
                pt.click()
                sleep(.05)
        except Exception as Err:
            print("No New Notifications.", Err)

        sleep(.25)


check_for_messages()
