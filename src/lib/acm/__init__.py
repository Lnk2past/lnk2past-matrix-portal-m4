def clear_portal(matrixportal):
    while matrixportal.graphics._bg_group:
        matrixportal.graphics._bg_group.pop()
    matrixportal.remove_all_text()


from acm.conway import GameOfLife
from acm.matrix import CodeRain
from acm.rutgers import RUC
# You need to have the local server running!
from acm.weather import Weather 

MODE_FUNCS = {
    'conway': GameOfLife,
    'matrix': CodeRain,
    'rutgers': RUC,
    'weather': Weather
}

MODES = list(MODE_FUNCS.keys())
