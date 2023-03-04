import os
import filter_corpus
import word_search
import duplicate_removal

# general variables:
input_files = ['H:\\Articles\\20-12-us0.txt', 'H:\\Articles\\20-12-us1.txt', 'H:\\Articles\\20-12-us2.txt', 'H:\\Articles\\20-12-us3.txt', 'H:\\Articles\\20-12-us4.txt', 'H:\\Articles\\20-12-us5.txt', 'H:\\Articles\\20-12-us6.txt', 'H:\\Articles\\20-12-us7.txt', 'H:\\Articles\\20-12-us8.txt', 'H:\\Articles\\20-12-us9.txt']
sources_file = "H:\\now-sources-2020.txt"

# The name of the super doc! This doc Will be an amalgamation of all the input docs (filtered if you have do_filtering set to True)
corpus_filtered_name = "corpus_filtered_any_source.txt"

# The name of the searched doc! Will be a version of the super doc with only documents that meet the word search if do_word_search=True, if do_word_search = False then the super doc will be renamed this and fed into duplicate removal
corpus_searched_name="corpus_searched_any_source.txt"

#The output of duplicate removal. Will be a version of the searched with duplicates removed if do_duplicate_removal=True, if do_duplicate_removal = False then the searched doc will be renamed this and will be your final output
final_file_out = "final_output_any_source.txt"


# Filtering Variables:


# If you set this variable to False then filtering won't happen and you can ignore the rest of the variables in
do_filtering = True

# Set to None if you don't want to filter by source
#list_of_sources_to_use = ["CNN", "cnn.com", "CNN on MSN.com", "MSN", "msn.com", "New York Times", "nytimes.com", "USA Today", "usatoday.com", "Washington Post", "washingtonpost.com", "Wall Street Journal", "wsj.com", "Newsweek", "newsweek on MSN.com", "The Hill", "thehill.com", "Fox News", "foxnews.com"]
list_of_sources_to_use = None

# start is inclusive, end is exclusive, format is: yy-m-d
date_range_start = "20-12-1"
date_range_end = "21-1-1"

# This allows you to create a new, filtered, version of the sources file. And if it already exists you can use it, saving time.


# Set this variable to True if you want to use preexisting sources file, and False if You don't.
# If it's set to false it will create a file you can use next time (if you are using the same filtering parameters for both runs)
use_existing_sources_file = False
sources_filtered_file = "now-sources-2020-filtered-any-source.txt"


#Word Search Variables:

do_word_search=True

# The word search will look for one of the following. These don't get any special treatment for spaces
primary_list = ["covid19", "covid 19", "covid-19", "coronavirus"]

# and one of these. Words in this list are allowed to be missing the spaces or have words or other stuff replacing or alongside the spaces
secondary_list = ["patent", "innovat", "invent", "therapeutic", "trial", "vaccine candidate", "orphan drug",
                  "food and drug administration approval", "fda emergency approval", "novel therapies",
                  "vaccine", "treatment*", "drug", "antiviral"]


#duplicate removal Variables:

do_duplicate_removal = True

#This file will contain all the articles that got removed
duplicates_file_out = "duplicates_out_any_source.txt"

#This file will contain all pairs identified as duplicates (can be set to None, which will save a small amount of runtime0
duplicate_comparison_file = "duplicate_comparison_any_source.txt"
#duplicate_comparison_file=None

#This variable is how many words need to be in a sentnece for it to be considered as aduplicate sentence
sentence_len_threshold=5
#This is how many duplicate sentences need to be in an article for it to be considered a duplicate article
sentence_count_threshold=5

