from pymodbus.client.sync import ModbusTcpClient as ModbusClientTCP
from pymodbus.client.sync import ModbusSerialClient as ModbusClientRTU
import logging
logging.basicConfig()
log = logging.getLogger()
log.setLevel(logging.DEBUG)
adress = '192.168.1.10'
client = ModbusClientTCP(host=adress, port="502")
client.connect()

client.write_coil(64, 0, unit=1)

rr = client.read_holding_registers(48, 1, unit=1)
client.write_register(57, 0, unit=1)

print(rr.registers)








# rr = client.read_holding_registers(0, 1, unit=0x00)
# raw_value = client.read_holding_registers(0, 1, unit=0x00)
# rr_response = client.execute(rr)
# raw_value_response = client.execute(raw_value)
# print(raw_value_response)
# print (rr_response)
# rr = client.read_holding_registers(0, 1, unit=0x00)
# rq = client.write_coils(23, [True]*1, unit=1)
# assert(rq.function_code < 0x80)
# print (rr.registers)
# client.read_coils(1, 1)
# read = client.read_input_registers(1, 1)
# 0x0 0x1 0x0 0x0 0x0 0x6 0x0 0x5 0x0 0xb 0xff 0x0
# 0x0 0x1 0x0 0x0 0x0 0x6 0x0 0x5 0x0 0x17 0xff 0x0
# data = client.recv(9)
# rcv = client.recv(9)
# print(bytes.hex('1000'))
# print(bin(send))
# print(rcv)
# print(data)
# print(int('15', 4))
# 127.0.0.
# for port in range(65536):
#     client = ModbusClient(host='192.168.1.67', port=port, timeout=0.001)
#     client.host = '192.168.1.67'
#     ret = client.connect()
#     if ret:
#         print(port,ret)
# rr = client.write_coil(1,1)
# # int
# # assert(rr[0] == True)          # test the expected value
# print(rr)
client.close()