import pexpect
import time
import re

devices_connect = '00:00:00:00:00:00'  # MAC address of the desired device on the air

scan_results = open("scan_results.txt", 'w')  # text list of all found devices on the air
blectl = pexpect.spawn("bluetoothctl")
blectl.send("scan on\n")
bledevices_list = []

blescan = False
a = 0
while not blescan:
    newbdaddr = blectl.expect("Device (([0-9A-Fa-f]{2}:){5}([0-9A-Fa-f]{2}))")
    newbdaddrgroup = blectl.match.group(1)
    bdaddrgr_re = re.findall(r'\w{1,2}', str(newbdaddrgroup))
    device_add = str(bdaddrgr_re[1]) + ':' + str(bdaddrgr_re[2]) + ':' + str(bdaddrgr_re[3]) + ':' \
                 + str(bdaddrgr_re[4]) + ':' + str(bdaddrgr_re[5]) + ':' + str(bdaddrgr_re[6])

    if device_add not in bledevices_list:
        bledevices_list.append(device_add)
        print(device_add)
        blescan = False
    else:
        time.sleep(1)
        a = a + 1
        if a == 20:
            scan_results.write(str(bledevices_list))
            blectl.close()
            scan_results.close()
            blescan = True

if devices_connect in bledevices_list:
    print('Device in network...', str(devices_connect))
else:
    print('Device NOT in network', str(bledevices_list))
