import pygame
import time
import subprocess
from threading import Thread
from datetime import datetime

pygame.init()

joystick = pygame.joystick.Joystick(0)
joystick.init()


'''
Configuration Parameters
'''
interface = 'can0'
delay = 0.02
speed_max = 56  # 140 MPH
rpm_max = 7000


'''
Default Values
'''
gear = 1  # 1=Park, 2=Reverse, 3=Neutral, 4=Drive
rpm = 0
speed = 0
fuel_level = 0  # 0-255


def cansend(arb_id, value):
    command = f'cansend {interface} {arb_id}#{value}'
    subprocess.run(command, shell=True)


def toggleable(value, original):
    if value > 0:
        adj = round(255 * (1 - event.value))
        return adj if adj < original else original
    else:
        adj = round(255 * abs(event.value))
        return adj if adj > original else original


def broadcaster():
    while True:
        cansend(arb_id='0C9', value=f'00{rpm * 4:02X}000000000000')  # RPM
        cansend(arb_id='1F5', value=f'0F0F00{gear:02X}00000300')  # PRNDL


def gear_broadcaster():
    while True:
        cansend(arb_id='1F5', value=f'0F0F00{gear:02X}00000300')


Thread(target=broadcaster).start()
Thread(target=gear_broadcaster).start()


def button_handler(event, timestamp):
    if event.button <= 3:  # X O Square Triangle
        gear = event.button + 1
        print(f'[{timestamp}] Gear: {gear} - 1F5#0F0F00{gear:02X}00000300')


def joystick_handler(event, timestamp):
    if event.axis == 5:  # Right Trigger
        speed = round(max(0, (event.value + 1) / 2) * speed_max)
        cansend(arb_id='3E9', value=f'{speed:02X}400A9503004000')
        print(f'[{timestamp}] Speedometer: {speed * 2.5:,}mph (max_speed: {speed_max * 2.5}) - 3E9#{speed:02X}400A9503004000')
    if event.axis == 2:  # Left Trigger
        rpm = round(max(0, (event.value + 1) / 2) * rpm_max)
        print(f'[{timestamp}] Tachometer: {rpm:,}rpm (max_rpm: {rpm_max}) - 0C9#00{rpm * 4:02X}000000000000')
    if event.axis == 4:  # Right Joystick
        fuel_level = toggleable(event.value, fuel_level)
        cansend(arb_id='4D1', value=f'0000000000{fuel_level:02X}0000')
        print(f'[{timestamp}] Fuel Level: {fuel_level:,} (max_fuel: 255) - 4D1#0000000000{fuel_level:02X}0000')


def controller_listener():
    while True:
        for event in pygame.event.get():
            timestamp = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            if event.type == pygame.JOYBUTTONDOWN:
                button_handler(event, timestamp)
            if event.type == pygame.JOYAXISMOTION:
                joystick_handler(event, timestamp)


controller_listener()

