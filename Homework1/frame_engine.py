import re
import json

def bit_frame(frame):
    for idx in range(len(frame)):
        frame[idx] = decimal_to_binary(frame[idx])
    return "".join(frame)


def decimal_to_binary(n):
    bits = bin(n).replace("0b", "")
    while len(bits) != 8 and len(bits) < 8:
        bits = '0' + bits
    return bits

def decode_frame_packet(frame):
    frame_dic = {
        "FIN": frame[0],
        "RSV1": frame[1],
        "RSV2": frame[2],
        "RSV3": frame[3],
        "OPCODE": frame[4:8],
        "MASK": frame[8],
        "PAYLEN": int(frame[9:16],2),
    }
    (frame, payload_length) = compute_payload(frame[16:], frame_dic["PAYLEN"])
    frame_dic["PAYLEN"] = payload_length
    (frame, mask_value) = compute_maskvalue(frame, frame_dic['MASK'])
    frame_dic["MASKVALUE"] = mask_value
    frame_dic["DATA"] = frame
    return frame_dic
    

def compute_payload(frame, payload_length):
    if payload_length < 126:
        return frame, payload_length
    elif payload_length == 126:
        return frame[16:], int(frame[0:16],2)
    else:
        return frame[64:], int(frame[0:64],2)

def compute_maskvalue(frame, mask_value):
    if int(mask_value) == 0:
        return frame, 0
    else:
        return frame[32:], frame[0:32]

def unmask_data(data, mask_value):
    list_unmasked = []
    start_idx = 0
    end_idx = 32
    while end_idx < len(data):
        unmasked_bits = decimal_to_binary(int(data[start_idx:end_idx],2)^int(mask_value,2))
        while len(unmasked_bits) != 32:
            unmasked_bits = '0' + unmasked_bits
        list_unmasked.append(unmasked_bits)
        start_idx += 32
        end_idx += 32
    unmasked_bits = decimal_to_binary(int(data[start_idx:],2)^int(mask_value[:len(data[start_idx:])],2))
    while len(unmasked_bits) != len(data[start_idx:]):
        unmasked_bits = '0' + unmasked_bits
    list_unmasked.append(unmasked_bits)
    return "".join(list_unmasked)

def decode_data(data):
    decoded_data = ""
    start_idx = 0
    end_idx = 8
    while end_idx != len(data)+8:
        single_data = data[start_idx:end_idx]
        single_data = int(single_data, 2)
        single_data = chr(single_data)
        decoded_data += single_data
        start_idx += 8
        end_idx += 8
    return json.loads(decoded_data)

def compute_payload_packet(payload_length, frame):
    if payload_length < 126:
        frame += decimal_to_binary(payload_length)[1:]
    elif payload_length >= 126 and payload_length < 65536:
        frame += decimal_to_binary(126)[1:]
        payload_binary = decimal_to_binary(payload_length)
        while len(payload_binary) < 16:
            payload_binary = '0' + payload_binary
        frame += payload_binary
    else:
        frame += decimal_to_binary(127)[1:]
        payload_binary = decimal_to_binary(payload_length)
        while len(payload_binary) < 64:
            payload_binary = '0' + payload_binary
        frame += payload_binary
    return frame

def create_chat_json(dic, handler):
    comment = dic["comment"].encode()
    comment = comment.replace(b'&', b'&amp;')
    comment = comment.replace(b'>', b'&gt;')
    comment = comment.replace(b'<', b'&lt;')
    dic["comment"] = comment.decode()
    json_value = json.dumps({'messageType': dic['messageType'], 'username': handler.websocket_connection[handler],'comment': dic['comment']})
    return json_value

def create_webRTC_json(dic):
    json_value = json.dumps({"messageType": dic["messageType"], "offer": dic["offer"]})
    return json_value

def create_message(packet, handler):
    message_dic = packet["DATA"]
    if message_dic['messageType'] == 'chatMessage':
        message = create_chat_json(message_dic, handler) 
        return message
    elif message_dic['messageType'] == 'webRTC-offer':
        message = create_webRTC_json(message_dic)
        return message

def compute_frame_bytes(frame, message):
    final_bytes = b''
    bytes_split = re.findall("........", frame)
    for byte in bytes_split:
        byte_value = int(byte, 2)
        final_bytes += byte_value.to_bytes(1, 'big')
    final_bytes += message.encode()
    return final_bytes

def build_frame_packet(packet, handler):
    frame = "100000010"
    message_json = create_message(packet, handler)
    frame = compute_payload_packet(len(message_json), frame)
    frame_bytes = compute_frame_bytes(frame, message_json)
    return frame_bytes


