import numpy
import reedsolo



class Coder():

    @staticmethod
    def encode_tmr(data):
        data_out = numpy.empty(data.size * 3, numpy.uint8)
        for i in range(data.size):
            data_out.itemset(3 * i, data.item(i))
            data_out.itemset(3 * i + 1, data.item(i))
            data_out.itemset(3 * i + 2, data.item(i))
        return data_out

    @staticmethod
    def encode_hamming_code(data):

        generator_matrix = numpy.array([[1, 1, 0, 1],
                                        [1, 0, 1, 1],
                                        [1, 0, 0, 0],
                                        [0, 1, 1, 1],
                                        [0, 1, 0, 0],
                                        [0, 0, 1, 0],
                                        [0, 0, 0, 1]], numpy.uint8)

        generator_matrix = generator_matrix.transpose()

        hamming_code = numpy.empty(data.size * 2, numpy.uint8)
        dataword_arr = numpy.empty(4, numpy.uint8)
        for i in range(data.size):
            dataword = data.item(i)
            for j in range(2):  # halfword (4 data bits)
                for x in range(4):
                    dataword_arr.itemset(x, dataword % 2)
                    dataword //= 2  # integer division
                codeword_arr = dataword_arr.dot(generator_matrix)
                codeword = 0
                for x in range(7):
                    codeword *= 2
                    codeword += (codeword_arr.item(6 - x) % 2)
                hamming_code.itemset(2 * i + j, codeword)
        return hamming_code

    @staticmethod
    def encode_reed_salomon(arr):
        arr_shape = arr.shape
        arr.resize(arr.size)
        rs = reedsolo.RSCodec(4)
        reedsolo.RSCodec()
        size_mod = arr.size % 4
        rs_code = numpy.empty(arr.size * 2 - size_mod, numpy.uint8)
        for x in range(0, arr.size - size_mod, 4):
            rs_code[2 * x:2 * x + 8] = numpy.frombuffer(rs.encode(arr[x:x + 4].tobytes()),
                                                        numpy.uint8)
        for x in range(size_mod):
            rs_code.itemset((arr.size - size_mod) * 2 + x, arr.item(arr.size - size_mod + x))
        arr.resize(arr_shape)
        return rs_code







