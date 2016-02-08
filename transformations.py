from true_type import get_type
import csv

def numeric_or_zero(string):
    if get_type(string) in [int, float]:
        return get_type(string)(string)
    return 0

def get_percentile(data_list, score, kind='weak'):
    """
    The percentile rank of a score relative to a list of scores.
    A percentile of, for example, 80 percent means that 80 percent of the
    scores in the data_list are below the given score. 
    
    In the case of gaps or ties, the exact definition depends on the type
    of the calculation stipulated by the kind keyword argument.
    
    This function is a modification of scipy.stats.percentileofscore. The 
    only major difference is that I eliminated the numpy dependency, and
    omitted the rank kwarg option until I can get more time to translate
    the numpy parts out.
    h3. Parameters
    
        * data_list: list
            
            * A list of scores to which the score argument is compared.
    
        * score: int or float
            
            * Value that is compared to the elements in the data_list.
            
        * kind: {'rank', 'weak', 'strict', 'mean'}, optional
        
            * This optional parameter specifies the interpretation of the resulting score:
                * "weak": This kind corresponds to the definition of a cumulative
                          distribution function.  A percentileofscore of 80%
                          means that 80% of values are less than or equal
                          to the provided score.
                
                * "strict": Similar to "weak", except that only values that are
                            strictly less than the given score are counted.
                
                * "mean": The average of the "weak" and "strict" scores, often used in
                          testing.      See
    
    h3. Documentation
    
        * "Percentile rank":http://en.wikipedia.org/wiki/Percentile_rank
        * "scipy.stats":http://www.scipy.org/SciPyPackages/Stats
    Example usage::
        Three-quarters of the given values lie below a given score:
            >>> percentileofscore([1, 2, 3, 4], 3)
            75.0
        Only 2/5 values are strictly less than 3:
            >>> percentile([1, 2, 3, 3, 4], 3, kind='strict')
            40.0
        But 4/5 values are less than or equal to 3:
            >>> percentile([1, 2, 3, 3, 4], 3, kind='weak')
            80.0
        The average between the weak and the strict scores is
            >>> percentile([1, 2, 3, 3, 4], 3, kind='mean')
            60.0
    """
    n = len(data_list)

    if kind == 'strict':
        return len([i for i in data_list if i < score]) / float(n) * 100
    elif kind == 'weak':
        return len([i for i in data_list if i <= score]) / float(n) * 100
    elif kind == 'mean':
        return (len([i for i in data_list if i < score]) + len([i for i in data_list if i <= score])) * 50 / float(n)
    else:
        raise ValueError("The kind kwarg must be 'strict', 'weak' or 'mean'. You can also opt to leave it out and rely on the default method.")

