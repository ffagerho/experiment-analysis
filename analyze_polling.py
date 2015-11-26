from pandas import DataFrame
import matplotlib.pyplot as plt
import matplotlib
matplotlib.style.use('ggplot')


def calc_times(df): # here df as returned by data_helper.import_and_clean_data function
    timearray = []
    for x in df[df.event=="POLL"].target_email.unique():
        polhaps = df[(df.event=="POLL") & (df.target_email==x)].more_info # poll 
        prevurl = ''
        for y in polhaps:
            ysplit = y.split(' ')
            if not(prevurl.startswith(ysplit[2])): # a new article, thus a new session
                prevurl = ysplit[2]
                timearray.append({'email': x, 'sessiontime': int(ysplit[0][:-1])})
    return DataFrame(timearray)

def userbased_values(df): # here df as returned by calc_times function
    for x in df.email.unique():
        temporary = df[df.email==x]
        print 'For user {} time (s) spent on articles is as follows.'.format(x)
        print 'Mean: '+repr(round(temporary.sessiontime.mean(),2))
        print 'Median: '+repr(temporary.sessiontime.median())
        print 'Minimum: '+repr(float(temporary.sessiontime.min()))
        print 'Maximum: '+repr(float(temporary.sessiontime.max()))
        print

def largescale_values(df): # here df as returned by calc_times function
    print 'For all users, time (s) spent on articles is as follows.'
    print 'Mean: '+repr(round(df.sessiontime.mean(),2))
    print 'Median: '+repr(df.sessiontime.median())
    print 'Minimum: '+repr(float(df.sessiontime.min()))
    print 'Maximum: '+repr(float(df.sessiontime.max()))
    print 

def show_histogram(df): # here df as returned by calc_times function
    df=group_sessiontimes(df)
    df.sessiontime.value_counts().sort_index().plot(kind='bar')
    ticklabels=['30 s', '65 s', '105 s', '150 s', '200 s','255 s', '315 s', '380 s','450 s', '525 s', '10-15 m', '15-30 m','30-60 m','1-24 h','24+ h']    
    plt.title('Histogram of polling times')
    plt.xticks(range(len(ticklabels)),ticklabels,rotation=45);
    plt.xlabel('Time')
    plt.ylabel('Occurances')
    plt.show()


def group_sessiontimes(df): # here df as returned by calc_times function
    timebins = [600,900,1800,3600,86400,df.sessiontime.max()+1]
    for i in range(0,len(timebins)-1):
        df['sessiontime'].loc[(df['sessiontime']>=timebins[i]) & (df['sessiontime']<timebins[i+1])]=timebins[i]
    return df