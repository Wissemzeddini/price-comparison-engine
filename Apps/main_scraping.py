from Apps.spacenet import *
from Apps.mytek import *
from Apps.tunisianet import *
from Apps.wiki import *
from Apps.sbsinfo import *
from Apps.itechstore import *
from Apps.alarabia import *
from Apps.bestbuy import * 
from Apps.zoom import *
# from scoop import *

def scraping_main_process():
    print('start scraping from tunisianet..'), tunisianet(), print('tunisianet scraping ends')
    print('start scraping from wiki...'), wiki(), print('wiki scraping ends')
    print('start scraping from sbs informatique..'), sbs_info(), print('sbs informatique scraping ends')
    print('start scraping from itech store...'), itech_store(), print('itech store scraping ends')
    print('start scraping from mytek...'), mytek(), print('mytek scraping ends')
    print('start scraping from zoom...'), zoom(), print('zoom scraping ends')
    print('start scraping from bestbuy...'), bestbuy(), print('bestbuy scraping ends')
    print('start scraping from Alarabia...'), alarabia(), print('Alarabia scraping ends')
    print('start scraping from space net...'), spacenet(), print('space net scraping ends')
    print('the scraping process is ended')