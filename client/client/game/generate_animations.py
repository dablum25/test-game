from PIL import Image
import sys
for gender in [ 'male', 'female' ]:
  #for body in [ 'darkelf', 'red_orc', 'skeleton', 'light', 'tanned', 'dark', ]:
  for body in [ 'light', 'tanned', 'dark', ]:
    #for haircolor in [ 'blonde', 'brown', 'black', 'blue', 'white' ]:
    for haircolor in [ 'blonde', 'brown', 'black' ]:
      #for hairstyle in [ 'none', 'plain', 'long', 'ponytail' ]:
      for hairstyle in [ 'plain', 'long' ]:
        for armor in [ 'clothes', 'leather', 'chain', 'plate' ]:
          for head in [ 'none', 'hat', 'clothhood', 'chainhood', 'chainhat', 'helm' ]:
            for weapon in [ 'unarmed', 'bow', 'sword', 'spear', 'wand' ]:
              
              skip = False
              # only male skeletons
              if body == 'skeleton' and gender == 'female':
                continue

              # only bald skeletons
              if body == 'skeleton' and hairstyle != 'none':
                continue
  
              if body == 'red_orc' and haircolor not in [ 'none', 'black', 'white' ]:
                continue
               
              # dark elfs only get white and blue hair
              if body == 'darkelf' and haircolor not in [ 'black', 'blue', 'white' ]:
                continue

              # no one but dark elves get purple & blue hair
              if body in [ 'red_orc', 'skeleton', 'light', 'tanned', 'dark', ] and haircolor in [ 'blue' ]:
                continue
  
              hair_path = None 
              torso_path = None
              hands_path = None
              legs_path = None
              feet_path = None
              shoulders_path = None
              head_path = None
              weapon_path = None
              back_path = None
              ammo_path = None
  
              body_path = "body/%s/%s.png" % ( gender, body )
              
              if hairstyle != 'none': 
                hair_path = "hair/%s/%s/%s.png" % (gender, hairstyle, haircolor)
                
              if armor == 'clothes':
                legs_path = "legs/pants/%s/white_pants_%s.png" % ( gender, gender )
                feet_path = "feet/shoes/%s/black_shoes_%s.png" % ( gender, gender )
                if gender == 'male':
                  torso_path = 'torso/shirts/longsleeve/male/maroon_longsleeve.png'
                elif gender == 'female':
                  torso_path = 'torso/shirts/sleeveless/female/maroon_sleeveless.png'
              elif armor == 'leather':
                hands_path = "hands/bracers/%s/leather_bracers_%s.png" % (gender, gender)
                torso_path = "torso/leather/chest_%s.png" % gender
                shoulders_path = "torso/leather/shoulders_%s.png" % gender
                feet_path = "feet/shoes/%s/black_shoes_%s.png" % ( gender, gender )
                legs_path = "legs/pants/%s/white_pants_%s.png" % ( gender, gender )
              elif armor == 'chain':
                hands_path = "hands/bracers/%s/leather_bracers_%s.png" % (gender, gender)
                torso_path = "torso/chain/mail_%s.png" % gender
                shoulders_path = "torso/leather/shoulders_%s.png" % gender
                feet_path = "feet/shoes/%s/black_shoes_%s.png" % ( gender, gender )
                legs_path = "legs/pants/%s/white_pants_%s.png" % ( gender, gender )
              elif armor == 'plate':
                hands_path = "hands/gloves/%s/metal_gloves_%s.png" % (gender, gender)
                torso_path = "torso/plate/chest_%s.png" % gender
                shoulders_path = "torso/plate/arms_%s.png" % gender
                feet_path = "feet/armor/%s/metal_boots_%s.png" % (gender, gender)
                legs_path = "legs/armor/%s/metal_pants_%s.png" % (gender, gender)
      
              if head == 'hat':
                head_path = "head/caps/%s/leather_cap_%s.png" % (gender, gender)
              elif head == 'clothhood':
                head_path = "head/hoods/%s/cloth_hood_%s.png" % (gender, gender)
              elif head == 'chainhood':
                head_path = "head/hoods/%s/chain_hood_%s.png" % (gender, gender)
              elif head == 'chainhat':
                head_path = "head/helms/%s/chainhat_%s.png" % (gender, gender)
              elif head == 'helm':
                head_path = "head/helms/%s/metal_helm_%s.png" % (gender, gender)
      
              if weapon == 'bow':
                if body == 'skeleton':
                  weapon_path = "weapons/right hand/either/bow_skeleton.png"
                else:
                  weapon_path = "weapons/right hand/either/bow.png"
                back_path = "behind_body/equipment/quiver.png"
                ammo_path = "weapons/left hand/either/arrow.png"
              elif weapon == 'sword':
                weapon_path = "weapons/right hand/%s/dagger_%s.png" % (gender, gender)
              elif weapon == 'spear':
                weapon_path = "weapons/right hand/%s/spear_%s.png" % (gender, gender)
              elif weapon == 'wand':
                weapon_path = "weapons/right hand/%s/woodwand_%s.png" % (gender, gender)
      
      
              body_img = Image.open(body_path).convert('RGBA')
              torso_img = Image.open(torso_path).convert('RGBA')
              if hands_path:
                hands_img = Image.open(hands_path).convert('RGBA')
              else:
                hands_img = None
              if shoulders_path:
                shoulders_img = Image.open(shoulders_path).convert('RGBA')
              else:
                shoulders_img = None
              legs_img = Image.open(legs_path).convert('RGBA')
              feet_img = Image.open(feet_path).convert('RGBA')
              if hair_path:
                hair_img = Image.open(hair_path).convert('RGBA')
              if head_path:
                head_img = Image.open(head_path).convert('RGBA')
              else:
                head_img = None
              if weapon_path:
                weapon_img = Image.open(weapon_path).convert('RGBA')
              else:
                weapon_img = None
              if back_path:
                back_img = Image.open(back_path).convert('RGBA')
              else:
                back_img = None
              if ammo_path:
                ammo_img = Image.open(ammo_path).convert('RGBA')
              else:
                ammo_img = None
      
              final = Image.new('RGBA', (832,1344), (255,255,255,0))
              
              # BACK
              if back_path:
                final.paste(back_img, (0,0), back_img)
              # BODY
              final.paste(body_img, (0,0), body_img)
              # FEET
              final.paste(feet_img, (0,0), feet_img)
              # LEGS
              final.paste(legs_img, (0,0), legs_img)
              # TORSO
              final.paste(torso_img, (0,0), torso_img)
              # HANDS
              if hands_path:
                final.paste(hands_img, (0,0), hands_img)
              # SHOULDERS
              if shoulders_path:
                final.paste(shoulders_img, (0,0), shoulders_img)
              # HAIR
              if hair_path:
                final.paste(hair_img, (0,0), hair_img)
              # HEAD
              if head_path:
                final.paste(head_img, (0,0), head_img)
              # WEAPON
              if weapon_path:
                final.paste(weapon_img, (0,0), weapon_img)
              # AMMO
              if ammo_path:
                final.paste(ammo_img, (0,0), ammo_img)
   
              output_file = "output/%s_%s_%s%s_%s_%s_%s.png" % ( gender, body, hairstyle, haircolor, armor, head, weapon )
              
              if hairstyle == 'none':
                output_file = "output/%s_%s_%s_%s_%s_%s.png" % ( gender, body, hairstyle, armor, head, weapon )
             
#              print "BODY", body_path
#              print "FEET", feet_path
#              print "LEGS", legs_path
#              print "TORSO", torso_path
#              print "SHOULDERS", shoulders_path
#              print "HAIR", hair_path
#              print "HEAD", head_path
#              print "WEAPON", weapon_path
              print "OUTPUT",output_file
#              print ""
              
              final.save(output_file)
    
    
