from datetime import datetime


def get_ids_from_unfiltered_source(date_start, date_end, sources, input_file, output_file=None):
    date_start = datetime.strptime(date_start, "%y-%m-%d")
    date_end = datetime.strptime(date_end, "%y-%m-%d")
    input_file = open(input_file, "r", errors="ignore")
    if output_file:
        output_file = open(output_file, "w", encoding="utf-8")
    list_of_ids = []
    for line in input_file:
        line_list = line.split('\t')
        try:
            if (sources is None or line_list[-3] in sources) and (date_start <= datetime.strptime(line_list[2], "%y-%m-%d") < date_end):
                list_of_ids.append(line_list[0])
                if output_file:
                    output_file.write(line)
        except Exception as e:
            print(f"Skipping line: {line} because of error: {e}")

    input_file.close()
    if output_file:
        output_file.close()
    return list_of_ids


def get_ids_from_prefiltered_source(input_file):
    list_of_ids = []
    input_file = open(input_file, "r", errors="ignore")

    try:
        for line in input_file:
            line_list = line.split('\t')
            list_of_ids.append(line_list[0])
    except Exception as e:
        input_file.close()
        print("Something went wrong, I'm guessing your sources-filtered file is corrupt! Try deleting it and starting "
              "again")
        raise e
    input_file.close()
    return list_of_ids

def create_super_doc_any_id(input_files, output_file):
    output_file = open(output_file, "w", encoding="utf-8")
    x=0
    for doc in input_files:
        curr_file = open(doc, "r", errors="ignore")
        for line in curr_file:
            output_file.write(line)
            x += 1
        curr_file.close()
    output_file.close()
    return

def create_super_doc(ids, input_files, output_file):
    output_file = open(output_file, "w", encoding="utf-8")

    if ids is None:
        create_super_doc_any_id(input_files, output_file)
        return

    x = 0
    for doc in input_files:
        curr_file = open(doc, "r", errors="ignore")
        for line in curr_file:
            id = line.split(" ")[0]
            id = id[2:]
            if id in ids:
                output_file.write(line)
                x += 1
                ids.remove(id)
                if x % 1000 == 0:
                    print(f"Found {x} articles that match source / dates")
        curr_file.close()
    output_file.close()
    return ids

def find_unused_ids(input_files, filtered_sources, super_doc_out, unused_id_file):
    ids = get_ids_from_prefiltered_source(filtered_sources)
    ids=create_super_doc(ids, input_files, super_doc_out)
    unused_file = open(unused_id_file, "w", encoding="utf-8")

    ids.sort()
    for id in ids:
        unused_file.write(id+"\n")
    unused_file.close()

