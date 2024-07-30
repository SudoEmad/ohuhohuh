# فتح ملف لكتابة جميع احتمالات عنوان IP
with open("ip_addresses.txt", "w") as file:
    # استخدام حلقات متداخلة لتوليد جميع الاحتمالات الممكنة
    for first in range(256):
        for second in range(256):
            for third in range(256):
                for fourth in range(256):
                    ip_address = f"{first}.{second}.{third}.{fourth}"
                    # كتابة عنوان IP إلى الملف
                    file.write(ip_address + "\n")

print("تمت كتابة جميع الاحتمالات إلى ملف ip_addresses.txt")
