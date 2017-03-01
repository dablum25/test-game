BUILD:

Use pyinstaller for distribution:

```
pip install twisted
pip install pytmx
pip install pyinstaller
pyinstaller --add-data data:data -n my_game_name game_server.py
```

TODO:
* More work on quests
* Gold currency
* Player leveling and it's effects on combat
* Skill trees
* Spells to summon monsters/companions that protect caster
* Player trades
* Player Groups
* Awarding exp
* Dividing treasure
* Crafting
* Define monster, NPC, player spawn points on zone map. Define warps on zone map. 
* Warp to bordering zone when edge reached
* content
* more content
* even more content
