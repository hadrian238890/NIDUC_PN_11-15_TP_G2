import numpy
import reedsolo

class Receiver():

    @staticmethod
    def decode_tmr(data, shape):
        data_out = numpy.empty(shape, numpy.uint8)
        for i in range(data_out.size):
            data_out.itemset(i, (data.item(3 * i) & (data.item(3 * i + 1) | data.item(3 * i + 2))) | (
                    data.item(3 * i + 1) & data.item(3 * i + 2)))
        return data_out

    @staticmethod
    def decode_hamming_code(data, shape):
        H = numpy.array([
            [1, 1, 1, 1, 1, 1, 1, 1],
            [0, 0, 0, 1, 1, 1, 1, 0],
            [0, 1, 1, 0, 0, 1, 1, 0],
            [1, 0, 1, 0, 1, 0, 1, 0]], numpy.uint8)

        R = numpy.array([
            [0, 0, 1, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 0, 1, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0]], numpy.uint8)

        data_out = numpy.empty(shape, numpy.uint8)
        codeword_array = numpy.empty(8, numpy.uint8)
        detected = 0
        for i in range(data_out.size):
            dataword = 0
            for j in range(2):
                codeword = data.item(2 * i + 1 - j)
                for x in range(8):
                    codeword_array.itemset(x, codeword % 2)
                    codeword //= 2
                errorcode_array = H.dot(codeword_array)
                errorcode = 0
                for x in range(4):
                    errorcode *= 2
                    errorcode += (errorcode_array.item(x) % 2)
                if errorcode > 0:
                    if errorcode >= 8:
                        if errorcode > 8:
                            errorcode -= 8
                        codeword_array.itemset(errorcode - 1, codeword_array.item(errorcode - 1) ^ 1)
                    else:
                        detected += 1
                datawordArr = R.dot(codeword_array)
                for x in range(4):
                    dataword *= 2
                    dataword += (datawordArr.item(3 - x) % 2)
            data_out.itemset(i, dataword)
        return data_out

    @staticmethod
    def decode_reed_salomon(arr, shape):
        rs = reedsolo.RSCodec(4)
        size_mod = arr.size % 4
        arr_out = numpy.empty(shape, numpy.uint8)
        arr_out.resize(arr_out.size)
        for i in range(0, arr_out.size - size_mod, 4):
            try:
                arr_out[i:i + 4] = numpy.frombuffer(rs.decode(arr[2 * i:2 * i + 8].tobytes()),
                                                    numpy.uint8)
            except reedsolo.ReedSolomonError:
                arr_out[i:i + 4] = arr[2 * i:2 * i + 4]
        for i in range(size_mod):
            arr_out.iteset(arr_out.size - size_mod + i, arr.item((arr_out.size - size_mod) * 2 + i))
        arr_out.resize(shape)
        return arr_out


