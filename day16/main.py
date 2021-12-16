import os
from pathlib import Path
import itertools
import functools
from typing import List

input_p = Path(os.getcwd()) / 'input'
text = input_p.read_text()
lines = text.splitlines()

def binary_to_decimal(binary: str) -> int:
    decimal = 0
    for (i, d) in enumerate(reversed([int(i) for i in binary])):
        decimal += (2**i)*d
    return decimal

hex_to_binary = {
    "0": "0000",
    "1": "0001",
    "2": "0010",
    "3": "0011",
    "4": "0100",
    "5": "0101",
    "6": "0110",
    "7": "0111",
    "8": "1000",
    "9": "1001",
    "A": "1010",
    "B": "1011",
    "C": "1100",
    "D": "1101",
    "E": "1110",
    "F": "1111"
}

encoded = lines[0]
binary = "".join([hex_to_binary[h] for h in encoded])

#packet_info = (version, type, [list_of_packets], value, length)
def process_packet(binary):
    packet_version = binary[:3]
    packet_type = binary[3:6]
    if packet_type == "100":
        packet_info = process_literal(binary)
    else:
        length_type = binary[6]
        if length_type == "0":
            packet_info = process_type_0(binary)
        else:
            packet_info = process_type_1(binary)

    return packet_info


def process_literal(binary):
    packet_version = binary[:3]
    packet_type = binary[3:6]

    numbers = []
    pos = 6
    while True:
        start_bit = binary[pos]
        number = binary[pos + 1: pos + 5]
        numbers.append(number)
        pos = pos + 5
        
        if start_bit == '0':
            break
    
    value = binary_to_decimal("".join(numbers))
    return (binary_to_decimal(packet_version), binary_to_decimal(packet_type), [], value, 6 + len(numbers) * 5)


def process_type_0(binary):
    packet_version = binary[:3]
    packet_type = binary[3:6]
    length_binary = binary[7:22]
    length = binary_to_decimal(length_binary)

    subpackets = []
    pos = 22
    while True:
        subpacket_info = process_packet(binary[pos:])
        subpackets.append(subpacket_info)
        pos += subpacket_info[-1]

        if pos >= length + 22:
            break
    
    packet = (binary_to_decimal(packet_version), binary_to_decimal(packet_type), subpackets, None, pos)
    value = calculate_value(packet)
    packet_with_value = (packet[0], packet[1], packet[2], value, packet[4])
    return packet_with_value


def process_type_1(binary):
    packet_version = binary[:3]
    packet_type = binary[3:6]
    n_subpackets_binary = binary[7:18]
    n_subpackets = binary_to_decimal(n_subpackets_binary)

    subpackets = []
    pos = 18
    while True:
        subpacket_info = process_packet(binary[pos:])
        subpackets.append(subpacket_info)
        pos += subpacket_info[-1]

        if len(subpackets) == n_subpackets:
            break
    
    packet = (binary_to_decimal(packet_version), binary_to_decimal(packet_type), subpackets, None, pos)
    value = calculate_value(packet)
    packet_with_value = (packet[0], packet[1], packet[2], value, packet[4])
    return packet_with_value


def sum_versions(packet):
    total = packet[0]

    for sub in packet[2]:
        total += sum_versions(sub)

    return total

def calculate_value(packet):
    t = packet[1]
    subpacket_values = [sub[-2] for sub in packet[2]]

    if t == 0:
        res = sum(subpacket_values)
    elif t == 1:
        res = 1
        for v in subpacket_values:
            res *= v
    elif t == 2:
        res = min(subpacket_values)
    elif t == 3:
        res = max(subpacket_values)
    elif t == 5:
        res = 1 if subpacket_values[0] > subpacket_values[1] else 0
    elif t == 6:
        res = 1 if subpacket_values[0] < subpacket_values[1] else 0
    elif t == 7:
        res = 1 if subpacket_values[0] == subpacket_values[1] else 0
    
    return res

res = process_packet(binary)
total = sum_versions(res)
print(total)
print(res[-2])
