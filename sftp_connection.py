import paramiko
import os
from dotenv import load_dotenv  # ondrova změna
load_dotenv('sftp.env')     # ondrova změna


class SFTPConnection:

    def __init__(self):
        try:
            self.conn = paramiko.SSHClient()
            self.conn.set_missing_host_key_policy(paramiko.AutoAddPolicy())
            self.conn.connect(
                hostname=os.getenv('hostname'),     # velké ondrovy změny
                port=int(os.getenv('port')),        # stačí bez integeru???
                username=os.getenv('user'),
                password=os.getenv('password'),
                look_for_keys=False
            )
            self.sftp = self.conn.open_sftp()
        except:
            print('Failed connecting to SFTP')

    def upload_recording(self, path):
        head, tail = os.path.split(path)
        remote_path = f'/home/projekt/{tail}'
        try:
            self.sftp.put(path, remote_path)
            return remote_path
        except:
            print('Upload failed')

    def file_exists(self, path):
        try:
            self.sftp.stat(path)
            return True
        except IOError:
            return False

    def close(self):
        self.conn.close()
        self.sftp.close()
