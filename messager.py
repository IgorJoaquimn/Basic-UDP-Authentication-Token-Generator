import struct
import re


ERROR_CODES = {
    1: "INVALID_MESSAGE_CODE - Sent when the client sent a request with an unknown type",
    2: "INCORRECT_MESSAGE_LENGTH - Sent when the client sent a request with incompatible size",
    3: "INVALID_PARAMETER - Sent when the server detects an error in any field of a request",
    4: "INVALID_SINGLE_TOKEN - Sent when one SAS in a GAS is invalid",
    5: "ASCII_DECODE_ERROR - Sent when a message contains a non-ASCII character"
}


class RequestError(Exception):
    def __init__(self, error_code):
        message = ERROR_CODES[error_code]
        self.message = message
        super().__init__(message)


class messager:
    def __init__(self, program_type):
        self.program_type = program_type

        if program_type == "itv":
            self.request = self.itv_request
            self.response = self.itv_response
        elif program_type == "itr":
            self.request = self.itr_request
            self.response = self.itr_response
        elif program_type == "gtr":
            self.request = self.gtr_request
            self.response = self.gtr_response
        elif program_type == "gtv":
            self.request = self.gtv_request
            self.response = self.gtv_response
        else:
            raise ValueError("Invalid program_type")
        

    def check_error_message(self, response):

        if(len(response) != 4): # A 4 bytes message is always an error
            return response

        error_message_format = '>HH'
        values = struct.unpack(error_message_format, response)
        raise RequestError(values[1])

    def parse_sas(self,sas):
        # Regular expression pattern to match the SAS format
        try:
            idd,nonce,token = sas.split(":")
            return idd,int(nonce),token
        except:
            raise ValueError("No id:nonce:token pattern found in the IFS4 token")

    def itr_request(self, params):
        ID, nonce = params
        nonce = int(nonce)
        packet_format = ">H 12s I"

        type_i = 1

        packet = struct.pack(packet_format, 
            type_i, 
            bytes(ID, encoding="ascii"), 
            nonce
            )

        self.packet_format = packet_format
        return packet

    def itr_response(self, response):
        packet_format = ">2s 12s I 64s"
        values = struct.unpack(packet_format, response)
        return values

    def itv_request(self, params):
        ID,nonce,token = self.parse_sas(params[0])
        packet_format = ">H 12s I 64s"

        type_i = 3
        packet = struct.pack(packet_format, 
            type_i, 
            bytes(ID, encoding="ascii"), 
            nonce,
            bytes(token, encoding="ascii")
            )

        self.packet_format = packet_format
        return packet

    def itv_response(self,response):
        packet_format = ">2s 12s I 64s 1s"
        values = struct.unpack(packet_format, response)
        return values

    def gtr_request(self, params):
        type_i = 5

        N = int(params[0])
        sass =  [self.parse_sas(p) for p in params[1:]]


        packet_format_sas = ">12s I 64s "
        sas_packets = [struct.pack(packet_format_sas,bytes(ID, encoding="ascii"),nonce,bytes(token, encoding="ascii")) for (ID,nonce,token) in sass]
        sas_packets = b''.join(sas_packets)
        packet_format = ">2s 2s"


        packet = struct.pack(packet_format, 
            type_i.to_bytes(2,"big"), 
            N.to_bytes(2,"big")
            ) +  sas_packets
        
        self.packet_format = (packet_format_sas * N).replace(">","")
        self.packet_format = ">H H " + self.packet_format
        return packet 

    def gtr_response(self,response):
        packet_format = self.packet_format + "64s"
        print(packet_format)
        values = struct.unpack(packet_format, response)
        return values

    def gtv_request(self, params):
        type_i = 7
        N = int(params[0])
        params = params[1].split("+")
        sass =  [self.parse_sas(p) for p in params[:-1]]
        token_g = params[-1]

        packet_format_sas = ">12s I 64s "
        sas_packets = [struct.pack(packet_format_sas,bytes(ID, encoding="ascii"),nonce,bytes(token, encoding="ascii")) for (ID,nonce,token) in sass]
        sas_packets = b''.join(sas_packets)
        packet_format = ">2s 2s"


        packet = struct.pack(packet_format, 
            type_i.to_bytes(2,"big"), 
            N.to_bytes(2,"big")
            ) + sas_packets + struct.pack("> 64s",bytes(token_g, encoding="ascii"))
        
        self.packet_format = (packet_format_sas * N).replace(">","")
        self.packet_format = ">2s 2s " + self.packet_format + "64s"
        return packet 

    def gtv_response(self,response):
        packet_format = self.packet_format + "1s"
        values = struct.unpack(packet_format, response)
        return values
