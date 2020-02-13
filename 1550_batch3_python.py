# import pandas, numpy
# Create the required data frames by reading in the files
import numpy as np

import pandas as pd

from datetime import datetime

df = pd.read_excel('SaleData.xlsx')


# Q1 Find least sales amount for each item
# has been solved as an example
def least_sales(df):
    # write code to return pandas dataframe
	ls = df.groupby(["Item"])["Sale_amt"].min().reset_index()
    return ls

# Q2 compute total sales at each year X region
def sales_year_region(df):
    # write code to return pandas dataframe
	df['Year'] =  df['OrderDate'].apply(lambda d: d.year)
	return pd.DataFrame(df.groupby(['Year','Region'])['Sale_amt'].sum())

# Q3 append column with no of days difference from present date to each order date
def days_diff(df):
    # write code to return pandas dataframe
	import datetime
	df['OrderDate'] = pd.to_datetime(df['OrderDate']).dt.date
	df['daysdiff'] = list(map(lambda x: datetime.date.today() - x, df['OrderDate']))
	return df


# Q4 get dataframe with manager as first column and  salesman under them as lists in rows in second column.
def mgr_slsmn(df):
    # write code to return pandas dataframe
	uniMan = df['Manager'].unique()
	x= list(map(lambda manager:(df[df['Manager']==manager]['SalesMan'].unique()),uniMan))
	return pd.DataFrame({'Manager': uniMan, 'SalesMan': x})

# Q5 For all regions find number of salesman and number of units
def slsmn_units(df):
    # write code to return pandas dataframe
	return pd.merge(df.groupby('Region')['SalesMan'].nunique(),df.groupby('Region')['Units'].sum(),on='Region')


# Q6 Find total sales as percentage for each manager
def sales_pct(df):
    # write code to return pandas dataframe
	q10 = pd.DataFrame(100*(df.groupby('Manager')['Sale_amt'].sum()/df['Sale_amt'].sum()))
    return q10

############################################################################################################################################

imdb = pd.read_csv('data/imdb.csv', escapechar='\\')

# Q7 get imdb rating for fifth movie of dataframe
def fifth_movie(imdb):
	# write code here
	return imdb['imdbRating'][4]
	

# Q8 return titles of movies with shortest and longest run time
def movies(imdb):
	# write code here
	return imdb[(imdb['duration'] == imdb['duration'].max()) | (imdb['duration'] == imdb['duration'].min())]
	

# Q9 sort by two columns - release_date (earliest) and Imdb rating(highest to lowest)
def sort_df(imdb):
	# write code here
	return (imdb.sort_values(['imdbRating','year'],ascending = False)).head()

# Q10 subset revenue more than 2 million and spent less than 1 million & duration between 30 mintues to 180 minutes
def subset_df(imdb):
	# write code here
	q10 = pd.read_csv('movie_metadata.csv')
	q10 = q10[(q10.gross>2000000) & (q10.budget<1000000) & (q10.duration > 30) & (q10.duration < 180)]
	return q10


############################################################################################################################################

dia = pd.read_csv('diamonds.csv',error_bad_lines = False)

# Q11 count the duplicate rows of diamonds DataFrame.
def dupl_rows(dia):
	# write code here
	return (dia[dia.duplicated()]).shape[0]

# Q12 droping those rows where any value in a row is missing in carat and cut columns
def drop_row(dia):
	# write code here
	dia['carat'] = pd.to_numeric(dia['carat'],errors = 'coerce')
	dia['z'] = pd.to_numeric(dia['z'],errors = 'coerce')
	dia.dropna()
	return dia
	

# Q13 subset only numeric columns
def sub_numeric(dia):
	# write code here
	(dia.select_dtypes(include=['float','int'])).head()
	return dia

# Q14 compute volume as (x*y*z) when depth > 60 else 8
def volume(dia):
	# write code here
	dia['vol'] = dia.x * dia.y * dia.z
	dia.loc[dia.depth < 60,'vol']=8
	return dia

# Q15 impute missing price values with mean
def impute(dia):
	# write code here
	return dia.fillna(value=dia.mean())
	
	
#BONUS QUESTIONS ############################################################################################################
	
