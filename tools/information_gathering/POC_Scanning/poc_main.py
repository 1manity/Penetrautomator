import datetime
import json
import os
import subprocess
from urllib.parse import urlparse
from pathlib import Path
import shutil


class Poc_Scanning:
    def __init__(self, target_url,timestamp):
        # Initialize the Port_Scanning object with target_url and timestamp
        self.timestamp = timestamp
        self.target_url = target_url
        self.script_path = os.path.dirname(os.path.realpath(__file__))
        self.main_path=Path(self.script_path).parent.parent.parent
        self.parsed_url = urlparse(self.target_url)
        file_name = f"{self.parsed_url.netloc}_poc.html"
        self.tool_path = os.path.join(self.script_path, 'xray', 'xray.exe')
        self.output_dir = os.path.join(self.main_path, 'output_file', f'{timestamp}')
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)
        self.output_file=os.path.join(self.output_dir, file_name)
        self.logfile = f"{self.main_path}\\result\\{timestamp}\\log.json"
        os.makedirs(os.path.dirname(self.logfile), exist_ok=True)

    def progress_record(self, module=None, finished=False):
        # Record the progress of a module
        if os.path.exists(self.logfile) is False:
            shutil.copy(f"{self.main_path}\\config\\log_template.json", f"{self.main_path}\\result\\{self.timestamp}\\log.json")
        with open(self.logfile, "r", encoding="utf-8") as f1:
            log_json = json.loads(f1.read())
        if finished is False:
            if log_json[module] is False:
                return False
            elif log_json[module] is True:
                return True
        elif finished is True:
            log_json[module] = True
            with open(self.logfile, "w", encoding="utf-8") as f:
                f.write(json.dumps(log_json))
            return True

    def run_poc_scan(self):
        # Run the port scan and record its progress
        original_directory = os.getcwd()
        os.chdir(os.path.dirname(self.tool_path))
        cmd = f'{self.tool_path} ws --url {self.parsed_url.netloc} --html-output {self.output_file}'
        print("Poc Scanning is running, please wait...")
        process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True,bufsize=0)
        stdout, stderr = process.communicate()

        print(stdout.decode('utf-8'))
        if process.returncode != 0:
            print(f"Error occurred: {stderr.decode('utf-8', 'ignore')}")
        else:
            print("Poc Port Scanning has completed its work")
            self.progress_record(module='poc_scan', finished=True)
        os.chdir(original_directory)

def poc_scan(target_url,timestamp):
    # Create a Port_Scanning object and run port scan
    tool = Poc_Scanning(target_url,timestamp)
    tool.run_poc_scan()

if __name__ == '__main__':
    # Main function: get the target URL from user input and run get_port
    TARGET_URL = input("Please enter the target website url：")
    TIMESTAMP = datetime.datetime.now().strftime('%Y%m%d%H%M%S')  # Add global variable TIME
    poc_scan(TARGET_URL,TIMESTAMP)