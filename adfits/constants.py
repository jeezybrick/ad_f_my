from settings import DEBUG

if DEBUG:
	AD_URL = "http://localhost:8888/"
else:
	AD_URL = "http://23.239.11.140:8050/"

#provides size of the thumbnails
THUMBNAIL_SIZE = (128, 100)

#provides size for the campaign images
IMG_SIZE = (368, 193)

#provides size for the publisher and sponsor logo
LOGO_SIZE = (35, 35)

#gives the size to the logo for making it a circle
LOGO_BOX = (300, 300)


AD_EMBED_SCRIPT = ''' 
<div id="ad-adfits">
<script>adwidget="%s"</script>
<script data-main="%sstatic/js/ads.js" src="%sstatic/js/require.js"></script>
</div>
'''

COUPON_SUBJECT = "Your Daily Reminder to Earn Rewards"
CAMPAIGN_SUBJECT = "New Rewards Now Available"

USER_PUBLISHER = "publisher"
USER_SPONSOR = "sponsor"