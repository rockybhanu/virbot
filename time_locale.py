import paramiko
import os
from dotenv import load_dotenv
import logging

# Load sensitive information from .env file
load_dotenv()
SSH_HOST = os.getenv("SSH_HOST")
SSH_USERNAME = os.getenv("SSH_USERNAME")
SSH_PASSWORD = os.getenv("SSH_PASSWORD")

# Set up logging to a file
logging.basicConfig(
    filename="automation_log.txt",
    level=logging.DEBUG,
    format="%(asctime)s - %(levelname)s - %(message)s",
)


# Commands for time, locale, and timezone settings
commands = [
    "sudo timedatectl set-ntp true",
    "sudo timedatectl set-timezone Asia/Kolkata",
    "sudo localectl set-keymap us",
]


def connect_ssh():
    # Establish SSH connection
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(SSH_HOST, username=SSH_USERNAME, password=SSH_PASSWORD)
        logging.info("Connected to host")
        print("Connected to host")
        return client
    except paramiko.SSHException as e:
        logging.error(f"Connection failed: {e}")
        print(f"Connection failed: {e}")
        return None


def execute_commands(client):
    for command in commands:
        logging.info(f"Executing: {command}")
        print(f"Executing: {command}")
        stdin, stdout, stderr = client.exec_command(command)
        # Send password for sudo commands if prompted
        stdin.write(SSH_PASSWORD + "\n")
        stdin.flush()
        if stdout.channel.recv_exit_status() == 0:
            output = stdout.read().decode().strip()
            logging.info(f"Success: {command}\nOutput: {output}")
            print(f"Success: {command}\nOutput: {output}")
        else:
            error = stderr.read().decode().strip()
            logging.error(f"Error executing: {command}\nError: {error}")
            print(f"Error executing: {command}\nError: {error}")


def verify_settings(client):
    # Verify system settings for time, locale, and timezone
    verify_commands = ["timedatectl", "localectl"]
    for verify_command in verify_commands:
        logging.info(f"\nVerifying: {verify_command}")
        print(f"\nVerifying: {verify_command}")
        stdin, stdout, stderr = client.exec_command(verify_command)
        output = stdout.read().decode().strip()
        logging.info(f"Output of {verify_command}:\n{output}")
        print(output)


def main():
    client = connect_ssh()
    if client:
        execute_commands(client)
        verify_settings(client)
        client.close()
        logging.info("Disconnected from host")
        print("Disconnected from host")


if __name__ == "__main__":
    main()
