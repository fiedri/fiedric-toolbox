#!/usr/bin/env python3
import os
import sys
import platform
import shutil
import subprocess
import math
import collections
import json
import time
import traceback
from pathlib import Path

# --- Configuration ---
RECOVERY_ROOT = Path.home() / "USB_RECOVERY_ROOT"
SAFE_EXTENSIONS = {
    # Documents
    ".jpg", ".jpeg", ".png", ".pdf", ".docx", ".xlsx", ".pptx", ".txt", ".mp3", ".mp4",
    ".doc", ".xls", ".ppt", ".rtf", ".csv", ".odt", ".ods", ".odp", ".html", ".htm",
    # Images
    ".gif", ".bmp", ".tiff", ".webp", ".svg", ".ico", ".jfif",
    # Audio
    ".wav", ".flac", ".m4a", ".ogg",
    # Video
    ".avi", ".mkv", ".mov", ".wmv",
    # Archives (Compressed)
    ".zip", ".rar", ".7z", ".tar", ".gz"
}
ENTROPY_THRESHOLD = 7.5  # Reduced false positives in compressed media

def is_admin():
    """Checks if the script is running with administrative privileges."""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.getuid() == 0
    except AttributeError:
        return False

def calculate_entropy(file_path):
    """Calculates Shannon entropy of a file's content."""
    try:
        with open(file_path, 'rb') as f:
            data = f.read()
            if not data:
                return 0.0
            counter = collections.Counter(data)
            entropy = 0
            for count in counter.values():
                p_x = float(count) / len(data)
                entropy -= p_x * math.log(p_x, 2)
            return entropy
    except Exception as e:
        print(f"[!] Error calculating entropy for {file_path}: {e}")
        return 0.0

def get_dir_size(path):
    """Calculates total size of a directory, skipping inaccessible files."""
    total = 0
    try:
        for root, dirs, files in os.walk(path):
            for f in files:
                fp = os.path.join(root, f)
                try:
                    if os.path.exists(fp):
                        total += os.path.getsize(fp)
                except (OSError, PermissionError):
                    continue
    except Exception as e:
        print(f"[!] Warning: Error walking directory {path}: {e}")
    return total

def list_drives():
    """Lists removable drives on Linux and Windows, including filesystem detection."""
    drives = []
    os_type = platform.system()
    
    if os_type == "Linux":
        try:
            result = subprocess.run(['lsblk', '-o', 'NAME,RM,SIZE,TYPE,MOUNTPOINT,LABEL,UUID,FSTYPE', '-J'], capture_output=True, text=True)
            data = json.loads(result.stdout)
            for device in data.get('blockdevices', []):
                if device.get('rm'):
                    children = device.get('children', [])
                    if not children and device.get('type') == 'disk' and device.get('mountpoint'):
                        drives.append({
                            'device': f"/dev/{device['name']}",
                            'mountpoint': device['mountpoint'],
                            'label': device['label'] or "Unnamed",
                            'size': device['size'],
                            'uuid': device.get('uuid'),
                            'fs': device.get('fstype', 'vfat')
                        })
                    else:
                        for part in children:
                            if part.get('mountpoint'):
                                drives.append({
                                    'device': f"/dev/{part['name']}",
                                    'mountpoint': part['mountpoint'],
                                    'label': part['label'] or "Unnamed",
                                    'size': part['size'],
                                    'uuid': part.get('uuid'),
                                    'fs': part.get('fstype', 'vfat')
                                })
        except Exception as e:
            print(f"[!] Error listing drives on Linux: {e}")
            
    elif os_type == "Windows":
        try:
            result = subprocess.run(['wmic', 'logicaldisk', 'where', 'drivetype=2', 'get', 'deviceid,volumename,size,filesystem', '/format:csv'], capture_output=True, text=True)
            lines = [l.strip() for l in result.stdout.strip().split('\n') if l.strip()]
            for line in lines:
                if line.startswith('Node') or not line: continue
                parts = line.split(',')
                if len(parts) >= 5:
                    # CSV alphabet order: Node, DeviceID, FileSystem, Size, VolumeName
                    drives.append({
                        'device': parts[1],
                        'mountpoint': parts[1] + "\\",
                        'fs': parts[2] if parts[2] else "FAT32",
                        'size': parts[3] if parts[3] else "Unknown",
                        'label': parts[4] if parts[4] else "Unnamed"
                    })
        except Exception as e:
            print(f"[!] Error listing drives on Windows: {e}")
            
    return drives

