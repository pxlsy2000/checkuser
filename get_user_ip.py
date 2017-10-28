import os
import time
import requests

def get_ip_info(ip):
	result={}
	r = requests.get('http://ip.taobao.com/service/getIpInfo.php?ip=%s'%ip)
	if r.json()['code']==0:
		i = r.json()['data']

		result['country']=i['country']
		result['area']	 =i['area']
		result['region'] =i['region']
		result['city']   =i['city']
		result['isp']    =i['isp']
			
		return result
	else:
		return result
		

def test():
	result_fname = '/home/pxlsy2000/sslogs/ss_user_443.log.bck'
	new_fname= '/home/pxlsy2000/sslogs/test.log'
	
	ans_list = []

	f = open(result_fname)	
	lines = f.readlines()
	f.close()
	for line in lines:
		ans={}
		ip=line.strip()
		ans=get_ip_info(ip)
		ans['ip']=ip
		ans_list.append(ans)
	
	newlines=[]
	for a in ans_list:
		newlines.append("%s: %s,%s,%s,%s,%s\n"%(a['ip'],a['country'],a['area'],a['region'],\
					       a['city'], a['isp']))

	for i in newlines:
		print(i)
	f=open(new_fname,'w')
	f.writelines(newlines)
	f.close()
	
		


def main():
	# get result
	result_fname = '/home/pxlsy2000/sslogs/ss_user_443.log'
	
	ip_list = []

	f = open(result_fname)	
	lines = f.readlines()
	f.close()
	for line in lines:
		ip_list.append(line.strip())
	

	f = os.popen("netstat -anp | grep 'ESTABLISHED' | grep '443' ")
	lines = f.readlines()
	f.close()
	for line in lines:
		line=line.split()
		port = line[3].split(':')[1]
		ip = line[4].split(':')[0]
		
		if port=='443':
			if ip not in p7508_list:
				p7508_list.append(ip)
			else:
				pass

		else:
			pass

	f = open(p7508_result_fname, 'w')
	for i in p7508_list:
		f.write(i+'\n')
	f.close()


	
			
				
		



if __name__ == '__main__':
#	while(1):	
#		main()
#		time.sleep(10)
	test()
