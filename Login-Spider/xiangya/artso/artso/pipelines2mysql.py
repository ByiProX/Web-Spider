import MySQLdb


class ArtsoPipeline(object):
    def process_item(self, item, spider):
        name = item['name']
        writer = item['writer']
        size = item['size']
        type = item['type']
        era = item['era']

        expected_price = item['expected_price']
        real_priceRMB = item['real_priceRMB']
        real_priceHKB = item['real_priceHKB']
        real_priceUSD = item['real_priceUSD']
        real_priceEUR = item['real_priceEUR']

        special_performance = item['special_performance']
        auction_time = item['auction_time']
        auction_company = item['auction_company']
        auction = item['auction']
        url = item['url']


        conn = MySQLdb.connect(
        		host='localhost',
        		port=3306,
        		user='root',
        		passwd='root',
        		db='artsoDB',
        		charset = 'utf8')
        cur = conn.cursor()
        cur.execute("INSERT INTO xiangyaAuction(name,writer,size,type,era,expected_price,real_priceRMB,real_priceUSD,real_priceUSD,real_priceEUR,special_performance,auction_time,auction_company,auction,url) values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (name,writer,size,type,era,expected_price,real_priceRMB,real_priceUSD,real_priceUSD,real_priceEUR,special_performance,auction_time,auction_company,auction,url))
        cur.close()
        conn.commit()
        conn.close()

        return item
