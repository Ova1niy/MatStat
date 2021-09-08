

class GroupedSelection:
    def __init__(self, task_path, answer_path):
        # ranges = []     # диапазоны значений
        # if input('Ranges are float or int(F/I)') == 'F':
        #     ranges = list(map(lambda r: list(map(float, r.split('-'))), input('Enter all ranges').split()))
        # else:
        #     ranges = list(map(lambda r: list(map(int, r.split('-'))), input('Enter all ranges').split()))
        # frequency = list(map(int, input('Enter all frequencies').split()))      # частоты в указанных диапазонах
        f = open(task_path, 'r')
        inp = f.readline().split(', ')

        # print(inp)
        ranges = []  # диапазоны значений
        if inp[0] == 'F':
            ranges = list(map(lambda r: list(map(float, r.split('_'))), inp[1].split()))
        else:
            ranges = list(map(lambda r: list(map(int, r.split('_'))), inp[1].split()))
        frequency = list(map(int, inp[2].split()))  # частоты в указанных диапазонах
        # print(ranges)
        # print(frequency)
        f.close()
        k = len(frequency)
        self.k = k
        self.n = sum(frequency)
        b = ranges[0][1] - ranges[0][0]     # длина интервала группировки
        mfr = frequency.index(max(frequency))       # индекс самого "популярного" интервала
        d = (ranges[mfr][1] + ranges[mfr][0]) / 2       # выборочная мода
        u = []
        for i in range(k):
            z = (ranges[i][1] + ranges[i][0]) / 2
            u.append((z - d) / b)
        self.new_sample = u
        self.frequency = frequency
        sum_first_pow = sum(self.get_product(self.frequency, u, 1))
        sum_second_pow = sum(self.get_product(self.frequency, u, 2))
        sum_third_pow = sum(self.get_product(self.frequency, u, 3))
        sum_fourth_pow = sum(self.get_product(self.frequency, u, 4))

        self.mean = self.get_mean(sum_first_pow, self.n, b, d)
        self.u_dispertion = self.get_u_dispersion(sum_first_pow, sum_second_pow, self.n)
        self.dispertion = self.get_x_dispersion(self.u_dispertion, b)
        self.skewness = self.get_skewness(self.u_dispertion, sum_first_pow, sum_second_pow, sum_third_pow, self.n)
        self.kurtosis = self.get_kurtosis(self.u_dispertion, sum_first_pow,
                                          sum_second_pow, sum_third_pow, sum_fourth_pow, self.n)

        f = open(answer_path, 'w')
        f.writelines('Среднее: ' + str(round(self.mean, 3)) +
                     '\nДисперсия: ' + str(round(self.dispertion, 3)) +
                     '\nКоэф. ассиметрии: ' + str(round(self.skewness, 3)) +
                     '\nКоэф. эксцесса: ' + str(round(self.kurtosis, 3)))
        f.close()

    def get_product(self, freq, sample, power):
        return [n_i * (u_i ** power) for n_i, u_i in zip(freq, sample)]

    def get_mean(self, sum_first_pow, n, b, d):
        return b * (sum_first_pow / n) + d

    def get_u_dispersion(self, sum_first_pow, sum_second_pow, n):
        return (sum_second_pow - (sum_first_pow ** 2 / n)) / n

    def get_x_dispersion(self, u_dispersion, b):
        return u_dispersion * b * b

    def get_skewness(self, u_dispersion, sum_first_pow, sum_second_pow, sum_third_pow, n):
        temp = (sum_third_pow / n) - 3 * (sum_second_pow / n) * (sum_first_pow / n) + 2 * ((sum_first_pow / n) ** 3)
        return temp * (1 / (u_dispersion ** 1.5))

    def get_kurtosis(self, u_dispersion, sum_first_pow, sum_second_pow, sum_third_pow, sum_fourth_pow, n):
        temp = (sum_fourth_pow / n) - 4 * (sum_third_pow / n) * (sum_first_pow / n) + 6 * (sum_second_pow / n) * \
               ((sum_first_pow / n) ** 2) - 3 * ((sum_first_pow / n) ** 4)
        return temp * (1 / u_dispersion ** 2) - 3

