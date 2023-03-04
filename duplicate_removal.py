import re


def file_to_list_of_lists(file_in):
    file_in = open(file_in, "r", errors="ignore")

    arr_out = []

    main_pattern = re.compile('[^a-zA-Z0-9!?. ]')
    single_letter_pattern = re.compile('(?<=\s)[^!?.](?=\s)')
    multiple_spaces_pattern = re.compile('( +)')

    for line in file_in:
        curr_line = line[15:]
        curr_line = re.sub(main_pattern, '', curr_line)
        curr_line = re.sub(single_letter_pattern, '', curr_line)
        curr_line = re.sub(multiple_spaces_pattern, ' ', curr_line)
        article_split = re.split("\.|!|\?", curr_line)
        article_split_and_filtered = []
        for element in article_split:
            if len(element) > 1:
                article_split_and_filtered.append(element)

        arr_out.append(article_split_and_filtered)

    file_in.close()
    return arr_out


def get_sentence_with_spaces_trimmed(sentence_in):
    multiple_spaces_pattern = re.compile('( +)')
    sentence = re.sub(multiple_spaces_pattern, ' ', sentence_in)
    if sentence[0] == ' ':
        sentence = sentence[1:]
    if sentence[-1] == ' ':
        sentence = sentence[:-1]
    return sentence


def remove_duplicates(file_in_name, list_of_sentence_list, final_out, duplicates_out, duplicate_comparison_file=None, sentences_that_dont_count_as_dups=[],
                      sentence_len_threshold=5, match_threshold=5):

    if duplicate_comparison_file!=None:
        duplicate_comparison_file=f"{sentence_len_threshold}_{match_threshold}_{duplicate_comparison_file}"
    file_in = open(file_in_name, "r", errors="ignore")
    final_out = open(final_out, "w", encoding="utf-8")
    duplicates_out = open(duplicates_out, "w", encoding="utf-8")

    lines_to_exclude = []
    all_duplicates = []
    duplicate_source_and_target_array=[]

    len_list = len(list_of_sentence_list)
    for sentence_list_it_outer in range(len(list_of_sentence_list)):
        candidate = list_of_sentence_list[sentence_list_it_outer]
        for sentence_list_it_inner in range(len(list_of_sentence_list)):
#            if sentence_list_it_outer == 70 and sentence_list_it_inner == 94:
#                print("def a dup")
            match_count = 0
            comparison_target = list_of_sentence_list[sentence_list_it_inner]
            for sentence in candidate:
                sentence_spaces_trimmed=get_sentence_with_spaces_trimmed(sentence)
                sentence_count_word_count = len(re.split(' ', sentence_spaces_trimmed))
                if (sentence_count_word_count >= sentence_len_threshold) and (
                        sentence_list_it_outer != sentence_list_it_inner) and (
                        sentence_spaces_trimmed not in sentences_that_dont_count_as_dups) and (sentence in comparison_target):
                    match_count += 1
                    print("Sentence Matched Between articles: " + sentence + "\n")
            if match_count >= match_threshold:
                all_duplicates.append(sentence_list_it_inner)
                all_duplicates.append(sentence_list_it_outer)
                lines_to_exclude.append(sentence_list_it_inner)
                duplicate_source_and_target_array.append([sentence_list_it_inner, sentence_list_it_outer])

        print(f"Process looking for duplicates: {sentence_list_it_outer + 1} / {len_list}")
    all_duplicates.sort()

    print("post processing and writing to files.")
    line_num = 0
    for line in file_in:
        if line_num not in lines_to_exclude:
            final_out.write(line)
        if line_num in all_duplicates:
            duplicates_out.write(line)
        if duplicate_comparison_file:
            for element_outer in range(len(duplicate_source_and_target_array)):
                for element_inner in range(len(duplicate_source_and_target_array[element_outer])):
                    if duplicate_source_and_target_array[element_outer][element_inner] == line_num:
                        duplicate_source_and_target_array[element_outer][element_inner] = line
        line_num += 1

    file_in.close()

    if duplicate_comparison_file:

        #sort array
        for element in duplicate_source_and_target_array:
            element.sort()
        duplicate_source_and_target_array.sort()

        #remove duplicates
        duplicate_source_and_target_array_processed=[]
        for element_num in range(len(duplicate_source_and_target_array)-1):
            if duplicate_source_and_target_array[element_num] != duplicate_source_and_target_array[element_num+1]:
                duplicate_source_and_target_array_processed.append(duplicate_source_and_target_array[element_num])
        duplicate_source_and_target_array_processed.append(duplicate_source_and_target_array[-1])

        #replace numbers with text
        file_in = open(file_in_name, "r", errors="ignore")
        line_num = 0
        for line in file_in:
            for element_outer in range(len(duplicate_source_and_target_array)):
                for element_inner in range(len(duplicate_source_and_target_array[element_outer])):
                    if duplicate_source_and_target_array[element_outer][element_inner] == line_num:
                        duplicate_source_and_target_array[element_outer][element_inner] = line
            line_num += 1
        file_in.close()

        #write_to_file
        duplicate_comparison_file=open(duplicate_comparison_file, "w", encoding="utf-8")
        for element_outer in duplicate_source_and_target_array_processed:
            for element_inner in element_outer:
                duplicate_comparison_file.write(element_inner+"\n")
            duplicate_comparison_file.write("\n")
        duplicate_comparison_file.close()


    final_out.close()
    duplicates_out.close()