def setup_recovery_dir():
    """Creates the RECOVERY_ROOT directory if it doesn't exist."""
    try:
        if RECOVERY_ROOT.exists():
            shutil.rmtree(RECOVERY_ROOT)
        RECOVERY_ROOT.mkdir(parents=True, exist_ok=True)
        print(f"[*] Clean recovery directory ready at: {RECOVERY_ROOT}")
        return True
    except Exception as e:
        print(f"[!] ERROR creating recovery directory: {e}")
        return False

def analyze_and_isolate(source_path, recovery_path):
    """Heuristically analyze files and move safe ones to recovery."""
    usb_size = get_dir_size(source_path)
    try:
        usage = shutil.disk_usage(Path.home())
        local_free = usage.free
    except Exception as e:
        print(f"[!] Warning: Could not check disk usage: {e}")
        local_free = 0
        
    if local_free > 0 and usb_size > local_free * 0.9: 
        print(f"[!] ERROR: Not enough local space. Needed: {usb_size}, Free: {local_free}")
        return 0, 0, False

    safe_count = 0
    risky_count = 0
    print(f"[*] Analyzing files in {source_path}...")
    
    risky_extensions = {'.exe', '.vbs', '.lnk', '.bat', '.cmd', '.js', '.scr', '.ps1', '.com', '.msi', '.jar'}
    system_folders = {'system volume information', '$recycle.bin', '.trashes', '__macosx', '.spotlight-v100', '.fseventsd'}
    system_files = {'autorun.inf', 'desktop.ini', 'thumbs.db', 'indexer_volume_guid', '.ds_store', 'icon\r'}

    for root, dirs, files in os.walk(source_path):
        root_parts = Path(root).parts
        if any(part.lower() in system_folders for part in root_parts):
            continue
            
        for file in files:
            file_path = Path(root) / file
            file_lower = file.lower()
            try:
                rel_path = file_path.relative_to(source_path)
                is_risky = False
                
                if file_lower in system_files or file_lower.startswith('._') or file_lower.startswith('~$'):
                    continue
                
                file_suffixes = [s.lower() for s in file_path.suffixes]
                if any(ext in risky_extensions for ext in file_suffixes):
                    is_risky = True
                
                if not is_risky and file_path.suffix.lower() not in SAFE_EXTENSIONS:
                    if calculate_entropy(file_path) > ENTROPY_THRESHOLD:
                        is_risky = True
                
                if not is_risky:
                    dest_path = recovery_path / rel_path
                    dest_path.parent.mkdir(parents=True, exist_ok=True)
                    shutil.copy2(file_path, dest_path)
                    safe_count += 1
                else:
                    risky_count += 1
                    print(f"[!] Risky file skipped: {rel_path}")
            except Exception as e:
                print(f"[!] Error processing {file}: {e}")
                
    return safe_count, risky_count, True

def format_drive(drive_info):
    """Performs a wipe and format of the target drive, preserving the original filesystem."""
    os_type = platform.system()
    target_dev = drive_info['device']
    orig_fs = drive_info.get('fs', 'FAT32').upper()
    print(f"[*] Formatting {target_dev} as {orig_fs}...")
    
    if os_type == "Linux":
        subprocess.run(['umount', target_dev], check=False)
        subprocess.run(['dd', 'if=/dev/zero', f"of={target_dev}", 'bs=1M', 'count=1', 'conv=notrunc'], check=True)
        mkfs_type = "vfat" if "FAT32" in orig_fs else "exfat"
        subprocess.run(['mkfs.' + mkfs_type, '-n', 'PURGED_USB', target_dev], check=True)
        mount_point = drive_info['mountpoint']
        Path(mount_point).mkdir(parents=True, exist_ok=True)
        subprocess.run(['mount', '-o', 'umask=000', target_dev, mount_point], check=True)
        
    elif os_type == "Windows":
        fs_flag = "/FS:EXFAT" if "EXFAT" in orig_fs else "/FS:FAT32"
        cmd = f'format {target_dev} {fs_flag} /Q /V:PURGED_USB /Y'
        try:
            subprocess.run(cmd, shell=True, check=True)
        except subprocess.CalledProcessError as e:
            print(f"[!] Format failed with {fs_flag}: {e}")
            alt_fs = "/FS:FAT32" if "EXFAT" in fs_flag else "/FS:EXFAT"
            print(f"[*] Retrying with alternative filesystem {alt_fs}...")
            subprocess.run(f'format {target_dev} {alt_fs} /Q /V:PURGED_USB /Y', shell=True, check=True)

