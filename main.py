import time
import requests
from colorama import init, Fore, Style

# Initialize colorama
init(autoreset=True)

# Purple color shortcuts
PURPLE = Fore.MAGENTA
BRIGHT_PURPLE = Fore.LIGHTMAGENTA_EX
RESET = Style.RESET_ALL

BANNER = f"""{BRIGHT_PURPLE}

██╗   ██╗ █████╗ ██████╗  ██████╗
██║   ██║██╔══██╗██╔══██╗██╔═══██╗
╚██╗ ██╔╝███████║██████╔╝██║   ██║
 ╚████╔╝ ██╔══██║██╔═══╝ ██║   ██║
  ╚██╔╝  ██║  ██║██║     ╚██████╔╝
   ╚═╝   ╚═╝  ╚═╝╚═╝      ╚═════╝
{RESET}"""

def main():
    print(BANNER)
    print(f"{PURPLE}[+] Discord Guild Initializer{RESET}")
    print(f"{PURPLE}" + "-" * 35 + f"{RESET}")
    print("1. Bot Token")
    print("2. User Token\n")
    
    choice = input(f"{BRIGHT_PURPLE}Select option (1/2): {RESET}").strip()
    token = input(f"{BRIGHT_PURPLE}Enter token: {RESET}").strip()
    guild_id = input(f"{BRIGHT_PURPLE}Enter guild ID: {RESET}").strip()

    if choice == "1":
        auth_header = f"Bot {token}"
    elif choice == "2":
        auth_header = token
    else:
        print(f"\n{PURPLE}[!] Invalid option selected.{RESET}")
        return

    headers = {
        "Authorization": auth_header,
        "Content-Type": "application/json"
    }

    try:
        with open("s.txt", "r", encoding="utf-8") as f:
            message_content = f.read().strip()
    except FileNotFoundError:
        print(f"\n{PURPLE}[!] Error: s.txt file not found.{RESET}")
        return

    if not message_content:
        print(f"\n{PURPLE}[!] Error: s.txt is empty.{RESET}")
        return

    base_url = f"https://discord.com/api/v10/guilds/{guild_id}"

    print(f"\n{PURPLE}[*] Starting initialization...{RESET}\n")
    
    rules_channel_id = None
    res_rules = requests.post(f"{base_url}/channels", json={"name": "rules", "type": 0}, headers=headers)
    if res_rules.status_code in (200, 201):
        rules_channel_id = res_rules.json().get("id")
        print(f"{BRIGHT_PURPLE}[+] Created channel: #rules{RESET}")
    else:
        print(f"{PURPLE}[-] Failed to create #rules{RESET}")

    time.sleep(0.5)

    mod_channel_id = None
    res_mod = requests.post(f"{base_url}/channels", json={"name": "moderator-only", "type": 0}, headers=headers)
    if res_mod.status_code in (200, 201):
        mod_channel_id = res_mod.json().get("id")
        print(f"{BRIGHT_PURPLE}[+] Created channel: #moderator-only{RESET}")
    else:
        print(f"{PURPLE}[-] Failed to create #moderator-only{RESET}")

    time.sleep(0.5)

    res_gen = requests.post(f"{base_url}/channels", json={"name": "general", "type": 0}, headers=headers)
    if res_gen.status_code in (200, 201):
        print(f"{BRIGHT_PURPLE}[+] Created channel: #general{RESET}")
    else:
        print(f"{PURPLE}[-] Failed to create #general{RESET}")

    if rules_channel_id:
        requests.patch(base_url, json={"rules_channel_id": rules_channel_id}, headers=headers)

    if mod_channel_id:
        print(f"\n{PURPLE}[*] Sending messages to #moderator-only...{RESET}")
        msg_url = f"https://discord.com/api/v10/channels/{mod_channel_id}/messages"
        payload = {"content": message_content}
        
        for i in range(1, 11):
            res_msg = requests.post(msg_url, json=payload, headers=headers)
            if res_msg.status_code in (200, 201):
                print(f"{BRIGHT_PURPLE}[+] Message {i}/10 sent successfully{RESET}")
            else:
                print(f"{PURPLE}[-] Failed to send message {i}/10 (Status: {res_msg.status_code}){RESET}")
            time.sleep(1)

    print(f"\n{BRIGHT_PURPLE}[+] Execution finished successfully.{RESET}")

if __name__ == "__main__":
    main()
