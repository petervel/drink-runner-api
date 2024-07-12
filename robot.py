import cyberpi 
import time
import urequests

BLINK_SPEED = 0.5
WIFI_SSID = "De Vluchte"
WIFI_PASS = "inloopkoelkast"

WEB_SERVER_IP = "http://bingo-barry.nl/bonk"
WEB_SERVER_PORT = 80


def print_msg(msg: str, color: str | None = None, clear: bool = True) -> None:
    if clear:
        cyberpi.console.clear()
    if color == 'r' or color == 'red':
        cyberpi.display.set_brush(255, 0, 0)
    elif color == 'g' or color == 'green':
        cyberpi.display.set_brush(0, 255, 0)
    elif color == 'b' or color == 'blue':
        cyberpi.display.set_brush(0, 0, 255)
    else:
        cyberpi.display.set_brush(255, 255, 255)
    cyberpi.console.println(msg)


def print_error(msg: object) -> None:
    print_msg("err: " + repr(msg), 'red')
    time.sleep(3)


def print_board_details() -> None:
    print_msg("mac addr: " + repr(cyberpi.get_mac_address()), clear=True)
    print_msg("firm v. : " + repr(cyberpi.get_firmware_version()), clear=False)
    print_msg("batt lev: " + repr(cyberpi.get_battery()), clear=False)
    time.sleep(1)


def connect_wifi(ssid: str, password: str, connected_msg_delay: int = 2) -> None:
    led_on = False
    print_msg("Connecting with WiFi ...", 'blue')
    cyberpi.wifi.connect(ssid, password)
    while not cyberpi.wifi.is_connect():
        if led_on:
            cyberpi.led.off()
        else:
            cyberpi.led.on("blue")
        led_on = not led_on
        time.sleep(BLINK_SPEED)
    
    print_msg("WiFi connected!", 'green')
    if connected_msg_delay > 0:
        cyberpi.led.on("green")
        time.sleep(connected_msg_delay)
    cyberpi.led.off()


def http_get():
    if not cyberpi.wifi.is_connect():
        raise Exception("http_get() > Not connected to Wifi!")

    # Make a GET request
    response = urequests.get(WEB_SERVER_IP)

    return response.text


# try:
#     print_board_details()
#     connect_wifi(WIFI_SSID, WIFI_PASS)
#     while True:
#         response = http_get()
#         print_msg("HTTP body:\r" + response, color='green')
#         time.sleep(3)
# except Exception as e:
#     print_error(e)

driving = False
speed = 20

# Returns 4 bits with 1s for each sensor that sensed the line, and 0s for each sensor that sensed the background.
# E.g: With line_is_white set to True, if the (white) line is in the middle, you get 0b0110
# When the line is on the left, you may get 0b1100
# The threshold may need to be tweaked depending on the background and line brightness.
# Note: Cyberpi has a built in function for this, but it doesn't work well on a dark background with a white line.
def get_line_bits(line_is_white, threshold = 50):
    val = 0
    multiplier = 1
    if not line_is_white:
        multiplier = -1
        threshold *= multiplier
    if cyberpi.quad_rgb_sensor.get_gray("L2") * multiplier > threshold:
        val += 8
    if cyberpi.quad_rgb_sensor.get_gray("L1") * multiplier > threshold:
        val += 4
    if cyberpi.quad_rgb_sensor.get_gray("R1") * multiplier > threshold:
        val += 2
    if cyberpi.quad_rgb_sensor.get_gray("R2") * multiplier > threshold:
        val += 1
    return val
    

while True:
    try:
        print_board_details()
        connect_wifi(WIFI_SSID, WIFI_PASS)

    except Exception as e:
        print_error(e)

    # Start driving when we press A.
    if cyberpi.controller.is_press('a'):
        driving = True
        cyberpi.console.println("Driving")
        
    # Stop driving when we press B.
    if cyberpi.controller.is_press("b"):
        driving = False
        cyberpi.console.println("Stop driving")
        cyberpi.mbot2.drive_power(0, 0)
        
    if driving:
        left_speed_multiplier = 1
        right_speed_multiplier = 1
        
        # Check where the line is sensed, configured for following a white line with a black background
        detected_line_bit_mask = get_line_bits(True, 50)
        
        # Turn left when we detect the line on the left
        # When we detect white only the left side
        if detected_line_bit_mask == 0b1000 or detected_line_bit_mask == 0b0100:
            left_speed_multiplier = 0
        elif detected_line_bit_mask == 0b1100:
            left_speed_multiplier = -1
           
        # Turn right when we detect the line on the right
        if detected_line_bit_mask == 0b0001 or detected_line_bit_mask == 0b0010:
            right_speed_multiplier = 0
        elif detected_line_bit_mask == 0b0011:
            right_speed_multiplier = -1
            
        # If we don't detect the line go back by half the speed
        if detected_line_bit_mask == 0:
            left_speed_multiplier = -0.5
            right_speed_multiplier = -0.5

        # If no special line cases are hit, we just keep moving forward
        # as the line is where we expect it to be (one or both of the center sensors)

        # The right wheel motor has to spin in te reverse direction to moe forward
        cyberpi.mbot2.drive_power(speed * left_speed_multiplier, -speed * right_speed_multiplier)
        
        # Keep going back for a second when we lost the line.
        if detected_line_bit_mask == 0:
            time.sleep(1)
