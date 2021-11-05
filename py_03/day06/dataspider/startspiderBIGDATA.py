from scrapy.cmdline import execute

execute(['scrapy','crawl','testspider','-a','job_type=大数据技术','-a','start_url=https://search.51job.com/list/000000,000000,0000,00,9,99,%25E5%25A4%25A7%25E6%2595%25B0%25E6%258D%25AE%25E6%258A%2580%25E6%259C%25AF,2,{0}.html?lang=c&postchannel=0000&workyear=99&cotype=99&degreefrom=99&jobterm=99&companysize=99&ord_field=0&dibiaoid=0&line=&welfare='])