#This is a list of scentences that shouldn't be considered duplicate senteces if they appear in multiple articles (also last var you need to set)
#If you don't want to use it then set it to empty like so:
#exclude_sentences = []
exclude_sentences = [
        "Today Headlines The most important news stories of the day curated by Post editors and delivered every morning",
        "Get all the stories you needtoknow from the most powerful name in news delivered first thing every morning to your inbox",
        "The Associated Press contributed to this report",
        "Check out what clicking on Foxnews",
        "Stay uptodate on the biggest health and wellness news with our weekly recap",
        "Read more here",
        "The Jerusalem Post Customer Service Center can be contacted with any questions or requests Telephone 2421 Extension Jerusalem Post or 037619056 Fax 035613699Email subsjpost",
        "Company Dow JonesDJ Network Intraday Data provided by FACTSET and subject to terms of use",
        "Historical and current endofday data provided by FACTSET",
        "All quotes are in local exchange time",
        "Realtime last sale data for U",
        "stock quotes reflect trades reported through Nasdaq only",
        "Intraday data delayed at least 15 minutes or per exchange requirements",
        "Keith began writing for the Fool in 2012 and focuses primarily on healthcare investing topics",
        "His background includes serving in management and consulting for the healthcare technology health insurance medical device and pharmacy benefits management industries",
        "Denise Chow Denise Chow is reporter for NBC News Science focused on the environment and space",
        "life long Mac user and Apple enthusiast Yoni Heisler has been writing about Apple and the tech industry at large for over years",
        "His writing has appeared in Edible Apple Network World MacLife Macworld UK and most recently TUAW",
        "When not writing about and analyzing the latest happenings with Apple Yoni enjoys catching Improv shows in Chicago playing soccer and cultivating new TV show addictions the most recent examples being The Walking Dead and Broad City",
        "Except for the headline this story has not been edited by NDTV staff and is published from syndicated feed",
        "It aims to spread awareness about critical health issues facing the country",
        "This material may not be published broadcast rewritten or redistributed",
        "Sign up for the Headlines Newsletter and receive up to date information",
        "Copyright 2020 Scripps Media Inc",
        "Copyright 2020 The Associated Press",
        "Or tip on how your town or community is handling the pandemic",
        "Sign up for the Rebound Newsletter and receive up to date information",
        "Andy is reporter in Memphis who also contributes to outlets like Fast Company and The Guardian",
        "This material may not be published broadcast rewritten or redistributed without permission",
        "comments Welcome to the discussion",
        "Please avoid obscene vulgar lewd racist or sexuallyoriented language",
        "PLEASE TURN OFF YOUR CAPS LOCK",
        "Threats of harming another person will not be tolerated",
        "Do nt knowingly lie about anyone or anything",
        "No racism sexism or any sort of ism that is degrading to another person",
        "Use the Report link on each comment to let us know of abusive posts",
        "We love to hear eyewitness accounts the history behind an article",
        "Some of the information in this story may have changed after publication",
        "As information about the coronavirus pandemic rapidly changes PEOPLE is committed to providing the most recent data in our coverage",
        "Chris Smith started writing about gadgets as hobby and before he knew it he was sharing his views on tech stuff with readers around the world",
        "Whenever he not writing about gadgets he miserably fails to stay away from them although he desperately tries",
        "But that not necessarily bad thing",
        "takes no responsibility for the content or accuracy of the above news articles Tweets or blog posts",
        "Please visit the source responsible for the item in question to report any concerns you may have regarding content or accuracy",
        "The news articles Tweets and blog posts do not represent IMDb opinions nor can we guarantee that the reporting therein is completely factual"
        "NPR transcripts are created on rush deadline by Verb8tm Inc",
        "an NPR contractor and produced using proprietary transcription process developed with NPR",
        "This text may not be in its final form and may be updated or revised in the future",
        "Accuracy and availability may vary",
        "The authoritative record of NPR programming is the audio record",
        "Raw Story readers power David Cay Johnston DCReport which we ve expanded to keep watch in Washington",
        "We ve exposed billionaire tax evasion and uncovered White House efforts to poison our water",
        "We ve revealed financial scams that prey on veterans and legal efforts to harm workers exploited by abusive bosses",
        "And unlike other news outlets we ve decided to make our original content free",
        "But we need your support to do what we do",
        "Unhinged from corporate overlords we fight to ensure no one is forgotten",
        "then let us make small request",
        "The COVID crisis has slashed advertising rates and we need your help",
        "Like you we believe in the power of progressive journalism and we re investing in investigative reporting as other publications give it the ax",
        "We need your support to do what we do",
        "then let us make small request",
        "Andy is reporter in Memphis who also contributes to outlets like Fast Company and The Guardian",
        "Alexi Cohan is general assignment reporter covering local news and government as well as health and medicine stories",
        " Alexi is from Springfield Massachusetts and attended college at Hofstra University in New York where she majored in journalism and Spanish",
        "Alexi professional experience encompasses print television and radio at NY1 CNN en Espa",
        "7FM WRHU and The Republican newspaper",
        "She enjoys making connections with the community she covers and imploring others to use journalism as tool to stay informed and engaged",
        "About the Authors Myra P",
        "Do you have personal experience with the coronavirus you like to share",
        "Updated December 19 2020 Coronavirus What you need to read The Washington Post is providing some coronavirus coverage free including",
        "33month to receive an invite to virtual party with Marco Werman and The World team",
        "We use cookies to understand how you use our site and to improve your experience",
        "To learn more review our Cookie Policy",
        "When you support The World with donation you ensure our incredible newsroom staff can continue the critical work that brings you stories from around the globe",
        "Donate today to help keep our coverage free and open to all",
        "Thank you for your support",
        "Donate 100 or pledge 8",
        "Breaking News Newsletter As it happens Get updates on the coronavirus pandemic and other news as it happens with our free breaking news email alerts",
        "Was this article valuable for you",
        "Valuable Not valuable Additional comments Receive selection of our best stories daily based on your reading preferences",
        "Newsletter Sign up for daily selection of our best stories based on your reading preferences",
        "reporter at Forbes and the author of What Next",
        "Your FiveYear Plan for Life After College published by Simon amp Schuster",
        "have master degree in journalism",
        "com The center is staffed and provides answers on Sundays through Thursdays between 0700 and 1400 and Fridays only handles distribution requests between 700 and 1300 For international customers The center is staffed and provides answers on Sundays through Thursdays between 7AM and 6PM Toll Free number in Israel only 1800574574 Telephone 97237619056 Fax 97235613699 Email subsjpost",
        "Lisa Kashinsky is multimedia journalist covering politics and more for The Boston Herald",
        "graduate of Boston University she previously covered the Merrimack Valley for The EagleTribune and the South Shore for Wicked Local winning awards for her work at both newspapers",
        "Visit ourThe Rebound Detroit place where we are working to help people impacted financially from the coronavirus",
        "We have all the information on everything available to help you through this crisis and how to access it",
        "Sign up for the Rebound Newsletter and receive up to date information",
        "Sign up for the Breaking News Newsletter and receive up to date information",
        "He was most recently reporter at The Lowell Sun",
        "Rick is Massachusetts native and graduated from Boston University",
        "While not reporting he enjoys longdistance running"]

if __name__ == "__main__":

    if do_filtering:
        if use_existing_sources_file:
            ids = filter_corpus.get_ids_from_prefiltered_source(sources_filtered_file)
        else:
            ids = filter_corpus.get_ids_from_unfiltered_source(date_range_start, date_range_end, list_of_sources_to_use,
                                                               sources_file, output_file=sources_filtered_file)

        filter_corpus.create_super_doc(ids, input_files, corpus_filtered_name)
    else:
        filter_corpus.create_super_doc(None, input_files, corpus_filtered_name)

    if do_word_search:
        word_search.word_search(primary_list, secondary_list, corpus_filtered_name, corpus_searched_name)
    else:
        os.rename(corpus_filtered_name, corpus_searched_name)

    if do_duplicate_removal:
        list_of_sentence_lists = duplicate_removal.file_to_list_of_lists(corpus_searched_name)
        duplicate_removal.remove_duplicates(corpus_searched_name, list_of_sentence_lists, final_file_out, duplicates_file_out,
                          duplicate_comparison_file, exclude_sentences, sentence_len_threshold=sentence_len_threshold, match_threshold=sentence_count_threshold)
    else:
        os.rename(corpus_searched_name, final_file_out)



