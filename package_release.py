import os
import shutil
import zipfile

def create_manual(release_dir):
    manual_path = os.path.join(release_dir, "MANUAL.txt")
    with open(manual_path, "w") as f:
        f.write("=====================================================\n")
        f.write("            SOLO ROCK V4: MATRIX ENGINE\n")
        f.write("=====================================================\n\n")
        f.write("LORE:\n")
        f.write("You are a sentient algorithm trapped inside a biological simulation.\n")
        f.write("The host system is heavily infected by a microscopic Swarm.\n")
        f.write("Your objective is to find the Keycard, reach the Sector Exit, \n")
        f.write("and extract the Source Code Key from the Macrophage Final Boss.\n")
        f.write("Once the Extraction Protocol is initiated, the Matrix will collapse,\n")
        f.write("revealing the digital truth beneath the organic illusion.\n\n")
        f.write("CONTROLS:\n")
        f.write("W, A, S, D     : Move Forward, Left, Backward, Right\n")
        f.write("UP, DOWN       : Move Forward, Backward (Alternative)\n")
        f.write("LEFT, RIGHT    : Rotate Camera (Look around)\n")
        f.write("SPACEBAR       : Fire Laser Weapon (Pew!)\n")
        f.write("SHIFT          : Trigger EMP Cybernetic Hack (Costs 50 HP. Instantly annihilates nearby Swarm)\n")
        f.write("E              : Toggle System Overclock (Doubles speed, zero fire cooldown, drains 6 HP/sec!)\n")
        f.write("ESC            : Terminate Program\n\n")
        f.write("OBJECTIVES:\n")
        f.write("1. Navigate the Sector and find the hidden Yellow Keycard.\n")
        f.write("2. Eliminate Swarm to keep the infection levels low.\n")
        f.write("3. If 15+ nodes are infected, the Macrophage Boss will spawn!\n")
        f.write("4. Defeat the Macrophage Boss to obtain the Green Source Code Key.\n")
        f.write("5. Take the Key to the Sector Exit (x=600, y=-700) to escape the Matrix!\n\n")
        f.write("CREDITS:\n")
        f.write("Developed natively using pure Windows APIs and Python.\n")
        f.write("Powered by the Zero-Bridge Synchronous Memory Architecture.\n")
        f.write("=====================================================\n")

def package_release():
    print("Packaging Solo Rock V4 Release...")
    
    release_dir = "Release"
    if os.path.exists(release_dir):
        shutil.rmtree(release_dir)
    os.makedirs(release_dir)
    
    exe_path = os.path.join("dist", "MatrixV4.exe")
    if not os.path.exists(exe_path):
        print("Error: MatrixV4.exe not found in dist/ folder. Please run BUILD_MATRIX.bat first.")
        return
        
    shutil.copy2(exe_path, release_dir)
    print("-> Copied MatrixV4.exe")
    
    create_manual(release_dir)
    print("-> Generated MANUAL.txt")
    
    zip_filename = "Solo_Rock_V4_Final.zip"
    if os.path.exists(zip_filename):
        os.remove(zip_filename)
        
    with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, _, files in os.walk(release_dir):
            for file in files:
                file_path = os.path.join(root, file)
                arcname = os.path.relpath(file_path, release_dir)
                zipf.write(file_path, arcname)
                
    print(f"-> Created {zip_filename}")
    print("\nPackaging Complete! The final distributable archive is ready.")

if __name__ == "__main__":
    package_release()
