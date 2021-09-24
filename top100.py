from collections import Counter
import os

try:
    from top100conf import logsize 
except:
    logsize = 0

def read_top (file):
    topsum = {}
    with open(file,'r') as infile:
        for line in infile:
            (key,val) = line.split()
            topsum[key] = int(val)
    return dict(topsum)

def write_top (file, top_dict):
    with open(file,'w+') as outfile:
        for key,val in top_dict.items():
            outfile.write(key+' '+str(val)+'\n')

def access_log_read (file):
    urlday = []
    urlignore = []
    try:
        with open('topignore.txt','r') as infile:
            for row in infile:
                row=row.rstrip("\n")
                urlignore.append(row)
    except:
        pass
    with open(file,'r') as infile:
        for row in infile:
            if not any(url in row for url in urlignore):
                if row not in urlignore:
                    if "\"GET" not in row.split(' ')[6] and row.split(' ')[6] not in urlignore:
                        urlday.append(row.split(' ')[6])
                    elif "\"GET" in row.split(' ')[6]:
                        urlday.append(row.split(' ')[7])
    return urlday

def write_log_size (logsize):
    with open('top100conf.py','w') as outfile:
        outfile.write(f"logsize={logsize}")

def check_exist(file):
    if not os.path.exists(file):
        with open(file, 'w'): pass

def write_top_html(file,tophtml):
    tbl_fmt = '''
    <table>{}
    </table>'''
    row_fmt = '''
      <tr>
        <td>{}</td>
        <td>{}</td>
      </tr>'''
    tophun={}
    for k,v in list(tophtml.items())[:100]:
        tophun[k]=v
    with open(file,'w') as outfile: 
        outfile.write(tbl_fmt.format(''.join(row_fmt.format(k, v) for k, v in tophun.items())))

def main():
    # Files variables
    accesslog = 'access.log'
    topfile = 'top100.txt'
    topfilemon = 'top100mon.txt'
    topfilehtml = 'top100.html'

    #Check files exist or creates it
    check_exist(topfile)
    check_exist(topfilemon)
    check_exist('top100conf.py')

    # Check if log file not rotated
    logsizecurr = os.path.getsize(accesslog)
    if logsize > logsizecurr:
        topold=read_top(topfile)
        topmon=read_top(topfilemon)
        write_top(topfilemon, dict(sorted((Counter(topday)+Counter(topmon)).items(), key=lambda x: x[1], reverse=True)))
        os.remove(topfile)

    write_log_size(logsizecurr)

    # Count top 100 ulrs in log
    #urlday = []
    urlday = access_log_read(accesslog)
    urlcount = Counter(urlday)
    topday = dict(sorted(urlcount.items(), key=lambda x: x[1], reverse=True))
    write_top(topfile, topday)
    write_top_html(topfilehtml,topday)

if __name__ == "__main__":
    main()