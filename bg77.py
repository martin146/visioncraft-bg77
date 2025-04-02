import sys
import time

import services
import serial
import re
from consts import *

def get_bands(bands: list) -> int:
    ret = 0
    for band in bands:
        if band in BANDS:
            ret |= BANDS[band]
    if ret == 0:
        ret = 0x4000000000000000000000
    return ret


def get_mode(mode: str) -> int:
    ret = 2
    if mode in MODES:
        ret = MODES[mode]
    return ret


class BG77:
    def __init__(self):
        try:
            self.ser = serial.Serial(port=services.config.config[PORT],
                                     baudrate=services.config.config[SPEED],
                                     dsrdtr=True,
                                     rtscts=True,
                                     timeout=0.2)
        except serial.SerialException as e:
            services.logger.error(f'Serial Exception: {e}')
            sys.exit(-1)

    def send_command(self, command: str) -> str:
        command = command + '\r\n'
        self.ser.write(command.encode())
        rec = self.ser.read(512)
        rec = re.sub(r'[\r\n]+', ' ', rec.decode().strip())
        services.logger.debug(rec)
        return rec

    def send_command_timeout(self, command: str, timeout: float) -> str:
        ticks = int(timeout / self.ser.timeout)
        i = 0
        command = command + '\r\n'
        self.ser.write(command.encode())
        while True:
            rec = self.ser.read(512)
            if len(rec) > 0:
                rec = re.sub(r'[\r\n]+', ' ', rec.decode().strip())
                services.logger.debug(rec)
                if 'OK' in rec or 'ERROR' in rec:
                    break
            if i >= ticks:
                services.logger.error('CMD TIMEOUT')
                break
            time.sleep(self.ser.timeout)
            i += 1
        return rec

    def wait_for_reg(self, reg_timeout: int) -> bool:
        start = time.time()
        while time.time() - start < reg_timeout:
            rec = self.send_command('AT+CGATT?')
            if '+CGATT: 1' in rec:
                return True
            time.sleep(0.5)
        return False

    def get_reg_status(self) -> None:
        rec = self.send_command('AT+CGATT?')
        if '+CGATT: 1' in rec:
            print('ATTACHED')
        else:
            print('DETACHED')

    def get_signal_stats(self) -> None:
        rec = self.send_command('AT+QCSQ')
        rec_list = re.split('[ ,]', rec.strip())

        if '+QCSQ:' in rec_list:
            idx = rec_list.index('+QCSQ:')
            tech = rec_list[idx + 1].replace('"', '')
            rssi = rec_list[idx + 2]
            rsrp = rec_list[idx + 3]
            sinr = int(rec_list[idx + 4]) / 5 - 20
            rsrq = int(rec_list[idx + 5])
            print(f'Tech: {tech}, RSSI: {rssi} dBm, RSRP: {rsrp} dBm, SINR: {sinr:.2f} dB, RSRQ: {rsrq}')

    def reg_to_network(self) -> None:
        bands = get_bands(services.config.config[BAND])
        mode = get_mode(services.config.config[TECH])
        plmn = services.config.config[PLMN]
        self.send_command_timeout('AT+CFUN=0', 2)
        self.send_command(f'AT+QCFG="iotopmode",{mode},1')
        self.send_command(f'AT+QCFG="band",0,{hex(bands)},{hex(bands)},1')
        self.send_command_timeout('AT+CFUN=1', 5)
        self.send_command(f'AT+CGDCONT=1,"IP","{services.config.config[APN]}"')
        if plmn == 'AUTO':
            self.send_command('AT+COPS=0')
        else:
            self.send_command(f'AT+COPS=1,2,"{plmn}"')
        if self.wait_for_reg(services.config.config[REG_TOUT]):
            print('ATTACHED')
        else:
            print('DETACHED')
            self.send_command_timeout('AT+CFUN=0', 2)