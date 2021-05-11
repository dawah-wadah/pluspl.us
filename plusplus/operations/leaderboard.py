from ..models import Thing
import json


def generate_leaderboard(team=None, losers=False):
    if losers:
        ordering = Thing.total_points.asc()
        header = "Here's the current loserboard:"
    else:
        ordering = Thing.total_points.desc()
        header = "Here's the current leaderboard:"

    # filter args
    user_args = {"user": True, "team": team}
    thing_args = {"user": False, "team": team}

    users = Thing.query.filter_by(**user_args).order_by(ordering).limit(10)
    things = Thing.query.filter_by(**thing_args).order_by(ordering).limit(10)

    formatted_things = [f"{thing.item} ({thing.total_points})" for thing in things]
    numbered_things = generate_numbered_list(formatted_things)

    formatted_users = [f"<@{user.item.upper()}> ({user.total_points})" for user in users]
    numbered_users = generate_numbered_list(formatted_users)

    leaderboard_header = {"type": "section",
                          "text":
                              {
                                  "type": "mrkdwn",
                                  "text": header
                              }
                          }
    body = {
        "type": "section",
                "fields": [
                    {
                        "type": "mrkdwn",
                        "text": "*Things*\n" + numbered_things
                    },
                    {
                        "type": "mrkdwn",
                        "text": "*Users*\n" + numbered_users
                    }
                ]
    }

    leaderboard = [leaderboard_header, body]
    return json.dumps(leaderboard)


def generate_numbered_list(items):
    out = ""
    for i, item in enumerate(items, 1):
        out += f"{i}. {item}\n"
    if len(out) == 0:
        out = "Welp, nothing's here yet."
    return out
