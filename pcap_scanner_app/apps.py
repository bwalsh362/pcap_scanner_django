from django.apps import AppConfig
# import subprocess, sys
#
#
class PcapScannerAppConfig(AppConfig):
    name = 'pcap_scanner_app'
#     verbose_name = "Network Topology Mapper"
#
#     def ready(self):
#         print('starting subprocess')
#         p = subprocess.Popen([sys.executable, 'scanner.py'],
#                              stdout=subprocess.PIPE,
#                              stderr=subprocess.STDOUT)
#         while True:
#             output = p.stdout.readline()
#             if output == '' and p.poll() is not None:
#                 break
#             if output:
#                 print(output.strip())
#         rc = p.poll()
#         return rc
