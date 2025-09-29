#!/usr/bin/env python3
import sys, requests, time, random

SITES = {
    # social
    "github": "https://github.com/{}",
    "gitlab": "https://gitlab.com/{}",
    "instagram": "https://instagram.com/{}",
    "tiktok": "https://www.tiktok.com/@{}",
    "x": "https://x.com/{}",
    "facebook": "https://www.facebook.com/{}",
    "linkedin": "https://www.linkedin.com/in/{}",
    "reddit": "https://www.reddit.com/user/{}",
    "pinterest": "https://www.pinterest.com/{}",
    "snapchat": "https://www.snapchat.com/add/{}",
    "telegram": "https://t.me/{}",
    # music
    "spotify": "https://open.spotify.com/user/{}",
    "soundcloud": "https://soundcloud.com/{}",
    "youtube": "https://www.youtube.com/@{}",
    # developer
    "stackoverflow": "https://stackoverflow.com/users/{}",
    "devto": "https://dev.to/{}",
    "bitbucket": "https://bitbucket.org/{}",
    "sourceforge": "https://sourceforge.net/u/{}",
    "figma": "https://www.figma.com/@{}", 
    # gaming
    "steam": "https://steamcommunity.com/id/{}",
    "twitch": "https://www.twitch.tv/{}",
    "epicgames": "https://www.epicgames.com/id/{}",
}

def generate_variations(base):
    """ first : base (original input) """
    u_variations = [base]
    for i in range(len(base)):
        u_variations.append(base[:i] + base[i]*2 + base[i+1:])
    for i in range(2, 6):
        """ range 2...6 """
        u_variations.append(base + base[-1] * i)
    u_variations.extend([base + "1", base + "123", base + "007", base + "_", base + ".", base + "_dev"])
    return list(dict.fromkeys(u_variations))

def check_username(username):
    u_found = []
    session = requests.Session()
    headers = {"User-Agent": "Mozilla/5.0"} # Mozilla Version 5.0
    for site, url in SITES.items():
        u = url.format(username)
        try:
            if site == "telegram":
                """ cookies for tele """
                for attempt in range(3):
                    try:
                        r = session.head(u, timeout=15, headers=headers, allow_redirects=True)
                        break
                    except requests.exceptions.RequestException:
                        time.sleep(random.uniform(2,5))
                else:
                    u_found.append((site, u, "ERROR timeout"))
                    continue
            else:
                r = session.get(u, timeout=15, headers=headers)
            if r.status_code == 200:
                u_found.append((site, u, "FOUND"))
            else:
                u_found.append((site, u, f"NOT FOUND ({r.status_code})"))
        except Exception as e:
            u_found.append((site, u, f"ERROR {e}"))
        time.sleep(1) # fix rate limit
    return u_found

def main():
    if len(sys.argv) < 2:
        # python3 tracking.py name
        print("Usage: python3 tracking.py <username>")
        sys.exit(1)
    base = sys.argv[1]
    u_variations = generate_variations(base)
    print(f"[INFO] Search base: {base}")
    print(f"[INFO] Generated {len(u_variations)} Variations\n")
    for v in u_variations:
        print(f"=== CHECKING: {v} ===")
        results = check_username(v)
        for site, link, status in results:
            print(f"[{site}] {link} -> {status}")
        print()

if __name__ == "__main__":
    main()