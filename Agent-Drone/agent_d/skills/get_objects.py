## IMPLEMENTATION DOESN"T WORK - NEED TO FIND A WAY TO GET THE POSE INFO OF OBJECTS IN GAZEBO SIMULATOR
## TRIED COMMAND LINE (gz model --list, gz topic --l), GZ TRANSPORT, PYGAZEBO, etc.
## CURRENTLY, TRISE TO RUN BASH SCRIPT GET_POSES.SH, but doesn't work!

import subprocess

def run_bash_script(script_path):
    
    print("Starting script")
    result = subprocess.run([script_path], stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    return result.stdout, result.stderr

script_path = './get_poses.sh'
stdout, stderr = run_bash_script(script_path)

if stderr:
    print(f"Error: {stderr}")
else:
    print(f"Output:\n{stdout}")
