import os
import shutil
import time
import ctypes

# Определим функцию, которая будет проверять, вставлена ли флешка
def is_usb_connected():
    drive_list = []
    drivebits = ctypes.windll.kernel32.GetLogicalDrives()
    for i in range(26):
        if drivebits & (1 << i):
            drive = chr(65 + i)
            drive_type = ctypes.windll.kernel32.GetDriveTypeW(f"{drive}:\\")
            if drive_type == 2:  # DRIVE_REMOVABLE
                drive_list.append(f"{drive}:\\")
    return drive_list

# Определим функцию для копирования файлов и папок с флешки в указанную папку
def copy_files_from_usb(source_dir, destination_dir):
    try:
        print(f"Копирование файлов с {source_dir} в {destination_dir}")
        for root, dirs, files in os.walk(source_dir):
            for file in files:
                source_file = os.path.join(root, file)
                dest_file = os.path.join(destination_dir, os.path.relpath(source_file, source_dir))
                dest_dir = os.path.dirname(dest_file)
                os.makedirs(dest_dir, exist_ok=True)
                shutil.copy2(source_file, dest_file)
        print("Файлы и папки успешно скопированы!")
    except Exception as e:
        print(f"Ошибка при копировании файлов: {e}")

# Определим основную функцию, которая будет мониторить флешки
def monitor_usb():
    while True:
        print("Проверка подключенных USB устройств...")
        connected_usb_drives = is_usb_connected()
        print("Подключенные USB устройства:", connected_usb_drives)
        if connected_usb_drives:
            for usb_drive in connected_usb_drives:
                try:
                    # Проверяем, что устройство является съемным носителем (флешкой)
                    drive_type = ctypes.windll.kernel32.GetDriveTypeW(usb_drive)
                    if drive_type == 2:  # DRIVE_REMOVABLE
                        source_dir = usb_drive
                        destination_dir = "C:\\ProgramData\\files"  # Укажите путь к папке назначения
                        copy_files_from_usb(source_dir, destination_dir)
                except Exception as e:
                    print(f"Ошибка при обработке USB устройства: {e}")
        else:
            print("Нет подключенных USB устройств.")
        print("Ждем 10 минут перед следующей проверкой...")
        time.sleep(300)  # Подождать 5 минут (300 секунд)

# Запустим основную функцию
monitor_usb()
