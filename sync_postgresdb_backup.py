# import subprocess

# # Step 1: Take a backup of the local database
# local_backup_path = r"C:\Users\euzoe\OneDrive\Desktop\DATA_ANALYSIS\MY_PROJECTS\SQL.sql"
# subprocess.run(["pg_dump", "-U", "postgres", "-d", "Instacart", "-f", local_backup_path])

# # Step 2: Copy the backup file to the Docker container
# container_id = "5601e071f31a"
# container_backup_path = "/tmp/SQL.sql"
# subprocess.run(["docker", "cp", local_backup_path, f"{container_id}:{container_backup_path}"])

# # Step 3: Restore the backup in the Docker container
# subprocess.run(["docker", "exec", "-it", container_id, "psql", "-U", "postgres", "-d", "Instacart", "-f", container_backup_path])


import subprocess
import os
from datetime import datetime

# Step 1: Check the last updated timestamp
last_backup_timestamp_path = r"C:\path\to\last_backup_timestamp.txt"
last_backup_timestamp = None

if os.path.exists(last_backup_timestamp_path):
    with open(last_backup_timestamp_path, "r") as f:
        last_backup_timestamp = f.read().strip()

# Step 2: Take an incremental backup of the local database
local_backup_path = r"C:\Users\euzoe\OneDrive\Desktop\DATA_ANALYSIS\MY_PROJECTS\SQL.sql"

if last_backup_timestamp:
    subprocess.run(
        [
            "pg_dump",
            "-U",
            "postgres",
            "-d",
            "Instacart",
            "-F",
            "p",
            "-b",
            "-v",
            "-f",
            local_backup_path,
            "--data-only",
            "--inserts",
            "--table",
            "table_name",
            "--where",
            f"modified_timestamp > '{last_backup_timestamp}'",
        ]
    )
else:
    subprocess.run(
        [
            "pg_dump",
            "-U",
            "postgres",
            "-d",
            "Instacart",
            "-F",
            "p",
            "-b",
            "-v",
            "-f",
            local_backup_path,
            "--data-only",
            "--inserts",
        ]
    )

# Step 3: Copy the backup file to the Docker container
container_id = "5601e071f31a"
container_backup_path = "/tmp/SQL.sql"
subprocess.run(
    ["docker", "cp", local_backup_path, f"{container_id}:{container_backup_path}"]
)

# Step 4: Restore the backup in the Docker container
subprocess.run(
    [
        "docker",
        "exec",
        "-it",
        container_id,
        "psql",
        "-U",
        "postgres",
        "-d",
        "Instacart",
        "-f",
        container_backup_path,
    ]
)

# Step 5: Update the last backup timestamp
current_timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
with open(last_backup_timestamp_path, "w") as f:
    f.write(current_timestamp)
