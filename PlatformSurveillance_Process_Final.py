import psutil
import sys
import os
import time
import schedule
import smtplib 
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders

# Defined CPU threshold for sending email
CPU_THRESHOLD = 80.0

def Send_Email(log_path, current_cpu):
    #Sends the generated log file via SMTP email.
    #To configure credentials and receiver details.

    sender_email = "sender_email@gmail.com"
    sender_password =  "asdfghjklqwertyu"   #This the App password for gmail
    receiver_email = "receiver_email@gmail.com"

    try:
        #MIMEMultipart() - allows an email to carry multiple different types of content at the same time—such as plain text, HTML, and file attachments
        msg = MIMEMultipart()
        msg["From"] = sender_email
        msg["To"] = receiver_email
        msg["Subject"] = f"[ALERT] High CPU Usage Detected ({current_cpu}%) - Surveillance Log"

        body = (f"Alert: System CPU usage has reached {current_cpu}% (Threshold: {CPU_THRESHOLD}%).\n"
            f"Please find the attached system surveillance log file for details.")

        #MIMEText - the text which goes inside the MIMEMultipart()
        msg.attach(MIMEText(body, "plain"))

        # To attach log file
        if os.path.exists(log_path):
            attachment = open(log_path,"rb")
            content = attachment.read()
            part = MIMEBase("application","octet-stream")
            part.set_payload(content)

            encoders.encode_base64(part)
            filename = os.path.basename(log_path)
            part.add_header("Content-Disposition",f"attachment; filename={filename}")
            msg.attach(part)
            attachment.close()

        #SMTP Server connection
        smtp = smtplib.SMTP_SSL("smtp.gmail.com", 465)
        smtp.login(sender_email, sender_password)
        smtp.sendmail(sender_email,receiver_email,msg.as_string())
        smtp.quit()

        print(f"[SUCCESS] High CPU log sent sucessfully to {receiver_email}")

    except Exception as email_err:
        print(f"[ERROR] Failed to send email alert: {email_err}")

                    
def ProcessScan():
    listprocess = []

    #Get details for every running process-(Iterate)--->
    for proc in psutil.process_iter():
        try:
            info = proc.as_dict(attrs=["pid","name","username","status"])
            info["cpu_percent"] = proc.cpu_percent(None)
            info["memory_percent"] = proc.memory_percent()
            listprocess.append(info)

        except(psutil.NoSuchProcess,psutil.AccessDenied,psutil.ZombieProcess):
            # Ignore processes that shut down or restricted processes during iteration
            pass

        except Exception as proc_err:
            print(f"[WARNING] Skipping a process due to error: {proc_err}")

    return listprocess

