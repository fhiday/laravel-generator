import shutil
import os
import progressbar
import time

def copy_repo(dbname):
    # Source directory (cloned repository)
    src_dir = os.path.join('component', 'laravel-master')

    # Destination directory (new folder with database name)
    dst_dir = os.path.join('output', dbname)

    # Create the destination directory if it doesn't exist
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)

    print(f"Copying repository to {dst_dir}...")

    # Copy the repository to the new folder
    shutil.copytree(src_dir, dst_dir,dirs_exist_ok=True)

    # Create a progress bar
    bar = progressbar.ProgressBar(maxval=100, widgets=[
        progressbar.Bar(marker='=', left='[', right=']'),
        ' ', progressbar.Percentage()
    ])

    # Start the progress bar
    bar.start()

    # Update the progress bar
    for i in range(100):
        bar.update(i)
        time.sleep(0.1)  # adjust the sleep time to control the speed of the progress bar

    # Finish the progress bar
    bar.finish()

    print(f"Repository copied to {dst_dir}!")