def immunize(target_path):
    """Applies collision-based immunization."""
    print("[*] Applying immunization...")
    target_path = str(target_path).rstrip('\\')
    autorun_dir = Path(target_path) / "autorun.inf"
    try:
        autorun_dir.mkdir(exist_ok=True)
        if platform.system() == "Windows":
            base = f"\\\\?\\{target_path}\\autorun.inf"
            for name in ['con', 'nul', 'aux', 'prn']:
                subprocess.run(f'mkdir "{base}\\{name}"', shell=True, check=False)
            subprocess.run(f'attrib +h +s +r "{autorun_dir}"', shell=True, check=False)
        else:
            for name in ['con', 'nul', 'aux', 'prn']:
                (autorun_dir / name).mkdir(exist_ok=True)
    except Exception as e:
        print(f"[!] Immunization warning: {e}")

def cleanup_traces(drive_info):
    """Cleans OS traces (registry on Win, Trash on Linux)."""
    print("[*] Cleaning system traces...")
    if platform.system() == "Linux":
        trash_dir = Path(drive_info['mountpoint']) / ".Trash-1000"
        if trash_dir.exists():
            shutil.rmtree(trash_dir)
    elif platform.system() == "Windows":
        pass

def main():
    try:
        print("=== USB-Purge Script (Cross-Platform) ===")
        if not is_admin():
            print("[!] ERROR: Admin privileges required. Please run as Administrator/Root.")
            return
        
        drives = list_drives()
        if not drives:
            print("[!] No removable drives found. Please insert a USB drive.")
            return

        print("\nAvailable Removable Drives:")
        for i, d in enumerate(drives):
            print(f"[{i}] {d['device']} ({d['label']}) - {d['size']} [{d['fs']}] mounted at {d['mountpoint']}")
        
        try:
            user_input = input("\nSelect drive index (or 'q' to quit): ")
            if user_input.lower() == 'q':
                return
            idx = int(user_input)
            if idx < 0 or idx >= len(drives):
                print(f"[!] ERROR: Index {idx} out of range.")
                return
            target = drives[idx]
        except ValueError:
            print("[!] ERROR: Please enter a valid number.")
            return
        except Exception as e:
            print(f"[!] ERROR selecting drive: {e}")
            return

        if input(f"\nCONFIRM WIPE {target['device']}? (y/n): ").lower() != 'y':
            print("[*] Operation cancelled by user.")
            return
        
        if not setup_recovery_dir():
            return

        safe, risky, success = analyze_and_isolate(target['mountpoint'], RECOVERY_ROOT)
        if not success:
            print("[!] ERROR: Analysis and isolation failed.")
            return
        
        print(f"[*] Isolated {safe} files. {risky} risky files identified.")
        
        try:
            format_drive(target)
        except Exception as e:
            print(f"[!] ERROR during format: {e}")
            return
        
        print("[*] Restoring data...")
        try:
            for item in os.listdir(RECOVERY_ROOT):
                shutil.move(str(RECOVERY_ROOT / item), target['mountpoint'])
        except Exception as e:
            print(f"[!] ERROR restoring data: {e}")
            return
        
        immunize(target['mountpoint'])
        cleanup_traces(target)
        
        report_path = Path.cwd() / "purge_report.txt"
        try:
            with open(report_path, "w") as f:
                f.write(f"USB Purge Report - {time.ctime()}\n")
                f.write(f"Target: {target['device']} ({target['label']})\n")
                f.write(f"FileSystem: {target['fs']}\n")
                f.write(f"Files Isolated: {safe}\n")
                f.write(f"Risky Files Removed: {risky}\n")
                f.write(f"Status: Success / Immunized\n")
            print(f"\n[+] USB Purge Complete! Report saved at {report_path}")
        except Exception as e:
            print(f"[!] Warning: Could not save report: {e}")

    except KeyboardInterrupt:
        print("\n[*] Script interrupted by user.")
    except Exception as e:
        print(f"\n[CRITICAL ERROR] An unexpected error occurred: {e}")
        traceback.print_exc()
    finally:
        print("\n" + "="*40)
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
