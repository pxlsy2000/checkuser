#!/usr/local/bin/python2.7
import os
import sys
import time
import requests


def get_ip_info(ip):
    result = {}
    r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s' % ip)
    if r.json()['code'] == 0:
        i = r.json()['data']

        result['country'] = i['country']
        result['area'] = i['area']
        result['region'] = i['region']
        result['city'] = i['city']
        result['isp'] = i['isp']

        return result
    else:
        return result



def main():
    # get result
    result_fname = '/home/pxlsy2000/sslogs/ss_user_443.log'

    ip_list = []

    f = open(result_fname)
    lines = f.readlines()
    f.close()

    for line in lines:
        #pdb.set_trace()
        unit={}
        #line=line.decode('UTF-8')
        line = line.split('#')
        unit['ip']=line[0].strip()
        unit['location']=line[1].strip()
        unit['last']=line[2].strip()
        unit['text']=line[3].strip()

        ip_list.append(unit)


    f = os.popen("netstat -anp | grep 'ESTABLISHED' | grep '443' ")
    lines = f.readlines()
    f.close()
    for line in lines:
        sline = line.split()
        port = sline[3].split(':')[1]
        ip = sline[4].split(':')[0]

        if port == '443':
            exist_flag=False
            for idx, item in enumerate(ip_list):
                #pdb.set_trace()
                if ip == item['ip']:
                    #update time
                    ctime=time.strftime('%y-%m-%d-%H:%M',time.localtime(time.time()))
                    ip_list[idx]['last']=ctime
                    ip_list[idx]['text']=line.strip()
                    exist_flag=True
                else:
                    continue
            #notexist
            if not exist_flag:
                info=get_ip_info(ip)
                item={}
                item['ip']=ip
                tmp="%s,%s,%s,%s"%(info['country'],info['region'],info['city'],info['isp'])
                item['location']=tmp.encode('UTF-8')
                ctime=time.strftime('%y-%m-%d-%H:%M',time.localtime(time.time()))
                item['last']=ctime
                item['text']=line.strip()
                ip_list.append(item)

        else:
            pass

    new_lines=[]
    for i in ip_list:
        line="%s # %s # %s # %s \n"%(i['ip'],i['location'],i['last'],i['text'])
        new_lines.append(line)

    f = open(result_fname, 'w')
    f.writelines(new_lines)
    f.close()

def now(detail):

# current
    f = os.popen("netstat -anp | grep 'ESTABLISHED' | grep '443' ")
    lines = f.readlines()
    f.close()

    ip_list=[]
    dict_list=[]
    for line in lines:
        sline = line.split()
        port = sline[3].split(':')[1]
        ip = sline[4].split(':')[0]

        if port == '443':
            if ip not in ip_list:
                ip_list.append(ip)
                item={}
                info=get_ip_info(ip)
                item['ip']=ip
                tmp="%s,%s,%s,%s"%(info['country'],info['region'],info['city'],info['isp'])
                item['location']=tmp.encode('UTF-8')
                item['text']=line.strip()
                dict_list.append(item)


    print('now ss user is:')
    for i in dict_list:
        print('\t%s # %s'%(i['ip'],i['location']))
        if(detail):
            print('\t  %s'%i['text'])

#total
    result_fname = '/home/pxlsy2000/sslogs/ss_user_443.log'

    ip_list = []

    f = open(result_fname)
    lines = f.readlines()
    f.close()

    for line in lines:
        #pdb.set_trace()
        unit={}
        #line=line.decode('UTF-8')
        line = line.split('#')
        unit['ip']=line[0].strip()
        unit['location']=line[1].strip()
        unit['last']=line[2].strip()
        unit['text']=line[3].strip()

        ip_list.append(unit)

    print('all logged user:')
    for i in ip_list:
        print('\t%s # %s # %s'%(i['ip'],i['location'],i['last']))
        if(detail):
            print('\t   %s'%i['text'])




if __name__ == '__main__':
    if sys.argv[1]=='log':
        #main()
    	while(1):
    		main()
    		time.sleep(120)
    elif sys.argv[1]=='now':
        now(False)
    elif sys.argv[1]=='now_detail':
        now(True)
    else:
        pass
