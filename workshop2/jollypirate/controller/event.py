# -*- coding: utf-8 -*-

#   Copyright(c) 2017 Jonas Sjöberg
#   Personal site:   http://www.jonasjberg.com
#   GitHub:          https://github.com/jonasjberg
#   University mail: js224eh[a]student.lnu.se


class Events(object):
    APP_QUIT         = 0x0001
    BOAT_DELETE      = 0x0002
    BOAT_REGISTER    = 0x0004
    BOAT_UPDATE      = 0x0008
    MEMBER_DELETE    = 0x0010
    MEMBER_INFOQUERY = 0x0020
    MEMBER_REGISTER  = 0x0040
    MEMBER_UPDATE    = 0x0080
    MEMBERS_LIST     = 0x0100
