import time, os, paramiko, socket
from datetime import datetime
from datetime import timedelta
import telepot
import logging

#---------------: Starting Logging into a file :---------------
def setLogger():
    logger = logging.getLogger()
    logger.setLevel(logging.WARNING)

    formatter = logging.Formatter('%(asctime)s|%(levelname)s|%(lineno)d|%(message)s' )

    fh = logging.FileHandler('log_filename.txt')
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(formatter)
    logger.addHandler(fh)

#---------------: Check ping of a machine :---------------
def pingchecker(host):
    response = os.popen(f"ping -n 1 "+host).read()
    if "TTL=" in response:
        return True
    else:
        return False

#---------------: Check status of applications running on Windows' machine :---------------
def check_winApps():
    result = str()
    try:
        server = '192.168.1.4'
        if pingchecker(server):
            output = os.popen('wmic /node:192.168.1.4 /user:username /password:passwd  process where "name like \'Cap%.exe\'" get ExecutablePath').readlines()

            app1_flag, app2_flag = False, False

            for line in output:
                content = line.strip()
                if not content == "":
                    if 'Capture_App1' in content:
                        app1_flag = True
                    if 'Capture_App2' in content:
                        app2_flag = True

            if not app1_flag:
                result = result + '\nProblem in Application 1'
            if not app2_flag:
                result = result + '\nProblem in Application 2'
        else:
            result = result + 'No ping to : ' + str(server)
    except Exception as e:
        result = result + str(e)
    if result == "":
        result = result + str("OK!")
    return result

#---------------: Check status of applications running on Linux' machine :---------------
def check_linuxApp():
    output_string = str()

    try:
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        serverList = [ '192.168.1.2', '192.168.1.3']
        no_ping = 0
        for server in serverList:
            if not pingchecker(server):
                output_string = output_string + '\n' + 'No ping to : ' + str(server)
                no_ping = no_ping + 1
            else:
                output_string = output_string + '\n' + 'Proceeding with ' + str(server)
                break
        if not no_ping == len(serverList):
            output_string = output_string + '\n'
            ssh.connect(server, username='root', password='123456')
            output = list()
            pathtoFile = "/path/to/script"
            stdin , stdout, stderr = ssh.exec_command('cd "' + pathtoFile +'" ; ./scriptname',timeout=600)
            while True:
                for line in stdout.readlines():
                    print(line)
                    output.append(line.strip())
                if stdout.channel.exit_status_ready():
                    break
            ssh.close()
            
            if output == []:
                output_string = output_string + str('ok!') + '\n'
            else:
                for line in output:
                    output_string = output_string + str(line) + '\n'
    except Exception as e:
        output_string = output_string + '\n' + str(e)
    return output_string

def print_output(text):
    my_bot.sendMessage(chat_id, text, parse_mode=None, disable_web_page_preview=None, disable_notification=None, reply_to_message_id=None, reply_markup=None)

#---------------: Main Starts Here :---------------
if __name__ == "__main__":
    #---------------: Calling Logger :---------------
    setLogger()
    #---------------: token to access the HTTP API :---------------
    token=''
    
    my_bot = telepot.Bot(token)
    
    #---------------: chat_id of group :---------------
    chat_id = 
    try:
        last_winapp_update , last_linuxapp_update = str(), str()
        
        crr_time = datetime.now()
        #---------------: ttl represents the Time To Close the script :---------------
        ttl = crr_time.replace(hour=15, minute=35, second=0, microsecond=0)

        while(1):            
            crr_time = datetime.now()

            #---------------: Comparing Crr_Time to Time To Leave/Exit/Close the program :---------------
            if ttl < crr_time:
                output = '\nIts Time to Leave! Stopping Process'
                print_output(output)
                break
            
            #---------------: Check status of applications running on windows machine :---------------
            print('Checking Windows Machine\'s applications', datetime.now().strftime('%H:%M'))
            output = check_winApps()
            if not output == last_winapp_update:
                print_output('Status till ' + crr_time.strftime('%H:%M') + '\n' + output)
            last_winapp_update = output

            #---------------: Check status of applications running on Linux' machine :---------------
            print('Checking Linux Machine\'s applications', datetime.now().strftime('%H:%M'))
            output = check_linuxApp()
            if not output == last_linuxapp_update:
                print_output('Status till ' + crr_time.strftime('%H:%M') + '\n' + output)
            last_linuxapp_update = output
            
            time.sleep(60)
            
    except Exception as e:
        #---------------: If any exception occured while running this program that exception will also sent in group :---------------
        print_output('Update till ' + crr_time.strftime('%H:%M') + '\n' + 'Application Crashed')
        logging.error(str(e))
    
print('Process Stopped')
