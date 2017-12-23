import scrapy
import codecs

class YahooSpider(scrapy.Spider):
    name = "yahoo"
    allowed_domains = ["answers.yahoo.com"]
    start_urls = [
    ]

    def parse(self, response):
        query = response.meta['query']
        index = response.meta['index']
        for sel in response.css('a[data-ylk*=ql]'):
            href = sel.css('::attr(href)').extract()
            ques = sel.css('::text').extract()
            url = response.urljoin(href[0])
            #print "URL=",url
            yield scrapy.Request(url, callback=self.parse_dir_contents, meta={'ques' : ques,'query':query,'index' : index})
            
    def parse_dir_contents(self, response):
        ques = response.meta['ques']
        query = response.meta['query']
        index = response.meta['index']
        quesPopularity = response.css('span[itemprop*=answerCount]::text').extract()
        
        
        for sel in response.css('.Mstart-75'):
            ans = sel.css('span').css('.ya-q-full-text').css('::text').extract()
            ansLife = sel.css('span[class*=Clr-88]::text').extract()
            upvote = sel.css('div[class*=count]').css('[itemprop=upvoteCount]::text').extract()
            downvote = sel.css('div[class*=count]').css(':not([itemprop])::text').extract()
            print "Query:",index,query
            print "Question:",''.join(ques).encode('utf-8').strip()
            print "Popularity:",''.join(quesPopularity).encode('utf-8').strip()
            print "Answer:",''.join(ans).encode('utf-8').strip()
            print "Lifetime:",''.join(ansLife).encode('utf-8').strip()
            print "upVotes:",''.join(upvote).encode('utf-8').strip()
            print "downVotes:",''.join(downvote).encode('utf-8').strip()

    def start_requests(self):
        with codecs.open(r"C:\Python27\myProgs\qa_questions_551-893.txt", u"r", encoding=u"GB18030") as f:
            for index, line in enumerate(f):
                try:
                    url="https://answers.yahoo.com/search/search_result?fr=uh3_answers_vert_gs&type=2button&p="
                    query = line.strip()
                    url = url+query

                    yield scrapy.Request(url,meta={'query' : query,'index' : index})
                except:
                    continue            


