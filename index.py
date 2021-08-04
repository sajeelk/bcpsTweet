from lxml import html
import requests, time, tweepy, smtplib
from config import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

old = "*** All schools operating on normal posted schedule. ***"

def getStatus(status):
	global old
	status = ""
	page = requests.get('http://www.bcps.org/')
	tree = html.fromstring(page.text)
	if tree.xpath('//*[@id="status"]/div/text()') == ['\r\n', '\r\n\r\n']:
		status = tree.xpath('//*[@id="status"]/span[2]/marquee/span/a/span/text()')
	else:
		try:
			status = tree.xpath('//*[@id="status"]/div/text()')[0]
		except IndexError:
			print "iBoss Error"
			status = old
	if old == status or status == "*** All schools operating on normal posted schedule. ***":
		return "0" + status
	else:
		return "1" + status


auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)
# def sendEmail(status):
# 	fromaddr = 'sajeelk@gmail.com'
# 	toaddrs  = 'sajeelk@gmail.com'
# 	msg = "\r\n".join([
# 	  "From: sajeelk@gmail.com",
# 	  "To: sajeelk@gmail.com",
# 	  "Subject: BCPS status",
# 	  "",
# 	  status
# 	  ])
# 	username = 'sajeelk@gmail.com'
# 	password = ...
# 	server = smtplib.SMTP('smtp.gmail.com:587')
# 	server.ehlo()
# 	server.starttls()
# 	server.login(username,password)
# 	server.sendmail(fromaddr, toaddrs, msg)
# 	server.quit()
while True:
	status = getStatus(old)
	if status[0] == "1":
		status = status[1:]
		# api.update_status("Status of @BaltCoPS:\n" + status + "\nTweeted from script BCPSTweet")
		sendEmail(status)
		print "Sent: '%s'." % status
		old = status
	else:
		print "didn't send"
	time.sleep(1)
