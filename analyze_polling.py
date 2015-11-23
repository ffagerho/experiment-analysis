from pandas import DataFrame

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