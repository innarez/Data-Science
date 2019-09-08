import sqlite3 as lite
import csv
import re
con = lite.connect('cs1656.sqlite')

with con:
    cur = con.cursor() 

	########################################################################		
	### CREATE TABLES ######################################################
	########################################################################		
	# DO NOT MODIFY - START 
    cur.execute('DROP TABLE IF EXISTS Actors')
    cur.execute("CREATE TABLE Actors(aid INT, fname TEXT, lname TEXT, gender CHAR(6), PRIMARY KEY(aid))")

    cur.execute('DROP TABLE IF EXISTS Movies')
    cur.execute("CREATE TABLE Movies(mid INT, title TEXT, year INT, rank REAL, PRIMARY KEY(mid))")

    cur.execute('DROP TABLE IF EXISTS Directors')
    cur.execute("CREATE TABLE Directors(did INT, fname TEXT, lname TEXT, PRIMARY KEY(did))")

    cur.execute('DROP TABLE IF EXISTS Cast')
    cur.execute("CREATE TABLE Cast(aid INT, mid INT, role TEXT)")

    cur.execute('DROP TABLE IF EXISTS Movie_Director')
    cur.execute("CREATE TABLE Movie_Director(did INT, mid INT)")
	# DO NOT MODIFY - END

	########################################################################		
	### READ DATA FROM FILES ###############################################
	########################################################################		
	# actors.csv, cast.csv, directors.csv, movie_dir.csv, movies.csv
	# UPDATE THIS
    
    #initialize arrays to store contents from file
    actors = []
    movies = []
    directors = []
    cast = []
    movie_dirs = []
    
    #read each of the files and store each line from the files 
    with open('actors.csv') as actor_file:
        reader = csv.reader(actor_file)
        for line in reader:
            actors.append(line)
    
    with open('movies.csv') as movie_file:
        reader = csv.reader(movie_file)
        for line in reader:
            movies.append(line)        
            
    with open('directors.csv') as dir_file:
        reader = csv.reader(dir_file)
        for line in reader:
            directors.append(line)
    
    with open('cast.csv') as cast_file:
        reader = csv.reader(cast_file)
        for line in reader:
            cast.append(line)
            
    with open('movie_dir.csv') as movie_dir_file:
        reader = csv.reader(movie_dir_file)
        for line in reader:
            movie_dirs.append(line)
 

	########################################################################		
	### INSERT DATA INTO DATABASE ##########################################
	########################################################################		
	# UPDATE THIS TO WORK WITH DATA READ IN FROM CSV FILES
    
    for actor in actors: 
        cur.execute("INSERT INTO Actors VALUES(" + actor[0].replace("'", "''") + ", '" + actor[1].replace("'", "''") + "', '" + actor[2].replace("'", "''") + "', '" + actor[3].replace("'", "''") + "')")
      
    for movie in movies:
        cur.execute("INSERT INTO Movies VALUES(" + movie[0].replace("'", "''") + ", '" + movie[1].replace("'", "''") + "', '" + movie[2].replace("'", "''") + "', '" + movie[3].replace("'", "''") + "')")
    
    for director in directors:
        cur.execute("INSERT INTO Directors VALUES(" + director[0].replace("'", "''") + ", '" + director[1].replace("'", "''") + "', '" + director[2].replace("'", "''")+ "')")
   
    for mem in cast:
        cur.execute("INSERT INTO Cast VALUES(" + mem[0].replace("'", "''") + ", '" + mem[1].replace("'", "''") + "', '" + mem[2].replace("'", "''") + "')")
   
    for movie_dir in movie_dirs:
        cur.execute("INSERT INTO Movie_Director VALUES(" + movie_dir[0].replace("'", "''") + ", '" + movie_dir[1].replace("'", "''")+ "')")

    con.commit()  	
    
    
	########################################################################		
	### QUERY SECTION ######################################################
	########################################################################		
    queries = {}

	# DO NOT MODIFY - START 	
	# DEBUG: all_movies ########################
    queries['all_movies'] = '''
SELECT * FROM Movies
'''	
	# DEBUG: all_actors ########################
    queries['all_actors'] = '''
SELECT * FROM Actors
'''	
	# DEBUG: all_cast ########################
    queries['all_cast'] = '''
SELECT * FROM Cast
'''	
	# DEBUG: all_directors ########################
    queries['all_directors'] = '''
SELECT * FROM Directors
'''	
	# DEBUG: all_movie_dir ########################
    queries['all_movie_dir'] = '''
SELECT * FROM Movie_Director
'''	
	# DO NOT MODIFY - END

	########################################################################		
	### INSERT YOUR QUERIES HERE ###########################################
	########################################################################		
	# NOTE: You are allowed to also include other queries here (e.g., 
	# for creating views), that will be executed in alphabetical order.
	# We will grade your program based on the output files q01.csv, 
	# q02.csv, ..., q12.csv

	# Q01 ########################		
    queries['q01'] = '''
    SELECT DISTINCT fname, lname
    FROM Actors AS a, Cast AS c
    WHERE a.aid = c.aid
    AND c.aid IN (SELECT c.aid
                  FROM Cast AS c, Movies AS m
                  WHERE m.mid = c.mid AND m.year > 1989 AND m.year < 2000)
    AND c.aid IN (SELECT c.aid
                  FROM Cast AS c, Movies AS m
                  WHERE m.mid = c.mid AND m.year > 2009)
    ORDER BY lname, fname
'''	
	
	# Q02 ########################		
    queries['q02'] = '''
    SELECT title, year
    FROM Movies 
    WHERE year IN(SELECT m.year
                FROM Movies AS m
                WHERE m.title = "Star Wars VII: The Force Awakens")
    AND rank > (SELECT rank
                FROM Movies 
                WHERE title = "Star Wars VII: The Force Awakens")
    ORDER BY title
'''	

	# Q03 ########################		
    queries['q03'] = '''
    SELECT DISTINCT a.fname, a.lname 
    FROM Actors AS a, Cast AS c, Movies AS m
    WHERE c.aid = a.aid
    AND m.mid = c.mid
    AND m.title IN (SELECT m1.title
                    FROM Movies AS m1
                    WHERE m1.title LIKE '%Star Wars%')
    GROUP BY a.aid
    ORDER BY count(m.title) DESC
'''	

	# Q04 ########################		
    queries['q04'] = '''
    SELECT a.lname, a.fname
    FROM Actors AS a
    WHERE NOT a.aid IN(SELECT a1.aid
                       FROM Actors AS a1, Cast AS c, Movies AS m
                       WHERE a1.aid = c.aid AND m.year > 1986 AND m.mid = c.mid)
    ORDER BY a.lname, a.fname
'''	

	# Q05 ########################		
    queries['q05'] = '''
    SELECT d.fname, d.lname, count(DISTINCT dm.mid) AS film_count
    FROM Directors AS d, Movie_Director AS dm 
    WHERE d.did = dm.did
    GROUP BY d.did
    ORDER BY film_count DESC
    LIMIT 20
'''	

	# Q06 ########################	
    
    cur.execute("DROP VIEW IF EXISTS cast_counts")
    
    q06a = """
    CREATE VIEW cast_counts AS
        SELECT m1.title, COUNT(c1.aid) as size 
        FROM Movies AS m1, Cast AS c1 
        WHERE m1.mid = c1.mid
        GROUP BY m1.title
        ORDER BY size DESC
        LIMIT 20
    """
    cur.execute(q06a)
    
    queries['q06'] = '''
    SELECT m.title, COUNT(c.aid) AS cast_size
    FROM Movies m, Cast c
    WHERE m.mid = c.mid
    GROUP BY m.mid
    HAVING cast_size >= (SELECT MIN(cs.size) FROM cast_counts cs)
    ORDER BY cast_size DESC
'''	

	# Q07 ########################		
    cur.execute("DROP VIEW IF EXISTS fem_counts")
    cur.execute("DROP VIEW IF EXISTS male_counts")
    
    q07a = """
    CREATE VIEW fem_counts AS 
        SELECT DISTINCT m.title as title, SUM(CASE WHEN a.gender = "Female" THEN 1 ELSE 0 END) as num_f
        FROM Movies AS m, Actors AS a, Cast as c
        WHERE c.mid = m.mid AND a.aid = c.aid 
        GROUP BY m.title
    """
    q07b = """
    CREATE VIEW male_counts AS 
        SELECT DISTINCT m.title as title, SUM(CASE WHEN a.gender = "Male" THEN 1 ELSE 0 END) as num_m
        FROM Movies AS m, Actors AS a, Cast as c
        WHERE c.mid = m.mid AND a.aid = c.aid 
        GROUP BY m.title
    """
    
    cur.execute(q07a)
    cur.execute(q07b)
    
    queries['q07'] = '''
    SELECT DISTINCT m.title, fm.num_f, ml.num_m 
    FROM Movies AS m, fem_counts as fm, male_counts as ml
    WHERE m.title = fm.title AND m.title = ml.title AND fm.num_f > ml.num_m
    ORDER BY m.title 
'''	

	# Q08 ########################		
    queries['q08'] = '''
    SELECT DISTINCT a.fname, a.lname, count(DISTINCT md.did) as dir_cnt
    FROM Actors AS a, Cast as c, Movie_Director as md, Directors as d
    WHERE c.aid = a.aid AND md.mid = c.mid AND d.did = md.did
    AND a.fname NOT IN(SELECT d1.fname
                       FROM Directors as d1
                       WHERE d1.fname = d.fname)
    AND a.lname NOT IN(SELECT d2.lname
                       FROM Directors as d2
                       WHERE d2.lname = d.lname)
    GROUP by a.aid
    HAVING dir_cnt > 5
    ORDER BY dir_cnt DESC    
'''	

	# Q09 ########################		
    queries['q09'] = '''
    SELECT a.fname, a.lname, count(DISTINCT m.title) as title_cnt
    FROM Actors AS a, Cast as c, Movies as m
    WHERE c.aid = a.aid AND m.mid = c.mid AND a.fname LIKE 'S%' 
    AND m.mid IN (SELECT m1.mid 
                  FROM Movies as m1, Cast as c1, Actors as a1
                  WHERE c1.mid = m1.mid AND a1.aid = c1.aid 
                  AND m.year = (SELECT MIN(m2.year)
                                  FROM Movies as m2, Cast AS c2, Actors AS a2 
                                  WHERE c2.mid = m2.mid AND a2.aid = a.aid AND a2.aid = c2.aid
                                  ))
    GROUP BY a.aid
    ORDER BY title_cnt DESC
'''	

	# Q10 ########################		
    queries['q10'] = '''
    SELECT a.lname, m.title
    FROM Actors as a, Cast as c, Movies as m, Movie_Director as md, Directors as d
    WHERE c.aid = a.aid AND m.mid = c.mid AND md.mid = m.mid AND d.did = md.did
    AND a.lname = d.lname AND a.fname NOT IN (SELECT d1.fname
                                              FROM Directors as d1
                                              WHERE d1.fname = d.fname)
    ORDER BY a.lname
'''	

    cur.execute("DROP VIEW IF EXISTS Hanks_Films")
    cur.execute("DROP VIEW IF EXISTS Hanks_Costars")
    cur.execute("DROP VIEW IF EXISTS Costar_Films")
    
    q011a = """
    CREATE VIEW Hanks_Films AS 
        SELECT DISTINCT m.mid as mid
        FROM Movies as m, Actors as a, Cast as c
        WHERE c.aid = a.aid AND m.mid = c.mid
        AND a.lname IN(SELECT a1.lname
                       FROM Actors as a1
                       WHERE a1.lname = "Hanks")
        AND a.fname IN(SELECT a2.fname
                       FROM Actors as a2
                       WHERE a2.fname = "Tom") 
        GROUP BY m.mid
    """
    q011b = """
    CREATE VIEW Hanks_Costars AS 
        SELECT DISTINCT a.aid as aid
        FROM Actors as a, Hanks_Films as hf, Cast as c
        WHERE c.aid = a.aid AND c.mid = hf.mid
        AND a.aid NOT IN (SELECT a2.aid
                          FROM Actors as a2
                          WHERE a2.lname = "Hanks" 
                          AND a2.fname = "Tom")
        GROUP BY a.aid
    """   
    
    q011c = """
    CREATE VIEW Costar_Films AS 
        SELECT DISTINCT m.mid as mid, m.title as title
        FROM Actors as a, Cast as c, Movies as m
        WHERE c.mid = m.mid AND c.aid = a.aid
        AND m.mid NOT IN(SELECT hf1.mid
                         FROM Hanks_Films as hf1)
        AND a.aid IN(SELECT hc1.aid
                     FROM Hanks_Costars as hc1)
        GROUP BY m.mid
    """ 
    
    cur.execute(q011a) 
    cur.execute(q011b)
    cur.execute(q011c)
    
	# Q11 ########################		
    queries['q11'] = ''' 
    SELECT DISTINCT a.fname, a.lname
    FROM Actors as a, Costar_Films as cf, Cast as c
    WHERE c.aid = a.aid AND c.mid = cf.mid
    AND a.aid NOT IN(SELECT hc1.aid
                     FROM Hanks_Costars as hc1)
    ORDER BY a.fname, a.lname
'''	

	# Q12 ########################		
    queries['q12'] = '''
    SELECT a.fname, a.lname, count(m.title), avg(m.rank) as avg_rank
    FROM Actors as a, Cast as c, Movies as m
    WHERE a.aid = c.aid AND m.mid = c.mid
    GROUP BY a.aid
    ORDER BY avg_rank DESC
    LIMIT 20
'''	


	########################################################################		
	### SAVE RESULTS TO FILES ##############################################
	########################################################################		
	# DO NOT MODIFY - START 	
    for (qkey, qstring) in sorted(queries.items()):
        try:
            cur.execute(qstring)
            all_rows = cur.fetchall()
			
            print ("=========== ",qkey," QUERY ======================")
            print (qstring)
            print ("----------- ",qkey," RESULTS --------------------")
            for row in all_rows:
                print (row)
            print (" ")

            save_to_file = (re.search(r'q0\d', qkey) or re.search(r'q1[012]', qkey))
            if (save_to_file):
                with open(qkey+'.csv', 'w') as f:
                    writer = csv.writer(f)
                    writer.writerows(all_rows)
                    f.close()
                print ("----------- ",qkey+".csv"," *SAVED* ----------------\n")
		
        except lite.Error as e:
            print ("An error occurred:", e.args[0])
	# DO NOT MODIFY - END
	
