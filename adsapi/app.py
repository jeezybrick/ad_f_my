import datetime
import tornado.web
from bson import ObjectId
from tornado.escape import json_encode
import mandrill
import settings


class AdContentHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

    @tornado.web.asynchronous
    def get(self):
        """
        Would valid the query data using the mongo stored procedure then 
        """

        widget_token = self.get_argument('wid', '')
        user_token = self.get_argument('adftoken', '')
        reference_url = self.get_argument('ref_url', '')
        self.callback_function = self.get_argument('callback', '')
        #prepred the query expression for eval
        query_exp = 'get_widget_data("' + widget_token + '", "' + user_token + '", "' + reference_url + '")'
        self.settings['db'].eval(query_exp, callback=self._on_campaign_response)

    @tornado.web.asynchronous
    def _on_campaign_response(self, data, error):
        """
        Would return the campaign response.
        """ 
                
        day_class = ''

        if data and data.get('status', False):
            #setting the money box css name
            money_box_position =  '%s%s' % (
                'adf-mboxwrapper-day', int(data['day'])
            )

            #Depending on the message box class setting the 
            #day class for process bars in the widget
            if data['message_class'] == "main1":
                day_class = 'active'
            else:
                day_class = 'received'

            if data['day'] == 1 and data['is_available']:
                radio_pattern = {
                    'adf-day1': day_class,
                    'adf-day2': '',
                    'adf-day3': '',
                    'adf-day4': '',
                    'adf-day5': '',
                }
            elif int(data['day']) == 2 and data['is_available']:            
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': day_class,
                    'adf-day3': '',
                    'adf-day4': '',
                    'adf-day5': '',
                }

            elif data['day'] == 3 and data['is_available']:
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': 'received',
                    'adf-day3': day_class,
                    'adf-day4': '',
                    'adf-day5': '',
                }
            elif data['day'] == 4 and data['is_available']:
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': 'received',
                    'adf-day3': 'received',
                    'adf-day4': day_class,
                    'adf-day5': '',
                }
            elif data['day'] == 5 and data['is_available']:
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': 'received',
                    'adf-day3': 'received',
                    'adf-day4': 'received',
                    'adf-day5': 'active',
                }
            else:
                radio_pattern = {
                    'adf-day1': '',
                    'adf-day2': '',
                    'adf-day3': '',
                    'adf-day4': '',
                    'adf-day5': '',
                }

                money_box_position =  '%s%s' % (
                    'adf-mboxwrapper-day', 5
                )
                
            response = { 
                'sponsor_logo': settings.MEDIA_URL + data['sponsor_logo'],
                'publisher_logo': settings.MEDIA_URL + data['publisher_logo'],
                'campaign_img': settings.MEDIA_URL + data['campaign_image'],
                'adfits_logo': '',
                'coupons_left': data['coupons_available'],
                'adfdy': data['day'],
                'radio_pattern': radio_pattern,
                'money_box_position': money_box_position,
                'adftoken': data['user_token'],
                'money_box_color': data['money_box_color'],
                'message_class': data['message_class'],
                'dollars_rewarded': settings.PER_COUPON_DOLLAR * data['coupons_available'],
                'status': data['status'],
                'sponsor_name': data['sponsor_name'],
                'publisher_name': data['publisher_name'],
                'landing_url': data['landing_url']
            }

            self.write(json_encode(response))
        else:
            self.write(json_encode(''))
        self.finish()


