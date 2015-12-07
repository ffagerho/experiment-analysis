from pandas import DataFrame

def click_percentages(df): # show-in-service & URL mail clicks
    mail_events = df[(df.event=='LOGIN') & (df.event_target=='REPORT')]
    clickcount = float(mail_events.shape[0])
    print 'Total amount of email clicks: '+repr(clickcount)
    print 'Amount of individual users : '+repr(mail_events.target_email.unique().shape[0])
    print 'Percentage of SHOW-IN-SERVICE clicks: '+repr(round(mail_events[mail_events.more_info=='SHOW-IN-SERVICE'].shape[0]/clickcount,3))
    print 'Percentage of URL clicks: '+repr(round(mail_events[mail_events.more_info!='SHOW-IN-SERVICE'].shape[0]/clickcount,3))
    print


def count_reportbased_clicks(df):
    reportstuff = []
    for x in df[df.event=='EMAIL_SENT'].event_target_id.unique():
        linecount = float(df[(df.event=='EMAIL_SENT') & (df.event_target_id==x)].report_line_count.all())
        prc = df[(df.event=='LOGIN') & (df.event_target_id==x) & df.more_info.str.startswith('http')].shape[0]/linecount
        reportstuff.append({'report': x, 'percentage': prc})
    resultdata = DataFrame(reportstuff)
    print 'Percentage of clicked articles, averaged over all reports: '+repr(round(resultdata.percentage.mean(),3))
    print
    #return resultdata


def count_userbased_clicks(df):
    reportstuff = []
    for x in df[df.event=='EMAIL_SENT'].target_email.unique():
        user_reports = df[(df.event=='EMAIL_SENT') & (df.target_email==x)].report_line_count.astype(int).sum()
        user_clicks = len(df[(df.event=='LOGIN') & (df.target_email==x) & df.more_info.str.startswith('http')])
        prc = float(user_clicks)/user_reports
        reportstuff.append({'user': x, 'percentage': prc})
    resultdata = DataFrame(reportstuff)
    print 'Percentage of clicked articles, averaged over all users: '+repr(round(resultdata.percentage.mean(),3))
    print
    #return resultdata

