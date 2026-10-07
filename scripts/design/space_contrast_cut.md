# Scene images: how each one was cut

Originals are the files as of commit dcaea901 (`git show dcaea901:assets/space/<name>.webp`).

`space_contrast_cut.py <originals> <out> name:thr:hole:glow:out` (see the script for the meaning):

    item-headset:24:0.03  item-gamepad:10:1:45  item-airdrop:14  item-trophy:30
    g-clash-of-clans-2:16  g-free-fire-1:14  g-free-fire-5:10:1  item-helmet:10:1  item-backpack:10:1  g-minecraft-4:7:1
    g-clash-of-clans-1:14::55  g-fortnite-2:22::60  g-minecraft-1:22::60  g-free-fire-2:20:1  ufo:20::70
    g-mobile-legends-1:22:::46  g-mobile-legends-5:22:::36  g-mobile-legends-4:30:::34  g-clash-royale-3:30:::46
    g-minecraft-2:34:::44  g-brawl-stars-2:30:::52  phone-6:10:1:32

`space_phone4_mask.py` — phone-4 (rotary phone). `space_satellite_patch.py` — satellite.
`space_item_masks.py` — every other item, phone, robot and astronaut.

After changing any scene image: raise `?v=` in assets/space-background.js (function img) and the script
version in the pages (`V` in space_rollout.py), otherwise the service worker keeps serving the old file.
    phone-5:12:1::36
    item-potion:30:::70
