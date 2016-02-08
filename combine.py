from true_type import get_type

def read_multiple_csv(files, key_header, acceptable_keys=None):
    """
    takes a list of filesnames and a key_header string to merge the files. 
    Can merge if there are different columns in the files, different records in
    the files. 
    Assumption - all the files should have the column named key_header
    example : files = ['grades.csv', 'previous_grades.csv']
    key_header = 'email'
    merged_data = read_multiple_csv(files, key_header)
    """
    data = {}
    # files = ['assignments.csv', 'discuss.csv', 'questions.csv']
    # key_header = 'email'
    # acceprable keys are list of keys allowed to go into final data
    # if not given all will be accepted, this list can come out of 
    # intersection or other set methods
    header_line = []
    import pdb
    pdb.set_trace()

    for filename in files:
        with open(filename, 'r+') as fo:
            headers = fo.readline().split(',')
            headers = [h.strip() for h in headers]
            header_line.extend(headers)

            for line in fo:
                splits = line.split(',')
                inner_dict = {}
                for k,header in enumerate(headers):
                    #assumes header is a string. probably it is
                    if header is not '':
                        inner_dict[header] = int(splits[k]) if get_type(splits[k]) is int else splits[k].strip()
                data_key = inner_dict.pop(key_header)
                if data_key in acceptable_keys:
                    try:
                        z = data[data_key].copy()
                    except KeyError:
                        z = {}
                    z.update(inner_dict)
                    data[data_key] = z
            data['headers'] = list(set(header_line))
    return data
            
def write_combined_csv(data, file_name='combined.csv'):
    import csv
    #headers = ['email']
    headers = data.pop('headers')
    #headers.extend(data[data.keys()[0]].keys())
    list_data = []
    for email, inner_dict in data.items():
        inner_dict['email'] = email
        list_data.append(inner_dict)
    with open(file_name, 'wb') as combined_file:
        dict_writer = csv.DictWriter(combined_file, headers)
        dict_writer.writeheader()
        dict_writer.writerows(list_data)


def get_intersection_keys(files, key_header):
    keys = None
    for filename in files:
        with open(filename, 'r+') as fo:
            headers = fo.readline().split(',')
            key_header_index = headers.index(key_header)
            file_keys = []
            for line in fo:
                line_data = line.split(',')
                file_keys.append(line_data[key_header_index])
            keys = keys & set(file_keys) if keys else set(file_keys)

    return keys


