f.write("### Q1 ###\n")
for record in result1:
    f.write("%s, %d\n" % (record['a.name'], record['c']))
    
result2 = transaction.run("MATCH (p:Person)-[r:RATED]->(m:Movie) WHERE r.stars < 4 RETURN m.title")
f.write("\n### Q2 ###\n")
for record in result2:
    f.write("%s \n" % (record['m.title']))
    
result3 = transaction.run("MATCH (p:Person)-[r:RATED]->(m:Movie)<-[:ACTS_IN]-(a:Actor) WITH m, count(a.name) as c RETURN m.title, max(c) as cnt order by max(c) DESC LIMIT 1")
f.write("\n### Q3 ###\n")
for record in result3:
    f.write("%s, %d\n" % (record['m.title'], record['cnt']))

result4 = transaction.run("MATCH (a:Actor)-[:ACTS_IN]->(m:Movie)<-[:DIRECTED]-(d:Director) WITH a,count(distinct d) AS c WHERE c>2 RETURN  a.name, c")
f.write("\n### Q4 ###\n")
for record in result4:
    f.write("%s, %d\n" % (record['a.name'], record['c']))

result5 = transaction.run("MATCH (a2:Actor)-[:ACTS_IN]->(m1:Movie)<-[:ACTS_IN]-(a1:Actor)-[:ACTS_IN]->(m2:Movie)<-[:ACTS_IN]-(bacon:Actor{name:'Kevin Bacon'}) RETURN a2.name")
f.write("\n### Q5 ###\n")
for record in result5:
    f.write("%s\n"% record['a2.name'])

result6 = transaction.run("MATCH (a:Actor{name:'Tom Hanks'})-[ACTS_IN]->(m:Movie) RETURN distinct m.genre")
f.write("\n### Q6 ###\n")
for record in result6:
    f.write("%s\n" % (record['m.genre']))
       
result7 = transaction.run("MATCH (d:Director)-[:DIRECTED]-> (m:Movie) WITH d,count(distinct m.genre) AS c where c>1  RETURN d.name, c")
f.write("\n### Q7 ###\n")
for record in result7:
    f.write("%s, %d\n" %(record['d.name'], record['c']))

result8 = transaction.run("MATCH (a:Actor)-[:ACTS_IN]->(m:Movie)<-[:DIRECTED]-(d:Director) RETURN d.name, a.name, count(m.title) as cnt ORDER BY count(m.title) DESC LIMIT 5")
f.write("\n### Q8 ###\n")
for record in result8:
    f.write("%s, %s, %d\n" % (record['d.name'], record['a.name'], record['cnt']))

transaction.close()
session.close()