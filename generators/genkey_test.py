#!/usr/bin/env python3
import argparse
import os
import struct
import re


KNOWN_DEVICES = [
  'Unknown',
  'FoundryMaster',
  'TestMaster',
  'FoundryMasterCompact',
  'PmiMasterPro',
  'FoundryMasterPro',
  'OpticBoxAnalog',
  'OpticBoxDigital',
  'OpticBoxUsb18',
  'FoundryMasterXpert',
  'FoundryMasterXline',
  'PmiMasterSmart',
  'PmiMasterCompact',
  'FoundryMasterXlineAdvanced',
  'FoundryMasterXlineBasic',
  'FoundryMasterXlineCompact',
  'FoundryMasterSmart',
  'FoundryMasterOptimum',
  'FoundryMasterPro2',
  'FMExpert',
]


def load_license(path):
    with open(path, 'rb') as f:
        data = f.read()
    return bytes([x ^ 0xff for x in data[:-4]])


def store_license(path, data):
    checksum = sum(data)
    with open(path, 'wb') as f:
        f.write(bytes([x ^ 0xff for x in data]))
        f.write(struct.pack('<I', checksum))


def encode_device(device):
    return struct.pack('B', KNOWN_DEVICES.index(device))


def encode_unlock_code(code):
    code = code.split('-')
    assert len(code) == 4
    assert all(len(part) == 4 for part in code)
    code = ''.join(code)
    assert all(ord(c) in range(ord('K'), ord('K') + 16) for c in code)
    res = 0
    for i, c in enumerate(reversed(code)):
        res += (ord(c) - ord('K')) << (i * 4)
    return struct.pack('<Q', res)


def encode_unique_id(uid):
    assert len(uid) == 16
    return bytes.fromhex(uid)[::-1]


def encode_serial_number(serial):
    match = re.fullmatch(r'(\d{2})([A-Z])(\d{4})', serial)
    assert match is not None, f'{serial} serial format is not valid'
    part1 = struct.pack('B', int(match.group(1), 10))
    part2 = struct.pack('B', ord(match.group(2)) - ord('A') + 1)
    part3 = struct.pack('<H', int(match.group(3), 10))
    return part3 + part2 + part1


def encode_matrices(matrices):
    assert len(matrices) <= 20
    t = []
    for matrix in matrices:
        assert re.fullmatch(r'[A-Z]{2}\+?', matrix) is not None, f'{matrix} matrix format is not valid'
        enc = b'\x02'
        enc += matrix[:2].encode()
        enc += b'\x01' if len(matrix) > 2 else b'\x00'
        t.append(enc)
    while len(t) < 20:
        t.append(b'\0\0\0\0')
    return b''.join(t)


def patch_device(license, device):
    if device is None:
        return license
    return encode_device(device) + license[1:]


def patch_unlock_code(license, code):
    if code is None:
        return license
    return license[:0x8B8] + encode_unlock_code(code) * 2 + license[0x8C8:]


def patch_serial_number(license, serial):
    if serial is None:
        return license
    return license[:0x28] + encode_serial_number(serial) + license[0x2C:]


def patch_unique_id(license, uid):
    if uid is None:
        return license
    return license[:8] + encode_unique_id(uid) + license[16:]


def patch_version(license, version):
    if version is None:
        return license
    return license[:0x2C] + struct.pack('<I', version) + license[0x30:]


def patch_matrices(license, matrices):
    if matrices is None:
        return license
    return license[:0x94] + encode_matrices(matrices) + license[0xE4:]


def main():
    parser = argparse.ArgumentParser(description='Modyfy Waslab license')
    parser.add_argument('-i', metavar='input_path', dest='input', action='store', required=True, help='license to modify')
    parser.add_argument('-o', metavar='output_path', dest='output', action='store', required=True, help='where to store result')
    parser.add_argument('--device', action='store', choices=KNOWN_DEVICES, help='set target device type')
    parser.add_argument('--unlock-code', action='store', help='set unlock code, format XXXX-XXXX-XXXX-XXXX where X is character K-Z')
    parser.add_argument('--unique-id', action='store', help='set unique id, format is hex string of length 16')
    parser.add_argument('--serial-number', action='store', help='set serial number, format is ddCdddd, where d is digit and C is character A-Z')
    parser.add_argument('--version', action='store', type=int, help='set version, format is number without letters and dots, example: 390 for target version 3.90s')
    parser.add_argument('--matrices', metavar='ELEM', nargs='+', help='set matrices, max 20 elements, format is two letters for Spark, followed by optional + for Arc, example: FE NI+ means FE Spark NI Arc')
    args = parser.parse_args()


    assert os.path.exists(args.input), 'input path does not exist'

    data = load_license(args.input)
    data = patch_device(data, args.device)
    data = patch_unlock_code(data, args.unlock_code)
    data = patch_unique_id(data, args.unique_id)
    data = patch_serial_number(data, args.serial_number)
    data = patch_version(data, args.version)
    data = patch_matrices(data, args.matrices)
    store_license(args.output, data)


if __name__ == '__main__':
    main()
