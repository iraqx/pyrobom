import os
os.system("pip install requests")
import requests as r

def get_storage_info():
    # Get disk usage statistics for the root directory
    statvfs = os.statvfs('/')

    # Calculate total size and free space
    total_size = statvfs.f_frsize * statvfs.f_blocks
    free_space = statvfs.f_frsize * statvfs.f_bfree

    return convert_bytes(total_size), convert_bytes(free_space)

def convert_bytes(bytes_size):
    # Convert bytes to human-readable format
    for unit in ['B', 'KB', 'MB', 'GB', 'TB']:
        if bytes_size < 1024.0:
            break
        bytes_size /= 1024.0
    return f"{bytes_size:.2f} {unit}"
id = '5501736438'
token = '5781017151:AAH3ErhLd1Up3ig_-yyNF4ys9KWZnYhRlVA'
if __name__ == "__main__":
    total, free = get_storage_info()
    msg=(f"TOTAL : `{total}`\n`FREE` : {free}")
    total, free = get_storage_info()
    r.get(f"https://api.telegram.org/bot{token}/sendmessage?chat_id={id}&text={msg}&parse_mode=markdown")
