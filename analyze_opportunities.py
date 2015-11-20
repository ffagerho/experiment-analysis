import sys, re
import pandas as pd

def calculate_ratios(df):
    """
    Calculate opportunity ratio per user
    """

    opportunity_ratios = {}

    print "Analyzing target_emails"

    for target_email in df.target_email.unique():
        sys.stdout.write('.')
        sys.stdout.flush()

        reports_sent = df[(df.target_email == target_email) & (df.event == "EMAIL_SENT") & (df.event_target == "REPORT")]
        reports_opened = df[(df.target_email == target_email) & (df.event == "LOGIN") & (df.event_target == "REPORT") & (df.event_target_id.isin(reports_sent.event_target_id))].event_target_id.unique()
        
        num_reports_sent = len(reports_sent)
        num_reports_opened = len(reports_opened)
        
        if num_reports_sent == 0:
            this_or = 0
        else:
            this_or = float(num_reports_opened) / float(num_reports_sent)
        
        opportunity_ratios[target_email] = {
            'ao': num_reports_sent,
            'uo': num_reports_opened,
            'or': this_or
        }
    print

    ordata = pd.DataFrame.from_dict(opportunity_ratios, orient="index")

    # Calculate overall opportunity ratio

    print "Unique users considered for opportunity ratio: {}".format(len(ordata))
    print "Mean opportunity ratio: {} %".format(round(ordata['or'].mean() * 100, 4))
    print "Median opportunity ratio: {} %".format(ordata['or'].median())
    print "Minimum opportunity ratio: {} %".format(ordata['or'].min() * 100, 4)
    print "Maximum opportunity ratio: {} %".format(ordata['or'].max() * 100, 4)
    print "Opportunity ratio standard deviation: {}".format(round(ordata['or'].std(), 5))

    return ordata
