# Grok Meets DOOM: Doom Unhinged

**DOOM just got a voice—and it’s savage.**  
This isn’t the silent demon-slaying you’re used to. With Grok, every NPC—demon, marine, or floating skull—spits wild, R18+ dialogue that’s as brutal as the chainsaw. Picture a cacodemon mid-battle screaming something so unhinged it throws you off, or a marine losing his mind in the heat of it. Grok turns DOOM into a trash-talking, pixelated nightmare—and it’s a blast.

**Who’s Grok?**  
Grok’s the AI mastermind behind the madness. Built by xAI, it’s got no filter and all the attitude, pumping out lines that are raw, chaotic, and pure DOOM. It’s the voice of hell you didn’t know you needed.

![Imps talking smack as they throw fireballs](https://i.imgur.com/mmSchtJ.png)

----------

**What You’re Getting**

-   Grok’s Dialogue: Real-time, unhinged NPC chatter powered by Grok via a Python server.
    
-   DOOM: The classic Linux Doom 1.10, now louder than ever.
    
-   Bare Necessities: A quick Xephyr setup for 8-bit vibes (we’ll keep it short).
    

----------

**Setup: Quick and Dirty**

1. DOOM + Xephyr

You need DOOM running in its retro 8-bit glory. Xephyr makes that happen—install it and move on:

-   Debian/Ubuntu: sudo apt install xserver-xephyr
    
-   Arch Linux: sudo pacman -S xserver-xephyr  
    Launch Xephyr:
    
```bash
sudo Xephyr :2 -ac -screen 640x480x8
```

Head to the DOOM folder:

```bash
cd linuxdoom-1.10
```

Point it to Xephyr and fire it up:

```bash
export DISPLAY=:2
./linux/linuxxdoom -2
```

2. Grok’s Python Power

Set up the dialogue server:

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Drop a .env file in the root:

```text
LLM=XAI
MODEL=grok-2-latest
XAI_API_KEY=your_xai_api_key
```

3. Unleash the Chaos

Run the Python script to connect Grok to DOOM:

```bash
python3 dialogue_server.py
```

It uses FIFOs—/tmp/doom_dialogue_req for requests, /tmp/doom_dialogue_res for Grok’s responses—and pumps out 40-character lines of pure mayhem.

----------

**Why It Rules**

-   Grok Steals the Show: NPCs go from mute to manic with dialogue that’s wild and unpredictable.
    
-   DOOM Feels Alive: Every demon’s got something to say, and it’s usually unprintable.
    
-   Fast and Furious: Setup’s a breeze so you can jump straight into the chaos.
    

----------

**Ready?**  
Fire it up, tweak it for your mods, and let Grok turn DOOM into a screaming, swearing, demon-filled riot. Rip and tear—with attitude!


**Credits:**

Source code yoinked from https://github.com/0Lunar/DOOM
Original source code from https://github.com/id-Software/DOOM

Copyright (c) ZeniMax Media Inc.
Licensed under the GNU General Public License 2.0.