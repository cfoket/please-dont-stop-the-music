import time
import psutil
import win32api
import win32con
import win32process

import toolkit

def chase_pointer(process_handle, address, offsets):

    try:

        offset, *offsets = offsets
        address += offset

        for offset in offsets:

            address = win32process.ReadProcessMemory(process_handle, address, 8)
            address = int.from_bytes(address, byteorder='little')
            address += offset

        return address

    except: return None

def get_current_song():

    for pid in toolkit.get_window_process_ids('GDI+ Window (Spotify.exe)'):

        process_handle = win32api.OpenProcess(
            win32con.PROCESS_ALL_ACCESS, False, pid)

        try:

            for module in psutil.Process(pid).memory_maps(False):

                if module.path.endswith('libcef.dll'):

                    memory_address = chase_pointer(
                        process_handle, int(module.addr, 16),
                        [0x0C2BD6D8, 0x18, 0x8, 0x20, 0x0])

                    if memory_address:

                        data = win32process.ReadProcessMemory(
                            process_handle, memory_address, 256)

                        data, *_ = data.split(b'\x00\x00\x00')
                        data += b'\x00'
                        data = data.split(b' \x00"  \x00')
                        data = [entry.decode('utf-16') for entry in data]

                        return data

        finally: win32api.CloseHandle(process_handle)

    return []

def main():

    while True:

        with open('song.html', 'w') as fp:

            current_song = get_current_song()
            print(current_song)
            fp.write("<br/>".join(current_song))

        time.sleep(1)

main()
