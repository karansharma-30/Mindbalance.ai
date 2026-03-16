import datetime
import subprocess
import time
import random
from colorama import Fore, init

init(autoreset=True)

# -----------------------------
# CONFIG
# -----------------------------

friends = ["Kathan Phone", "Priyansh Device"]
BED_HOUR = 23
BED_MINUTE = 30
social_apps = {
    "com.instagram.android": "Instagram",
    "com.google.android.youtube": "YouTube",
    "com.snapchat.android": "Snapchat",
    "com.facebook.katana": "Facebook"
}

# -----------------------------
# STATS
# -----------------------------

wellness = 50
dopamine = 30

scroll_start = None
current_app = None

lock_until = None
locked_app = None

idle_start = None
last_idle_reward = 0
last_friend_reward = 0

scan_shown = False

reality_rewards = 0
friends_detected = 0
idle_rewards = 0
detox_events = 0

usage = {
    "Instagram": 0,
    "YouTube": 0,
    "Snapchat": 0,
    "Facebook": 0
}

idle_log = []

# -----------------------------
# UTILITY FUNCTIONS
# -----------------------------

def run(cmd):
    try:
        return subprocess.check_output(cmd, shell=True).decode()
    except:
        return ""

def clear():
    print("\033[2J\033[H", end="")

def get_screen():
    out = run("adb shell dumpsys power | grep 'Display Power'")
    return "ON" in out

def get_app():
    return run("adb shell dumpsys activity activities | grep mResumedActivity")

def bluetooth():
    out = run("adb shell dumpsys bluetooth_manager | grep enabled")
    return "true" in out.lower()

def battery():
    out = run("adb shell dumpsys battery | grep level")
    if ":" in out:
        return out.split(":")[1].strip()
    return "?"

def meter(v):
    bars = int(v/5)
    return "[" + "█"*bars + "░"*(20-bars) + "]"

def risk(sec):
    if sec < 5:
        return "LOW"
    elif sec < 10:
        return "MEDIUM"
    else:
        return "HIGH"

def bedtime_countdown():
    now = datetime.datetime.now()

    bedtime = now.replace(
        hour=BED_HOUR,
        minute=BED_MINUTE,
        second=0,
        microsecond=0
    )

    if now > bedtime:
        return "Bedtime Mode Active"

    remaining = bedtime - now
    total = int(remaining.total_seconds())

    hours = total // 3600
    minutes = (total % 3600) // 60

    return f"{hours}h {minutes}m"

# -----------------------------
# STARTUP ANIMATION
# -----------------------------

print("\nMindBalance AI Initializing...\n")
time.sleep(1)
print("Loading Cognitive Engine...")
time.sleep(1)
print("Loading Reality Bridge...")
time.sleep(1)
print("Connecting Device Interface...\n")
time.sleep(1)

# -----------------------------
# MAIN LOOP
# -----------------------------

try:

    while True:

        clear()

        screen = get_screen()
        bt = bluetooth()
        bat = battery()
        app_data = get_app()

        print(Fore.YELLOW + "========== MindBalance AI ==========")
        print("Device Monitor")
        print("------------------------------------")
        print(Fore.MAGENTA + "Bedtime Lock :", bedtime_countdown())
        print("Screen State :", "ACTIVE" if screen else "OFF")
        print("Bluetooth    :", "ON" if bt else "OFF")
        print("Battery      :", bat + "%")

        print("\nDigital Health")
        print("------------------------------------")
        print("Wellness :", wellness)
        print("Dopamine :", meter(dopamine), dopamine, "%")

# ------------------------------------------------
# ACTIVE MODE
# ------------------------------------------------

        if screen:

            print(Fore.GREEN + "\nMODE : ACTIVE MONITORING")

            idle_start = None
            scan_shown = False

            detected = None

            for pkg in social_apps:
                if pkg in app_data:
                    detected = pkg
                    break

            if lock_until and time.time() < lock_until:

                remain = int(lock_until - time.time())

                print("\nDetox Lock Active")
                print("Blocked App :", locked_app)
                print("Unlock In   :", remain, "sec")

                if detected:
                    subprocess.run(
                        f"adb shell am force-stop {detected}",
                        shell=True
                    )

            else:

                locked_app = None
                lock_until = None

                if detected:

                    if current_app != detected:
                        current_app = detected
                        scroll_start = time.time()
                        usage[social_apps[detected]] += 1

                    sec = int(time.time() - scroll_start)

                    print("\nActive App Monitor")
                    print("App      :", social_apps[detected])
                    print("Session  :", sec, "sec")
                    print("Scroll Risk :", risk(sec))

                    dopamine = min(dopamine + 2, 100)

                    if sec > 15:

                        subprocess.run(
                            f"adb shell am force-stop {detected}",
                            shell=True
                        )

                        locked_app = social_apps[detected]
                        lock_until = time.time() + 30

                        detox_events += 1

                        current_app = None
                        scroll_start = None

                else:
                    current_app = None
                    scroll_start = None

            print("\nApp Usage Counter")
            for k, v in usage.items():
                print(k, ":", v)

            time.sleep(3)

# ------------------------------------------------
# IDLE MODE
# ------------------------------------------------

        else:

            print(Fore.CYAN + "\nMODE : RECOVERY + REALITY BRIDGE")

            if idle_start is None:
                idle_start = time.time()

            idle = int(time.time() - idle_start)

            print("\nIdle Timer :", idle, "sec")

            if idle - last_idle_reward >= 15:

                idle_rewards += 1
                last_idle_reward = idle

                idle_log.append(
                    f"{idle}s : Screen Idle +1 Wellness"
                )

                wellness += 1

            if idle >= 27 and not scan_shown and bt:

                print("\nReality Bridge Scanner")
                print("Scanning nearby devices .")
                time.sleep(0.4)
                print("Scanning nearby devices ..")
                time.sleep(0.4)
                print("Scanning nearby devices ...")

                scan_shown = True

            if idle - last_friend_reward >= 30 and bt:

                friend = random.choice(friends)

                reality_rewards += 2
                friends_detected += 1

                wellness += 2

                idle_log.append(
                    f"{idle}s : Friend detected ({friend}) +2"
                )

                last_friend_reward = idle

            print("\nReality Bridge Stats")
            print("Friends Detected :", friends_detected)
            print("Interaction Points :", reality_rewards)
            print("Idle Rewards :", idle_rewards)

            print("\nRecent Idle Events")

            for log in idle_log[-5:]:
                print(log)

            dopamine = max(dopamine - 1, 0)

            time.sleep(4)

# ------------------------------------------------
# EXIT SUMMARY
# ------------------------------------------------

except KeyboardInterrupt:

    clear()

    print("========== MindBalance AI Report ==========\n")

    print("Detox Control")
    print("--------------------------------")
    print("Detox Locks Triggered :", detox_events)

    print("\nIdle Recovery")
    print("--------------------------------")
    print("Idle Rewards :", idle_rewards)

    print("\nReality Bridge")
    print("--------------------------------")
    print("Friends Detected :", friends_detected)
    print("Interaction Points :", reality_rewards)

    print("\nDigital Health")
    print("--------------------------------")
    print("Final Wellness :", wellness)
    print("Final Dopamine :", dopamine)

    print("\nToday's Session Finished Successfully\n")
