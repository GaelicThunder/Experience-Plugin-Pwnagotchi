# Experience-Plugin-Pwnagotchi

A totally not useful plugin for the Pwnagotchi, making it getting expierence everytime he Associate, Deauth or get an Handshake, try to level him up!

Wanted to make him more like a Tamagotchi, but moved that idea on another project.

Im a total newb when it comes to Python so, feel free to help if you see im doing som ebad stuff or you got some interesting ideas

Thanks to @mbudget0x01 and @hannadiamond for all the cool stuff!

## Setup
1. Copy over `exp.py` into your custom plugins directory
2. In your `config.toml` file, add:
   1. `main.plugins.exp.enabled = true`
   2. `main.plugins.exp.lvl_x_coord = -125`
   3. `main.plugins.exp.lvl_y_coord = 81`
   4. `main.plugins.exp.exp_x_coord = -85`
   3. `main.plugins.exp.exp_y_coord = 81`
3. Restart your device to see your new plugin!


## Things to do
  
- [x] Better Save System -> Saves are now in json Format and will per default migrate.
  
- [x] Make him count how many Handshake you have already captured and try to make a fair level up if you not starting from zero and you just installed the plugin [Example: if i already have 250 Handshake when i start the plugin for the first time, my Pwnagotchi will only be lv 1, while it should be lv 13(?)] -> if session-stats Plugin is installed, initially the data will be parsed from there. If not, just the last session will be counted.

- [] Make Things configurable through settings.

- [ ] Testing, lots of testing.