# Q16 Generate a report that tracks the various Genere combinations for each type year on year.
#     The result data frame should contain type, Genere_combo, year, avg_rating, min_rating, max_rating, total_run_time_mins

movies = pd.read_csv('data/movie_metadata.csv')
imdb = pd.read_csv('data/imdb.csv', escapechar='\\')

def Gen_combo(movies):
	return movies.groupby(['genres','title_year'])['imdb_score','duration'].agg(['min','max','mean','sum']).head()


# Q17 Is there a realation between the length of a movie title and the ratings ? Generate a report that captures the trend
# of the number of letters in movies titles over years. We expect a cross tab between the year of the video release and the 
# quantile that length fall under. The results should contain year, min_length, max_length, num_videos_less_than25Percentile, 
# num_videos_25_50Percentile , num_videos_50_75Percentile, num_videos_greaterthan75Precentile

def year_len(imdb):
	imdb['tit_len'] = imdb['title'].str.len()
	imdb['year'] = pd.to_numeric(imdb['year'], errors='coerce')
	df1 = imdb.groupby('year')['tit_len'].agg(['min','max','count'])
	imdb['length_quantile'] = pd.qcut(imdb['tit_len'],q=4,labels='0-25% 25-50% 50-75% 75-100%'.split())
	df2 = pd.crosstab(imdb['year'],imdb['length_quantile'])
	return pd.merge(df1,df2,on='year').head()


# Q18 In diamonds data set Using the volumne calculated above, create bins that have equal population within them. 
# 	 Generate a report that contains cross tab between bins and cut. Represent the number under each cell as a
# 	 percentage of total.

def vol_quan(dia):
	df = dia.copy()
	df['Volume_quantile'] = pd.qcut(df['vol'],q=4,labels='0-25% 25-50% 50-75% 75-100%'.split())
	return pd.crosstab(df['Volume_quantile'],df['cut'],normalize=True)*100


# Q19 Generate a report that tracks the Avg. imdb rating quarter on quarter, in the last 10 years, for movies
# that are top performing. You can take the top 10% grossing movies every quarter. Add the number of top performing 
# movies under each genere in the report as well.

def top_perform(movies):
	df = movies[movies.title_year > (movies.title_year.max()-10)].copy()
	df = df[df.gross > df.gross.quantile(0.90)]
	df1 = df.genres.str.split('|',expand=True).stack().str.get_dummies().sum(level=0)
	df=pd.concat([df,df1],axis=1)
	return pd.merge(df.groupby('title_year')['imdb_score'].mean(),df.groupby('title_year')['Action',
				   'Adventure', 'Animation', 'Biography', 'Comedy', 'Crime', 'Drama',
				   'Family', 'Fantasy', 'History', 'Horror', 'Music', 'Musical', 'Mystery',
				   'Romance', 'Sci-Fi', 'Sport', 'Thriller', 'War', 'Western'].agg('sum'),on='title_year')


# Q20 Bucket the movies into deciles using the duration. Generate the report that tracks various features 
# like nomiations, wins, count, top 3 geners in each decile.

def dur_dec(imdb):
	imdb['duration_dec'] = pd.qcut(imdb.duration,q=10,
								labels = '0-10 10-20 20-30 30-40 40-50 50-60 60-70 70-80 80-90 90-100'.split())
	df1 = imdb.groupby('duration_dec')['nrOfNominations','nrOfWins'].agg('sum')
	x = imdb.groupby('duration_dec')['Action', 'Adult', 'Adventure', 'Animation', 'Biography','Comedy',
								  'Crime', 'Documentary', 'Drama', 'Family', 'Fantasy','FilmNoir', 
								  'GameShow', 'History', 'Horror', 'Music', 'Musical','Mystery', 
								  'News', 'RealityTV', 'Romance', 'SciFi', 'Short', 'Sport',
								  'TalkShow', 'Thriller', 'War', 'Western'].agg('sum')
	xt = x.transpose()
	m=[]
	for j in xt.columns:
		top3 = sorted(xt[j],reverse=True)[:3]
		for i in xt.index:
			if xt[j][i] in top3:
				m.append(i)
				
	return pd.concat([df1,Top3],axis = 1)



