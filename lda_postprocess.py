import csv

num_of_topics__criteria_for_cut_words = 20
num_of_appearance__criteria_for_cut_words = 10
output_num_of_words_per_topic = 50

def load_vocab():
    num=0
    vocab = []
    with open('input/title_vocab.csv','rb') as readcsvfile:
        reader = csv.reader(readcsvfile, delimiter=',', quotechar='|')
        for row in reader:
            if num!=0:
                vocab.append(row[1])
            num+=1
    return num-1, vocab

def check_line_is_useless(line, cut_topic, cut_word):
    count = 0
    for i in xrange(1,len(line)):
        if int(line[i]) >= cut_word:
            count+=1
    if count >= cut_topic:
        return True
    return False

def load_lda(num_vocab, vocab, cut_topic, cut_word):
    f = open("input/title_lda.txt","r")
    line = f.readline()
    line = line.split()
    n_topics = len(line)-1
        
    ret = []
    removed_words = []
    index = int(line[0])
    for i in xrange(n_topics):
        ret.append([0] * num_vocab)
    if check_line_is_useless(line, cut_topic, cut_word):
        print vocab[index]
        removed_words.append(vocab[index])
    else:
        for i in xrange(n_topics):
            ret[i][index] = int(line[i+1])
    for line in f:
        line = line.split()
        index = int(line[0])
        if check_line_is_useless(line, cut_topic, cut_word):
            print vocab[index]
            removed_words.append(vocab[index])
        else:
            for i in xrange(n_topics):
                ret[i][index] = int(line[i+1])

    for i in xrange(n_topics):
        ret[i] = list(enumerate(ret[i]))
        ret[i].sort(key=lambda item:item[1], reverse=True)
    
    return removed_words, n_topics, ret
    
def write_csv(lda, vocab, removed_words, n_topic, n_word):
    with open('lda.csv', 'wb') as writecsvfile:
        writer = csv.writer(writecsvfile, delimiter=',', quotechar='|')
        row = []
        for i in range(n_topic):
            row.append("topic" + str(i+1))
        writer.writerow(row)
        for i in range(n_word):
            row = []
            for j in range(n_topic):
                row.append(vocab[lda[j][i][0]])
            writer.writerow(row)
        writer.writerow([])
        removed_words.insert(0,'')
        removed_words.insert(0,'removed_words')
        writer.writerow(removed_words)

num_vocab,vocab = load_vocab()
print "reading vocabulary file finished!"
#remove_words = ['of', 'the', 'and', 'in', 'for', 'a', 'to', 'with', 'by', 'on','at', 'an']
removed_words, num_topic,lda = load_lda(num_vocab, vocab,
                            num_of_topics__criteria_for_cut_words,
                            num_of_appearance__criteria_for_cut_words)
print "processing lda file finished!"
write_csv(lda,vocab, removed_words, num_topic, output_num_of_words_per_topic)
print "writing lda file finished!"
