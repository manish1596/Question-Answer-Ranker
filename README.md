Question Answer Ranking System completed as part of the *Exploratory Project in 4th Semester* under the supervision of Prof.A.K. Singh.

### Running Ranker 
1. Run the GBRank.py file.
2. By default it runs on dataTrec99.txt(Data of TREC Evaluation 1999)
3. This can be modified by changing the line 57
from
```fea=process_doc("dataTrec99.txt")```
to
```fea=process_doc(Name Of Data File in String)```

### Generating Data
Yahoo spider conatins python crawler built using scrapy to extract Yahoo Answers data.


### Description
1. The function_h function can be used to calculate score of any question answer tuple in order to compare it with some other tuple corresponding to same query.
2. clfvec is a part of the above function definition and once it is learnt it can be used to score any given feature vector.
3. After running GBrank.py file the clfvec list can be input to function_h to get the final ranking function.

### Authors
1. Manish Kumar Singh  
2. Arjun Malik

