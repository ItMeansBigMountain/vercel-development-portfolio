# from pynput.keyboard import Key, Controller, Listener
# import time
# import threading

# keyboard = Controller()
# running = True



# # count from 0-10
# def enum_f():
#     print("Enumerating") 
#     time.sleep(1.7)
#     with keyboard.pressed("f"):
#         time.sleep(6.5)
#         keyboard.release('f')


# # count up by one
# def increment_f():
#     print("Incrementing") 
#     time.sleep(2)
#     keyboard.press('f')
#     time.sleep(1.5)
#     keyboard.release('f')


# # moves to the right index and if at the end, then will start at the first index on the lefts
# def tap_f(): 
#     print("Tapping") 
#     time.sleep(1.2)
#     keyboard.press('f')
#     time.sleep(0.3)
#     keyboard.release('f')






# def run_in_app():
#     ...







# def on_press(key):
#     global running
#     if key == Key.esc:
#         running = False
#         return False




# # CALLING FUNCTIONS DOWN HERE
# for x in range(10, 0 , -1):
#     print("starting bot in: " , x)
#     time.sleep(1)



# # Set up listener for escape key
# listener = Listener(on_press=on_press)
# listener.start()

# # Start the loop in a separate thread so it can be interrupted by the listener
# app_thread = threading.Thread(target=run_in_app, args=())
# app_thread.start()






# for a in range(10):
#     for b in range(10):
#         for c in range(10):
#             for d in range(10):
#                 combination = [a, b, c, d]
#                 print(combination)






# for x in range(10, 0 , -1):
#     print("starting bot in: " , x)
#     time.sleep(1)


# array = [0, 0, 0, 0]
# length = len(array)

# while array[0] < 10:
#     # Print current combination
#     print(array)
    
#     # Increment the last index, and handle overflow
#     index = length - 1
#     while index >= 0:
#         array[index] += 1
#         if array[index] == 10 and index > 0:
#             array[index] = 0
#             index -= 1
#         else:
#             break










from pynput.keyboard import Key, Controller, Listener
import time
import threading

keyboard = Controller()
running = True

def enum_f():
    print("Enumerating")
    time.sleep(1.7)
    with keyboard.pressed("f"):
        time.sleep(6.5)
        keyboard.release('f')

def increment_f():
    print("Incrementing")
    time.sleep(2)
    keyboard.press('f')
    time.sleep(1.5)
    keyboard.release('f')

def tap_f():
    print("Tapping")
    time.sleep(1.2)
    keyboard.press('f')
    time.sleep(0.3)
    keyboard.release('f')

array = [0, 0, 0, 0]
length = len(array)

index = length - 1

while array[0] < 10:
    # Print current combination
    print(''.join(map(str, array)))

    if array[index] == 9:
        # Enumerate from 0 to 9 (reset the value at the current index)
        enum_f()
        array[index] = 0
        # Move to the next index (right), and loop back to 0 if at the end
        index = (index + 1) % length
    else:
        # Increment the value at the current index
        increment_f()
        array[index] += 1

    # Move to the next index (right), and loop back to 0 if at the end
    tap_f()
    index = (index + 1) % length
