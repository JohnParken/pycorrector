#import sys
#sys.path.append('../')
import pycorrector

#@profile 内存监测
def test(path, result_path):
    count, count_all = 0,0
    #_badcase = open('../../positive_badcase.txt','w', encoding='utf-8')
    with open(path, 'r', encoding='utf-8') as file, open(result_path,'w',encoding='utf-8') as wfile:
        line = file.readline()
        while line != None and line != '':
            count_all += 1

            # 用于测试sighan数据的部分代码
            index, origin_string = line.strip().split(' ')[0], line.strip().split(' ')[1]

            #if count_all == 4:
            #    break
            # 用于测试笔录数据的部分代码
            """
            origin_string = line.strip().split(',')[0]
            if len(line.strip().split(',')) > 1:
                origin_string += line.strip().split(',')[1]
            corr_string, detail = pycorrector.correct(origin_string)
           
            if str(detail) == "[]":
                count += 1
            else:
                #wfile.write('{}\t{}\n'.format(corr_string, detail))
                wfile.write('{}\t{}\t{}\n'.format(index, corr_string, detail))
        print('{} / {}'.format(count, count_all)) 
             """
            idx = index.strip().split('=')[1].strip(')')
            idx,corr_string, detail = pycorrector.correct(idx,origin_string)
            wfile.write('{}\t{}\t{}\n'.format(index, corr_string, detail))
            line = file.readline()



if __name__ == '__main__':

    path = './corpus/sighan15.txt'
    result_path = './corpus/sighan15_result.txt'
    test(path, result_path)