def PlatformSurvillance(FolderName):
    Border = "-"*50
    try:
        #Check system CPU usage
        current_cpu = psutil.cpu_percent(interval=1)
        print(f"Current System CPU Usage: {current_cpu}%")

        Ret = False
        Ret = os.path.exists(FolderName)

        if(Ret == True):
            Ret = os.path.isdir(FolderName)
            if(Ret == False):
                print("Unable to proceed as directory name is existing but it's not a directory")
                return
        else:
            os.mkdir(FolderName)
            print("Directory for log file gets created sucessfully.")

        #strftime used for string format time
        timestamp = time.strftime("%Y-%m-%d_%H_%M-%S")

        FileName = os.path.join(FolderName,"Marvellous_%s.log" %timestamp)

        fobj = open(FileName,"w")

        print(f"Log file successfully created with name {FileName}")

        fobj.write(Border+"\n")
        fobj.write("----Marvellous platform survillance system----\n")
        fobj.write("Log file created at: "+timestamp+"\n")
        fobj.write(Border+"\n\n")

        fobj.write("--------System Report--------\n")


        #CPU Information---->
        try:
            fobj.write("Number of active CPU cores: %s\n"%psutil.cpu_count())
           
            fobj.write("CPU Usage: %s %%\n"%current_cpu)


        except Exception as cpu_err:
            fobj.write(f"Error fetching CPU info: {cpu_err}\n")
        fobj.write(Border+"\n")


        #RAM Information---->
        try:
            memory = psutil.virtual_memory()
            fobj.write("RAM Usage: %s %%\n"%memory.percent)
            fobj.write("Total RAM Available: %s\n"%memory.total)

        except Exception as ram_err:
            fobj.write(f"Error fetching RAM info: {ram_err}\n")
        fobj.write(Border+"\n")


        #Network Usage---->
        try:
            netobj = psutil.net_io_counters()
            
            fobj.write("Network Usage Report\n")

            #Convert bytes to MB for upload
            fobj.write("Sent : %.2f MB\n"%(netobj.bytes_sent / (1024*1024))) 

            #Convert bytes to MB for download
            fobj.write("Received : %.2f MB\n"%(netobj.bytes_recv / (1024*1024))) 

        except Exception as net_err:
            fobj.write(f"Error fetching Network info: {net_err}\n")


        #Process log---->
        Data = ProcessScan()

        for info in Data:
            
            fobj.write("PID:       %s\n"%info.get("pid"))
            fobj.write("Name:      %s\n"%info.get("name"))
            fobj.write("User Name: %s\n"%info.get("username"))
            fobj.write("Status:    %s\n"%info.get("status"))
            fobj.write("CPU usage: %.2f\n"%info.get("cpu_percent"))
            fobj.write("RAM usage: %.2f\n"%info.get("memory_percent"))
            
            fobj.write(Border+"\n")

        fobj.write(Border+"\n")
        fobj.write("----------------------End of log file----------------------\n")
        fobj.write(Border+"\n")
        fobj.close()

        #Send_email if threshold met---->
        if current_cpu >= CPU_THRESHOLD:
            print(f"[ALERT] CPU usage ({current_cpu}%) reached threshold ({CPU_THRESHOLD}). Sending email....")
            Send_Email(FileName,current_cpu)
        else:
            print(f"[INFO] CPU usage ({current_cpu}%) is below threshold ({CPU_THRESHOLD}). Email not sent....")

        
    except(PermissionError,OSError,IOError) as io_err:
        print(f"[ERROR] File or Directory Operation Failed:{io_err}")
    except Exception as general_err:
        print(f"[ERROR] An unexpected error occured during survillance report generation: {general_err}")
        
           
def main():
    
    Border = "-"*50
    print(Border)
    print("------Marvellous platform survillance system------")
    print(Border)

    try:
        #--h and --u handling
        if(len(sys.argv) == 2):
            if(sys.argv[1] == "--h" or sys.argv[1] == "--H"):
                print("This automation script is used to perform.")
                print("1 : It fetches information of running processes.")
                print("2 : It fetches information about the primary storage as RAM.")
                print("3 : It fetches information about the secondary storage as HDD.")
                print("4 : It fetches information about the microprocessor.")
                print("5 : It auto-schedules execution periodically.")
                print("6 : It maintains all records into log file.")
                print("7 : It sends the log files through mail periodically.")

            elif(sys.argv[1] == "--u" or sys.argv[1] == "--U"):
                print("Use the automation script as: ")
                print(f"python {sys.argv[0]} Time_Interval Folder_Name")
                print("Time_Interval : Time in minutes for periodic execution.")
                print("Folder_Name : Name of folder for the log file creation")
            
            else:
                print("Unable to proceed as there are no matcing arguments.")
                print("Please use --h or --u flag for getting more details.")

        #Actual project code
        elif(len(sys.argv) == 3):
            try:
                interval = int(sys.argv[1])
            except ValueError:
                print(f"[ERROR] Time interval must be an integer (in minutes).")
            
            print("Scheduler started sucessfully.")
            print("Press Ctrl + C to abort the automation script.")

            schedule.every(int(sys.argv[1])).minutes.do(PlatformSurvillance,sys.argv[2])
            while True:
                schedule.run_pending()
                time.sleep(1)
        else:
            print("Invalid number of arguments.")
            print("Unable to proceed as arguments are not matching.")
            print("Please use --h or --u flag for getting more details.")

    except KeyboardInterrupt:
        print("\n[INFO] Scheduler stopped by user (Ctrl + C). Exiting safely....")
    except Exception as main_err:
        print(f"[ERROR] Unexpected script error: {main_err}")
            
    print(Border)
    print("----Thank you for using our automation system.----")
    print(Border)


if __name__ == "__main__":
    main()