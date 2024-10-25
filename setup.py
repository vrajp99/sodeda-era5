import os
repo_dir = os.path.dirname(os.path.realpath(__file__))
REPO_DIR = f"REPO_DIR=\"{repo_dir}\"\n"
path_str = os.path.join(repo_dir, "docker/")
with open(os.path.join(path_str,'run-gradio.template'), 'r') as t_file:
    content = t_file.read()

with open(os.path.join(path_str,'run-gradio.sh'), 'w') as sh_file:
    sh_file.write("#!/bin/bash\n")
    sh_file.write(REPO_DIR)
    sh_file.write(content)
print("Done!")