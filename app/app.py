from siteFrame import SiteFrame
import atexit


site_frame = SiteFrame()

atexit.register(lambda: site_frame.exit())
