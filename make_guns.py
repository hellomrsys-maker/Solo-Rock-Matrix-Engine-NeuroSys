from PIL import Image, ImageDraw

def make_gun(filename, firing=False):
    # Create 512x512 magenta background
    img = Image.new('RGB', (512, 512), color='#FF00FF')
    draw = ImageDraw.Draw(img)
    
    # Draw simple double barrel shotgun (two gray rectangles)
    # Barrel left
    draw.rectangle([200, 200, 240, 512], fill='#555555', outline='#333333', width=5)
    # Barrel right
    draw.rectangle([272, 200, 312, 512], fill='#555555', outline='#333333', width=5)
    
    # Handle / Base
    draw.rectangle([180, 400, 332, 512], fill='#333333')
    
    if firing:
        # Draw massive muzzle flash
        draw.ellipse([150, 50, 362, 250], fill='#FF8800')
        draw.ellipse([200, 100, 312, 200], fill='#FFFF00')
        draw.ellipse([240, 130, 272, 170], fill='#FFFFFF')
        
    img.save(filename)

make_gun('C:\\Users\\sysyo\\.gemini\\antigravity-ide\\scratch\\solo_rock_v4\\gun_idle.bmp', firing=False)
make_gun('C:\\Users\\sysyo\\.gemini\\antigravity-ide\\scratch\\solo_rock_v4\\gun_fire.bmp', firing=True)
print("Generated gun BMPs!")
