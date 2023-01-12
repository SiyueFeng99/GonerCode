import numpy as np
from sklearn.metrics.pairwise import cosine_similarity, pairwise_distances
import csv
from get_txt import listdir
import time
from itertools import islice
from multiprocessing import Pool
from functools import partial
import json


def sim(pairs, npypath, resultpath):
    exc = []

    existnpy = []
    listdir(npypath, existnpy)
    j = 0
    for p in pairs:
        f1 = npypath + p[0].split('.java')[0] + '.npy'
        f2 = npypath + p[1].split('.java')[0] + '.npy'
        if f1 in existnpy and f2 in existnpy:
            matrix1 = np.load(f1)
            matrix2 = np.load(f2)
            cos = cosine_similarity(matrix1, matrix2)

            cosine = []

            for i in range(len(cos[0])):
                cosine.append(cos[i][i])

            data = [f1, f2]
            data.extend(cosine)
            exc.append(data)

            j += 1
            print(j)

    with open(resultpath + 'cos.csv', 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        for row in exc:
            writer.writerow(row)


def main(pairspath, npypath, resultpath):
    pairs = csv.reader(open(pairspath, 'r', encoding='gbk'))

    start1 = time.time()
    sim(pairs, npypath, resultpath)
    end1 = time.time()
    t1 = end1 - start1
    print('sim_time:')
    print(t1)


if __name__ == '__main__':
    main('BCB_clone.csv', './BCB_2_matrix/', './BCB_2gram_clone_')
    main('BCB_nonclone.csv', './BCB_2_matrix/', './BCB_2gram_nonclone_')

