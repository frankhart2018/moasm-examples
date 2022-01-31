import glob
import os
import subprocess
from tqdm import tqdm


if __name__ == "__main__":
    moasm_file_paths = glob.glob(os.path.join("examples", "*.moasm"))

    for moasm_file_path in tqdm(moasm_file_paths):
        moasm_file_name = ".".join(os.path.basename(moasm_file_path).split(".")[:-1])
        output_file_path = os.path.join("outputs", moasm_file_name)
        subprocess.run(["moasm", "-i", moasm_file_path, "-r", output_file_path])