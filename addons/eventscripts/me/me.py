import es, usermsg, psyco
from playerlib import getPlayer, getPlayerList
psyco.full()

sglobal = False

def load():
    es.addons.registerSayFilter(sayFilter)

def unload():
    es.addons.unregisterSayFilter(sayFilter)

def sayFilter(userid, text, teamonly):
    if userid == int(-1):
        return (userid, text, teamonly)
    player = getPlayer(userid)
    name = player.name
    team = player.team
    if team == 0:
        teamname = '#un'
    elif team == 1:
        teamname = '#spec'
    elif team == 2:
        teamname = '#t'
    elif team == 3:
        teamname = '#ct'
    index = player.index
    isdead = player.isdead
    striptext = text.strip('"')
    newtext = None
    if striptext.lower().startswith('/me'):
        striptext = striptext.lstrip('/me ')
        if teamonly:
            if isdead:
                if team == 1:
                    newtext = '\x01(Spectator)\x03 %s %s' %(name, striptext)
                elif team == 2:
                    newtext = '\x01*DEAD*(Terrorist)\x03 %s %s' %(name, striptext)
                elif team == 3:
                    newtext = '\x01*DEAD*(Counter-Terrorist)\x03 %s %s' %(name, striptext)
            else:
                if team == 1:
                    newtext = '\x01(Spectator)\x03 %s %s' %(name, striptext)
                elif team == 2:
                    newtext = '\x01(Terrorist)\x03 %s %s' %(name, striptext)
                elif team == 3:
                    newtext = '\x01(Counter-Terrorist)\x03 %s %s' %(name, striptext)
        else:
            if isdead:
                if team == 1:
                    newtext = '\x01*SPEC*\x03 %s %s' %(name, striptext)
                elif team == 2:
                    newtext = '\x01*DEAD*\x03 %s %s' %(name, striptext)
                elif team == 3:
                    newtext = '\x01*DEAD*\x03 %s %s' %(name, striptext)
            else:
                if team == 1:
                    newtext = '\x03%s %s' %(name, striptext)
                elif team == 2:
                    newtext = '\x03%s %s' %(name, striptext)
                elif team == 3:
                    newtext = '\x03%s %s' %(name, striptext)
    if newtext:
        if not sglobal:
            if teamonly == 1 and player.isdead == 1:
                for k in getPlayerList(teamname + ',' + '#dead'):
                    if getPlayer(k).isdead:
                        usermsg.saytext2(k, index, newtext)
            elif teamonly == 1 and player.isdead == 0:
                for k in getPlayerList(teamname):
                    usermsg.saytext2(k, index, newtext)
            elif teamonly == 0 and player.isdead == 1:
                for k in getPlayerList('#dead'):
                    usermsg.saytext2(k, index, newtext)
            elif teamonly == 0 and player.isdead == 0:
                for k in getPlayerList('#human'):
                    usermsg.saytext2(k, index, newtext)
        else:
            for k in getPlayerList():
                usermsg.saytext2(k, index, newtext)
        return (0, None, None)
    else:
        return (userid, text, teamonly)
