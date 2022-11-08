import ctypes


async def generate_token(data):
    library = ctypes.cdll.LoadLibrary('./utils/token/library.so')

    create_token = library.createToken

    create_token.argtypes = [ctypes.c_char_p]

    i = 0
    data_string = "{"
    for param in data:
        i += 1
        if i < len(data):
            data_string += "\"" + str(param) + "\": \"" + str(data[param]) + "\", "
        else:
            data_string += "\"" + str(param) + "\": \"" + str(data[param]) + "\""

    data_string += "}"

    data = create_token(data_string.encode('utf-8'))
    data_bytes = ctypes.string_at(data)
    data_string = data_bytes.decode('utf-8')

    return data_string
