import emoji

import reddit
from sentry_sdk import capture_message
import praw
import datetime
import reddit


def tabulate_votes(submission, thread_id):
    aye = 0
    nay = 0
    abst = 0
    alerts = 0
    print(datetime.datetime.utcnow().isoformat() + " Plugins::Secure // [INFO] Securing Thread " + thread_id + ".")
    capture_message(datetime.datetime.utcnow().isoformat() + " Plugins::Secure // [INFO] Securing Thread " + thread_id + ".")
    submission.comments.replace_more(limit=None)
    all_comments = submission.comments.list()
    comm_count = len(all_comments)
    for i in all_comments:
        if reddit.parse_vote(i.body, i.author.name) == 1:
            aye = aye + 1
        elif reddit.parse_vote(i.body, i.author.name) == 0:
            nay = nay + 1
        elif reddit.parse_vote(i.body, i.author.name) == 2:
            abst = abst + 1
        elif reddit.parse_vote(i.body, i.author.name) == 10:
            print(" Plugins::Secure // [INFO] I see myself!")
        else:
            print(datetime.datetime.utcnow().isoformat() + " Plugins::Secure // [WARN] Parser Mismatch (" + i.id + ").")
            capture_message(datetime.datetime.utcnow().isoformat() + " Plugins::Secure // [WARN] Parser Mismatch (" + i.id + ").")
            alerts = alerts + 1
    count = [aye], [nay], [abst], [alerts]
    return count


def secure_thread(submission, count):
    aye = count[0]
    nay = count[1]
    abst = count[2]
    alerts = count[3]
    if alerts == 0:
        submission.reply("THREAD IS SECURED! \n\n \n\n Ayes: " + str(aye) + " \n\n Nays: " + str(nay) + " \n\n Abstain: " + str(abst))
    if alerts != 0:
        submission.reply(emoji.emojize(":biohazard:") + " I HAVE ALERTS! CHECK SENTRY! " + emoji.emojize(":biohazard:") + " \n\n \n\n \n\n \n\n THREAD IS SECURED WITH " + emoji.emojize(":biohazard:") + " " + str(alerts) + " ALERTS! \n\n \n\n Ayes: " + str(aye) + " \n\n Nays: " + str(nay) + " \n\n Abstain: " + str(abst))
    submission.mod.lock()