class SaveUserTokenHandler(tornado.web.RequestHandler):

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

    @tornado.web.asynchronous
    def post(self):
        """
        Would insert user data for each campaign redeem
        """

        widget_token = self.get_argument('wid', '')
        user_token = self.get_argument('adftoken', '')
        reference_url = self.get_argument('ref_url', '')
        email = self.get_argument('email', '')
        fname = self.get_argument('fname', '')
        lname = self.get_argument('lname', '')
        location = self.get_argument('location', '')
        age = self.get_argument('age','')
        sex = self.get_argument('sex', '')
        notify_me = self.get_argument('notify_me', '')
        agreed = self.get_argument('agreed', '')
        query_exp = 'redeem_coupon("' + widget_token + '", "' + user_token + '", "' + reference_url + '", "' + email + '", "' + age + '", "' + sex + '", "' + location + '", "' + notify_me + '", "' + agreed + '", "' + fname + '", "' + lname +'")'
        self.settings['db'].eval(query_exp, callback=self._on_widget_response)

    def _on_widget_response(self, data, error):
        day_class = ''

        if data and data.get('status', False):
            #setting the money box css name
            money_box_position =  '%s%s' % (
                'adf-mboxwrapper-day', int(data['day'])
            )

            #Depending on the message box class setting the 
            #day class for process bars in the widget
            if data['message_class'] == "main1":
                day_class = 'active'
            else:
                day_class = 'received'

            if data['day'] == 1 and data['is_available']:
                radio_pattern = {
                    'adf-day1': day_class,
                    'adf-day2': '',
                    'adf-day3': '',
                    'adf-day4': '',
                    'adf-day5': '',
                }
            elif int(data['day']) == 2 and data['is_available']:
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': day_class,
                    'adf-day3': '',
                    'adf-day4': '',
                    'adf-day5': '',
                }
            elif data['day'] == 3 and data['is_available']:
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': 'received',
                    'adf-day3': day_class,
                    'adf-day4': '',
                    'adf-day5': '',
                }
            elif data['day'] == 4 and data['is_available']:
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': 'received',
                    'adf-day3': 'received',
                    'adf-day4': day_class,
                    'adf-day5': '',
                }
            elif (data['day'] == 5 and data['is_available'] 
                or data['day'] == 5 and data['is_redeemed']):
                radio_pattern = {
                    'adf-day1': 'received',
                    'adf-day2': 'received',
                    'adf-day3': 'received',
                    'adf-day4': 'received',
                    'adf-day5': 'active',
                }
            else:
                radio_pattern = {
                    'adf-day1': '',
                    'adf-day2': '',
                    'adf-day3': '',
                    'adf-day4': '',
                    'adf-day5': '',
                }

                money_box_position =  '%s%s' % (
                    'adf-mboxwrapper-day', 5
                )

            response = { 
                'status': data['status'],
                'sponsor_logo': settings.MEDIA_URL + data['sponsor_logo'],
                'publisher_logo': settings.MEDIA_URL + data['publisher_logo'],
                'campaign_img': settings.MEDIA_URL + data['campaign_image'],
                'adfits_logo': '',
                'coupons_left': data['coupons_available'],
                'adfdy': data['day'],
                'radio_pattern': radio_pattern,
                'money_box_position': money_box_position,
                'adftoken': data['user_token'],
                'money_box_color': data['money_box_color'],
                'message_class': data['message_class'],
                'dollars_rewarded': settings.PER_COUPON_DOLLAR * data['coupons_available']
            }

            if data['is_redeemed']:
                self.send_confirmation(
                    self.get_argument('email', ''), 
                    data['publisher_name'], 
                    data['sponsor_name']
                )

            self.write(json_encode(response))
        else:
            self.write(json_encode(""))

        self.finish()

    def send_confirmation(self, email, publisher_name, sponsor_name):

        message = {
            'auto_html': None,
            'auto_text': None,
            'from_email': 'notifications@adfits.com',
            'from_name': 'Jennifer Williams',
            'headers': {'Reply-To': 'notifications@adfits.com'},
            'html': settings.REDEEM_MESSAGE % (publisher_name, sponsor_name),
            'important': True,
            'subject': settings.REDEEM_SUBJECT,
            'tags': ['Redeemed-confirmation'],
            'text': settings.REDEEM_MESSAGE % (publisher_name, sponsor_name),
            'to': [{'email': email}],
            'track_clicks': True,
            'track_opens': True
        }

        try:
            mandrill_client = mandrill.Mandrill(settings.MANDRILL_API_KEY)
            sent_status = mandrill_client.messages.send(
                message=message, 
                async=True, 
                ip_pool='Main Pool'
            )
            return sent_status
        except:
            return {}


class SaveCouponDollarHandler(tornado.web.RequestHandler):
    """
    Would be used to save the coupon dollar for the user depending on the token.
    """

    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

    @tornado.web.asynchronous
    def post(self):
        """
        Would insert user data for each campaign redeem
        """

        widget_token = self.get_argument('wid', '')
        user_token = self.get_argument('adftoken', '')
        coupon_day = self.get_argument('adfday', '')
        reference_url = self.get_argument('ref_url', '')
        query_exp = 'save_user_coupon("' + widget_token + '", "' + user_token + '", "' + reference_url + '")'
        self.settings['db'].eval(query_exp, callback=self._on_widget_response)

    def _on_widget_response(self, data, error):
        
        if data:
           self.write(json_encode(data))
        else:
            self.write(json_encode(''))

        self.finish()
        

class SocialShareHandler(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")

    @tornado.web.asynchronous
    def post(self):
        """
        Would store the record for each social share.
        """

        widget_token = self.get_argument('wid', '')
        user_token = self.get_argument('adftoken', '')
        reference_url = self.get_argument('ref_url', '')
        social_type = self.get_argument('social_type', '')
        query_exp = 'social_save("' + widget_token + '", "' + user_token + '", "' + reference_url + '", ' + social_type + ')'
        self.settings['db'].eval(query_exp, callback=self._on_social_save)

    def _on_social_save(self, data, error):
        
        if data:
            self.write(json_encode(data))
        else:
            self.write(json_encode(""))

        self.finish()    


class NotifyHandler(tornado.web.RequestHandler):
    
    def set_default_headers(self):
        self.set_header("Access-Control-Allow-Origin", "*")

    def set_extra_headers(self, path):
        self.set_header("Cache-control", "no-cache")
    
    @tornado.web.asynchronous
    def post(self):
        widget_token = self.get_argument('wid', '')
        user_token = self.get_argument('adftoken', '')
        notify_type  = self.get_argument('notify_type', '')
        reference_url = self.get_argument('ref_url', '')
        email = self.get_argument('email', '')
        day = self.get_argument('adfdy', '')
        query_exp = 'save_notifications("' + widget_token + '", "' + user_token + '", "' + reference_url + '", "' + email + '", "' + notify_type + '", ' + day + ')'
        self.settings['db'].eval(query_exp, callback=self._on_notify_response)

    def _on_notify_response(self, data, error):

        if data:
            self.write(json_encode(data))
        else:
            self.write(json_encode(""))
        self.finish()