def calculate_assignments_attempted():
    csv_file = open('assignments.csv')
    headers_list = csv_file.next().strip().split(',')
    headers_list.append('assignments_submitted')
    lines = [headers_list]

    for line in csv_file:
        splits = line.split(',')
        splits = [f.strip() for f in splits]
        zeroes = len([f for f in splits if f in ['', '0']])
        assignments_submitted = 2 - zeroes
        splits.append(str(assignments_submitted))
        lines.append(splits)

    csv_file.close()

    with open('aaa.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(lines)

def calculate_questions_attempted():
    csv_file = open('questions.csv')
    headers_list = csv_file.next().strip().split(',')
    headers_list.append('questions_attempted')
    lines = [headers_list]

    for line in csv_file:
        splits = line.split(',')
        splits = [f.strip() for f in splits]
        zeroes = len([f for f in splits if f =='0'])
        questions_submitted = 15 - zeroes
        splits.append(str(questions_submitted))
        lines.append(splits)
    
    csv_file.close()

    with open('qqq.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(lines)

def calculate_questions_grade():
    """
    calculates grading for all students
    grade is first calculated as total score normalized by standard deviation 
    across scores. Then scaled to 0-10 from whatever the values are. Usually 
    for good normal distribution across scores, the max normalized score should
    be around 4. But there always can be outliers, like a test which is overly 
    difficult for most people except exceptional people. 
    """
    import numpy as np
    csv_file = open('qqq.csv')
    headers_list = csv_file.next().strip().split(',')
    headers_list.append('questions_grade')
    data_lines = []
    scores = []
    
    for line in csv_file:
        splits = [f.strip() for f in line.split(',')]
        splits = [int(s) if get_type(s) is int else s for s in splits]
        scores.append(splits[2])
        data_lines.append(splits)

    std_dev = np.std(scores)
    grades = [score*1.0/std_dev for score in scores]
    max_grade = max(grades)
    grades = [g*10/max_grade for g in grades]

    graded_lines = [headers_list]
    for key, split_line in enumerate(data_lines):
        split_line.append(round(grades[key], 2))
        graded_lines.append(split_line)

    csv_file.close()

    with open('qqq2.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(graded_lines)

def calculate_assignment_grade():
    import numpy as np
    csv_file = open('aaa.csv')
    headers_list = csv_file.next().strip().split(',')
    headers_list.append('assignment_grade')
    data_lines  = []
    scores = []

    for line in csv_file:
        splits = [f.strip() for f in line.split(',')]
        splits = [int(s) if get_type(s) is int else s for s in splits]
        if splits[3] == '':
            splits[3] = 0
        if splits[4] == '':
            splits[4] = 0
        try:
            scores.append(splits[3] + splits[4])
        except TypeError:
            import ipdb; ipdb.set_trace() 
        data_lines.append(splits)


    non_zero_scores = [s for s in scores if s > 0]
    std_dev = np.std(non_zero_scores)
    grades = [s*1.0/std_dev for s in scores]
    max_grade = max(grades)
    grades = [g*10/max_grade for g in grades]

    graded_lines = [headers_list]
    for key,split_line  in enumerate(data_lines):
        split_line.append(round(grades[key], 2))
        graded_lines.append(split_line)

    csv_file.close()

    with open('aaa2.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(graded_lines)

def calculate_total_grade():
    import numpy as np
    csv_file = open('combined.csv')
    headers_list = csv_file.next().strip().split(',')
    headers_list.append('total_grade')
    data_lines = []
    scores = []
    
    for line in csv_file:
        splits = [f.strip() for f in line.split(',')]
        splits = [int(s) if get_type(s) is int else s for s in splits]
        ph_score = numeric_or_zero(splits[6]) #int(splits[6]) if get_type(splits[6]) is int else 0
        q_score = numeric_or_zero(splits[7])#float(splits[7]) if get_type(splits[7]) is float else 0
        a_score = numeric_or_zero(splits[11]) #float(splits[11]) if get_type(splits[11]) is float else 0
        total_score = ph_score + q_score + a_score
        scores.append(total_score)
        data_lines.append(splits)

    final_lines = [headers_list]
    for key, split_line in enumerate(data_lines):
        split_line.append(round(scores[key], 2))
        final_lines.append(split_line)

    csv_file.close()

    with open('ccc2.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(final_lines)

def calculate_final_percentile():
    csv_file = open('final.csv')
    headers_list = csv_file.next().strip().split(',')
    headers_list.append('percentile')
    lines = [headers_list]
    final_lines = [headers_list]

    scores = []
    for line in csv_file:
        splits = line.split(',')
        splits = [f.strip() for f in splits]
        scores.append(numeric_or_zero(splits[14]))
        lines.append(splits)
        
    for splits in lines[1:]:
        score_percentile = get_percentile(scores, numeric_or_zero(splits[14]))
        splits.append(score_percentile)
        final_lines.append(splits)


    csv_file.close()

    with open('ggg.csv', 'w') as fp:
        a = csv.writer(fp, delimiter=',')
        a.writerows(final_lines)
