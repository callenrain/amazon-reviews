from collections import defaultdict

def main():
	infile = file("kindlereviews.txt",'r')
	lines = infile.readlines()
	d = defaultdict(lambda: 0)
	for i in range(len(lines)):
		split_lines = lines[i].split('"')
		split_lines = [word for word in split_lines if word != ',']
		if len(split_lines) == 10:
			small_dict = defaultdict(lambda: 0)
			small_dict["num"] = split_lines[1]
			small_dict["score"] = split_lines[4]
			small_dict["text"] = split_lines[8]
			d[i]=small_dict
		
if __name__=='__main__':
    main()
