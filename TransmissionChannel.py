import numpy
import random


class TransmissionChannel():

    @staticmethod
    def pass_gilbert(data):

        # pz >> pd

        is_in_good_state = True

        pd = 1  # Prawdopodobieństwo błędu w stanie dobrym modelu
        pz = 0.5  # Prawdopodobieństwo błędu w stanie złym modelu

        pdz = 0.001  # Prawdopodobieństwo przejścia modelu ze stanu dobrego do złego
        pzd = 0.02  # Prawdopodobieństwo przejścia modelu ze stanu złego do dobrego

        mg = [[1 - pdz, pdz],  # Macierz symulująca układ gilberta
              [pzd, 1 - pzd]]

        data = numpy.array(data)

        for i in range(data.size):
            noise = 0
            for x in range(8):
                noise *= 2
                if is_in_good_state:
                    if random.random() < mg[0][1]:
                        is_in_good_state = False
                    if random.random() >= pd:
                        noise += 1
                else:
                    if random.random() < mg[1][0]:
                        is_in_good_state = True
                    if random.random() >= pz:
                        noise += 1
            data.itemset(i, data.item(i) ^ noise)
        return data

    @staticmethod
    def pass_bsc(data):
        p = 0.05
        data = numpy.array(data)
        for i in range(data.size):
            noise = 0
            for x in range(8):
                noise *= 2
                if random.random() < p:
                    noise += 1
            data.itemset(i, data.item(i) ^ noise)
        return data

    @staticmethod
    def pass_interleave(arr):
        arr_out = numpy.empty(arr.size, numpy.uint8)
        size_mod = arr.size % 8
        for i in range(0, arr.size - size_mod, 8):
            for j in range(7, -1, -1):
                dataword = arr.item(i + j)
                for k in range(8):
                    arr_out.itemset(i + k, arr_out.item(i + k) * 2)
                    arr_out.itemset(i + k, arr_out.item(i + k) + dataword % 2)
                    dataword //= 2
        for i in range(arr.size - size_mod, arr.size):
            arr_out.itemset(i, arr.item(i))
        return arr_out






