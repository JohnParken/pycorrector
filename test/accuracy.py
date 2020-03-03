import re

def accuracy(result_path, truth_path):
    
    far_list = []
    # DA: correct detected results / all_testing
    corr_detected_results, all_testing = 0, 0
    # FAR
    TTP, TFP = 0, 0
    # DP： correct detected errs/ reported_errs
    corr_detected_errs, reported_errs = 0, 0
    # DR： correct detected errs / all_errors
    all_errors = 0
    # ELA: sentences with correct location detection / all testing sentences
    corr_detected_location, corr_detected_loc_errs, corr_deteted_without_errs = 0, 0, 0
    # CA
    corr_corr_err = 0
    # CP
    sent_with_corr = 0
    
    badcase = open('badcase_word.txt','w',encoding='utf-8')
    with open(result_path, 'r', encoding='utf-8') as result, open(truth_path, 'r', encoding='utf-8') as truth:
        # 将答案写入字典中
        truth_dict = {}
        truth_lines = truth.readlines()
        for line in truth_lines:
            line_list = line.strip().split(',')
            index = line_list[0]
            truth_dict[index] = []
            truth_dict[index].extend(line_list[1:])
        
        
        # 答案与结果进行比对
        result_lines = result.readlines()
        for line in result_lines:
            
            line_list = line.strip().split('\t')
            index = line_list[0].split('=')[1].strip(')')
            detail = line_list[2]
            if len(str(detail)) > 2:
                detail = detail.strip('[]').split('],')
                # print(detail)

            # DA: 探测到句子有错误 / 所有的句子数量 
            all_testing += 1
            if len(str(detail)) == 2 and truth_dict[index][0] == " 0":
                corr_detected_results += 1
            if len(str(detail)) > 2:
                # detail = detail.strip('[]').split('],')
                # print(truth_dict[index])
                for i in range(len(detail)):
                    for j in range(len(truth_dict[index])//2):
                        #print(truth_dict[index][j*2], detail[i].strip('[').split(',')[2],
                        #detail[i].strip('[').split(',')[3])
                        #print(detail)
                        if int(truth_dict[index][j*2]) > int(detail[i].strip('[').split(',')[2]) and \
                        int(truth_dict[index][j*2]) <= int(detail[i].strip('[]').split(',')[3])+1 :
                            corr_detected_results += 1
                            corr_detected_errs += 1
                            break
                    break

            # FAR :  实际上没有错误，但预测有错误了/ 测试用例里实际没有错误的数量
            if truth_dict[index][0] == " 0":
                TTP += 1
                if len(str(detail))!=2:
                    TFP += 1
                    far_list.append(index)
            # DR： 句子有错且探测正确 / 句子本身存在错误
            if truth_dict[index][0] != " 0":
                all_errors += 1
            # DP: 句子有错且探测正确 / 报告有错
            if len(str(detail)) > 2:
                reported_errs += 1
                for i in range(len(detail)):
                    flag = True
                    for j in range(len(truth_dict[index])//2):
                        if int(truth_dict[index][j*2]) > int(detail[i].strip('[').split(',')[2]) and \
                        int(truth_dict[index][j*2]) <= int(detail[i].strip('[').split(',')[3])+1 :
                            flag = flag
                        else:
                            flag = False
                if flag:
                    corr_detected_loc_errs += 1
            # ELA : corr_detected_loc_errs + corr_deteted_without_errs
            if len(str(detail)) == 2 and truth_dict[index][0] == " 0":
                corr_deteted_without_errs += 1 
            # CA
            if len(str(detail)) > 2:
                flags = False
                for j in range(len(truth_dict[index])//2):
                    print(index, str(truth_dict[index][j*2+1]).strip() +"**"+str(detail))
                    if re.search(truth_dict[index][j*2+1].strip(), str(detail)):
                        flags = True
                    else:
                        flags = False
                
                if flags:
                    corr_corr_err += 1
                else:
                    badcase.write('{}\n'.format(line))
            # CP
            if truth_dict[index][0] != " 0":
                sent_with_corr += 1

        corr_detected_location = corr_detected_loc_errs + corr_deteted_without_errs

        FAR = TFP / (TTP+1)
        DA = corr_detected_results / all_testing
        DP = corr_detected_errs / reported_errs
        DR = corr_detected_errs / all_errors
        DF1 = 2 * DP * DR / (DP + DR)
        ELA = corr_detected_location / all_testing
        ELP = corr_detected_loc_errs / reported_errs
        ELR = corr_detected_loc_errs / all_errors
        ELF1 = 2 * ELP * ELR / (ELP + ELR)
        LA = corr_detected_loc_errs / all_testing
        CA = corr_corr_err / all_testing
        CP = corr_corr_err / sent_with_corr
        print('FAR, {}\nDA, {}\nDP, {}\nDR, {}\nDF1, {}\nELA, {}\nELP, {}\nELR, {}\nELF1, {}\nLA, {}\nCA, {}\nCP, {}'
                .format(FAR, DA, DP, DR, DF1, ELA, ELP, ELR, ELF1, LA, CA, CP))
        print('reported_errs, {}\nall_testing, {}\n'.format(reported_errs, all_testing))
        print('lar_list, \n{}'.format(far_list))




if __name__ == '__main__':

    result_path = './sighan13_01_result_char.txt'
    truth_path = './sighan13_01_Truth.txt'
    accuracy(result_path, truth_path)

