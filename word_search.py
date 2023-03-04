import re


def secondary_list_replace_spaces(secondary_list):
    list_out = []
    for element in secondary_list:
        list_out.append(element.replace(" ", "[^.?!]*"))
    return list_out


def concat_list_with_regex_ors(list_in):
    list_out = []
    first = False
    out = "[^.?!]*"
    for x in list_in:
        x = "[^.?!]*" + x
        if first is False:
            first = True
            out += x
        else:
            out += "|" + x
        list_out.append(out)
    return out


def gen_regex_pattern(primary_list, secondary_list):
    secondary_list=secondary_list_replace_spaces(secondary_list)
    pattern_part2 = concat_list_with_regex_ors(secondary_list)
    pattern_part1 = concat_list_with_regex_ors(primary_list)
    # do note that this pattern isn't for searching multiline strings (specifically the \\n at the end can cause uninteded behaviour)
    regex_pattern = f'(\.|!|\?|@@)(?={pattern_part1})(?={pattern_part2})'+r'[^.?!]*(\.|!|\?|\n|\Z)'
    print(regex_pattern)
    return regex_pattern


def word_search(primary_list, secondary_list, input_file, output_file):
    regex_pattern = gen_regex_pattern(primary_list, secondary_list)
    pattern = re.compile(regex_pattern)

    input_file = open(input_file, "r", errors="ignore")
    output_file = open(output_file, "w", encoding="utf-8")
    article_count=0
    for line in input_file:
        if pattern.match(line):
            output_file.write(line)
        print(f"Performed word search on: {article_count} articles")
        article_count+=1

    input_file.close()
    output_file.close()
    return




