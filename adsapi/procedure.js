var conn = new Mongo();
db = conn.getDB("adfits");
db.auth("adf-ap-user", "ApP$AF*99*Al!2014#$");

db.system.js.save({
 	_id: "get_widget_data", 
 	value: function (widget_token, user_token, ref_url) {
 		var reference_url = ref_url + "/"

 		//Getting widet info and check if token already exists in user token collection.
		var widget_data = db.campaign_widget.findOne({'token': widget_token});

		if (widget_data) {
			var message_class;
			var is_available;
			var next_day;
			var campaign_data = db.campaign_campaign.findOne({
				'_id': widget_data['campaign_id']
			});

			var d = new Date();
			
			var campaign_end = campaign_data['end_date'];
			var campaign_start = campaign_data['start_date'];
			current_date = new Date(
				d.getFullYear(), 
				d.getMonth(), 
				d.getDate()
			);		

			if (campaign_data) {
				
				var campaign_start_day = new Date(
					campaign_start.getFullYear(), 
					campaign_start.getMonth(), 
					campaign_start.getDate()
				);
				var campaign_last_day = new Date(
					campaign_end.getFullYear(), 
					campaign_end.getMonth(), 
					campaign_end.getDate()
				);

				//validating whether the campaign has started or not or 
				//already end.
				if ((campaign_start_day.getTime() > current_date.getTime())
					|| current_date.getTime() > campaign_last_day.getTime()) {

					//campaign not yet publisher or over
					return {};
				}

				var website_data = db.publisher_website.findOne({
					'_id': campaign_data['website_id'],
					'website_domain': reference_url
				})
				
				if (website_data) {
					var user_data = db.client_usertoken.findOne({
						'token': user_token, 
						'widget_id': widget_data['_id'],
						'campaign_id': widget_data['campaign_id'],
						'website_id': website_data['_id'],
						'reference_url': reference_url
					});

					//Getting sponsor and publisher logo
					var sponsor_data = db.sponsor_sponsor.findOne(
						{'_id': campaign_data['sponsor_id']}, 
						{'logo': 1, 'name':1}
					)
					var publisher_data = db.publisher_publisher.findOne(
						{'_id': campaign_data['publisher_id']}, 
						{'logo': 1, 'name':1}
					)

					if (user_data) { 

						var campaign_viewed = user_data['last_viewed'];
						//setting the last viewed date
						var last_viewed = new Date(
							campaign_viewed.getFullYear(), 
							campaign_viewed.getMonth(), 
							campaign_viewed.getDate()
						);
						
						if (campaign_data['coupons_available'] == 0) {
							message_class = "main7"
							is_available = false
							next_day = user_data['dollar_saved']
						} else if (last_viewed.getTime() != current_date.getTime()
							&& user_data['dollar_saved'] == 5) {

							//if user already reedeemed the coupon, 
							//from next day onward show message 7 i.e campaign closed.
							message_class = "main7"
							is_available = false
							next_day = user_data['dollar_saved']
						} else if (last_viewed.getTime() != current_date.getTime() 
							&& user_data['dollar_saved'] < 5) {
							
							//if the user has not collect all the parts of coupon
							is_available = true
							next_day = user_data['dollar_saved'] + 1

							//setting the next day and updating the collection.
							db.client_usertoken.update(
								{ '_id': user_data['_id'] }, 
								{
									$set: { 'last_viewed': current_date }, 
									$inc: { 'day': 1 }
								}, false, false
							);

							if (parseInt(next_day) == 5) {
								message_class = "main5"
							} else {
								message_class = "main1"	
							}	
	  					} else if (last_viewed.getTime() == current_date.getTime() 
							|| user_data['dollar_saved'] == 5) {

							is_available = true
							next_day = user_data['dollar_saved']
								
							if (parseInt(user_data['dollar_saved']) == 5) {

								message_class = "main6"
							} else if (parseInt(user_data['dollar_saved']) == 4) {
								message_class = "main5"
							} else {
								message_class = "main4"
							}
						}
						
						response = {
							'status': true,
							'day': next_day,
							'user_token': user_data['token'],
							'campaign_image': campaign_data['image'],
							'coupon_left': campaign_data['coupons_available'],
							'sponsor_logo': sponsor_data['logo'],
							'sponsor_name': sponsor_data['name'],
							'publisher_logo': website_data['website_logo'],
							'publisher_name': publisher_data['name'],
							'money_box_color': campaign_data['color'],
							'message_class': message_class,
							'coupons_available': campaign_data['coupons_available'],
							'is_available': is_available,
							'landing_url': campaign_data['landing_url']
						}
					} else {
						//create new response
						var next_day;
						var message_class;
						var is_available;

						if (campaign_data['coupons_available'] == 0) {
							next_day = 6; //some greater value 
							is_available = false;
							message_class = 'main7';
						} else {
							next_day = 1;
							is_available = true;
							message_class = 'main1';
						}

						response = {
							'status': true,
							'day': next_day,
							'user_token': ObjectId().str,
							'campaign_image': campaign_data['image'],
							'coupon_left': campaign_data['coupons_available'],
							'sponsor_logo': sponsor_data['logo'],
							'sponsor_name': sponsor_data['name'],
							'publisher_logo': website_data['website_logo'],
							'publisher_name': publisher_data['name'],
							'money_box_color': campaign_data['color'],
							'message_class': message_class,
							'coupons_available': campaign_data['coupons_available'],
							'is_available': is_available,
							'landing_url': campaign_data['landing_url'] 
						}
					}

					//Make enter in the campaigntracker to track how many time an ad was viewed(vd).
					db.campaign_campaigntracker.insert({
						'widget_id': widget_data['_id'],
						'campaign_id': widget_data['campaign_id'],
						'day' : NumberInt(response['day']),
						'reference_token': user_token,
						'clicked_on' : new Date(),
						'action': 'vd',
						'publisher_id': publisher_data['_id'],
						'sponsor_id': sponsor_data['_id'],
						'website_id': website_data['_id'],
						'reference_url': reference_url
					});
				} else {
					response = {
						'status': false,
						'msg': "Website not allowed."
					};
				}
			} else {
				response = {
					'status': false,
					'msg': "Campaign not available."
				};
			}
		} else {
			response = {
				'status': false,
				'msg': "Widget not available."
			};
		}
	return response;
	}
});


db.system.js.save({
 	_id: "save_user_coupon", 
 	value: function (widget_token, user_token, ref_url) {
 		var response;
 		var reference_url = ref_url + "/";

 		//Getting the widget info and checking if token already exists.
 		var widget_data = db.campaign_widget.findOne({'token': widget_token});

 		//if token is already available, then check if campaign is available.
		var campaign_data = db.campaign_campaign.findOne({
			'_id': widget_data['campaign_id']
		});

		var website_data = db.publisher_website.findOne({
			'_id': campaign_data['website_id'],
			'website_domain': reference_url
		})

		if (website_data) {
			var user_data = db.client_usertoken.findOne({
				'token': user_token, 
				'widget_id': widget_data['_id'],
				'campaign_id': widget_data['campaign_id'],
				'website_id': website_data['_id']
			});
			
			var date = new Date();
			//setting the last current date
			current_date = new Date(
				date.getFullYear(), 
				date.getMonth(), 
				date.getDate()
			);

			if (user_data) {

				if(campaign_data) {
					var sponsor_data = db.sponsor_sponsor.findOne(
						{'_id': campaign_data['sponsor_id']}, 
						{'logo': 1}
					)
					var publisher_data = db.publisher_publisher.findOne(
						{'_id': campaign_data['publisher_id']}, 
						{'logo': 1}
					)

					var token_date = user_data['last_saved'];
					var campaign_date = campaign_data['end_date'];

					//setting the last viewed date
					var last_saved = new Date(
						token_date.getFullYear(), 
						token_date.getMonth(), 
						token_date.getDate()
					);

					var campaign_last_day = new Date(
						campaign_date.getFullYear(), 
						campaign_date.getMonth(), 
						campaign_date.getDate()
					);

					var day = user_data['dollar_saved'] + 1
					//putting entery for number times clicked(cd)
					db.campaign_campaigntracker.insert({
						'widget_id': widget_data['_id'],
						'campaign_id': widget_data['campaign_id'],
						'reference_url': ref_url,
						'day' : NumberInt(day),
						'reference_token': user_token,
						'clicked_on' : new Date(),
						'action': 'cd',
						'publisher_id': publisher_data['_id'],
						'sponsor_id': sponsor_data['_id'],
						'website_id': website_data['_id']
					})		

					//if campaign is over meaning the end date is less then the current date.
					if (current_date.getTime() > campaign_last_day.getTime()) {
						response = {
							'status' : false,
							'msg': 'Campaign not available.',
							'is_redeemed': '',
							'is_available': false
						}
					} else if (current_date.getTime() == last_saved.getTime()) {
						//if coupon already saved for the day
						response = {
							'status' : true,
							'msg': 'Coupon already saved for the day.',
							'is_redeemed': user_data['is_redeemed'],
							'is_available': user_data['is_available']
						}
					} else {
						//Update the user token collection and 
						//insert an entry in lient_savereward collection.
						var data_update;

						//if user trying to save the coupon on his 5 day
						// in the dollar saved counter and set is_redeemed 
						//as true and is_available as false.
						if (user_data['dollar_saved'] == 5) {
							db.client_usertoken.update({
								'_id': user_data['_id']
							}, {
								$set: {
									'last_saved': current_date,
									'is_redeemed': true,
									'is_available': false
								},
								$inc: {'dollar_saved': 1}
							}, false, false);

							response = {
								'status' : true,
								'msg': 'Coupon saved for the day.',
								'is_redeemed': true,
								'is_available': false
							}
						} else {					
							db.client_usertoken.update({
								'_id': user_data['_id']
							}, {
								$set: {'last_saved': current_date},
								$inc: {'dollar_saved': 1}
							}, false, false);

							response = {
								'status' : true,
								'msg': 'Coupon saved for the day.',
								'is_redeemed': user_data['is_redeemed'],
								'is_available': user_data['is_available']
							}
						}

						//insert an enter in client_savereward collection.
						db.client_savereward.insert({
							'usertoken_id': user_data['_id'],
							'coupon_part': user_data['dollar_saved'] + 1,
							'saved_on': date,		
							'widget_id': widget_data['_id'],
							'campaign_id': campaign_data['_id'],
							'publisher_id': publisher_data['_id'],
							'sponsor_id': sponsor_data['_id']
						});
					}
				} else {
					response = {
						'status' : false,
						'msg': 'Campaign not available.',
						'is_redeemed': '',
						'is_available': false
					}
				}
			} else {
				//if the token does not exists, then insert an enter in client_usertoken
				//and insert an enter in client_savereward collection.
				db.client_usertoken.insert({
					'widget_id': widget_data['_id'],
					'campaign_id': widget_data['campaign_id'],
					'token': user_token,
					'day': NumberInt(1),
					'dollar_saved': NumberInt(1),
					'created': current_date,
					'last_viewed': current_date,
					'last_saved': current_date,
					'is_redeemed': false,
					'is_available': true,
					'reference_url': reference_url,
					'website_id': website_data['_id']
				});

				var save_response = db.client_usertoken.findOne({
					'widget_id': widget_data['_id'],
					'campaign_id': widget_data['campaign_id'],
					'token': user_token
				}, {'_id': 1})

				var campaign_data = db.campaign_campaign.findOne({
					'_id': widget_data['campaign_id']
				});

				var sponsor_data = db.sponsor_sponsor.findOne(
					{'_id': campaign_data['sponsor_id']}, 
					{'logo': 1}
				)
				var publisher_data = db.publisher_publisher.findOne(
					{'_id': campaign_data['publisher_id']}, 
					{'logo': 1}
				)

				db.client_savereward.insert({
					'usertoken_id': save_response['_id'],
					'coupon_part': NumberInt(1),
					'saved_on': date,
					'widget_id': widget_data['_id'],
					'campaign_id': widget_data['campaign_id'],
					'publisher_id': publisher_data['_id'],
					'sponsor_id': sponsor_data['_id']
				})

				response = {
					'status' : true,
					'msg': 'Coupon saved for the day.',
					'is_redeemed': false,
					'is_available': true
				}

				//enter to track widget clicked(cd)
				db.campaign_campaigntracker.insert({
					'widget_id': widget_data['_id'],
					'campaign_id': widget_data['campaign_id'],
					'day' : NumberInt(1),
					'reference_token': user_token,
					'clicked_on' : new Date(),
					'action': 'cd',
					'publisher_id': publisher_data['_id'],
					'sponsor_id': sponsor_data['_id'],
					'reference_url': reference_url,
					'website_id': website_data['_id']
				});
			}
		} else {
			response = {
				'status': false,
				'msg': "Website not allowed."
			};
		}	
		return response;
	}
});


db.system.js.save({
 	_id: "redeem_coupon", 
 	value: function (widget_token, user_token, ref_url, email, age, sex, location, notify_me, agreed, fname, lname) {
 		//Getting the widget info and checking if token already exists.
 		var reference_url = ref_url + "/";
 		var widget_data = db.campaign_widget.findOne({'token': widget_token});
 		var campaign_data = db.campaign_campaign.findOne({
			'_id': widget_data['campaign_id']
		});
 		var website_data = db.publisher_website.findOne({
			'_id': campaign_data['website_id'],
			'website_domain': reference_url
		});

		if (website_data) {	
			var user_data = db.client_usertoken.findOne({
				'token': user_token, 
				'widget_id': widget_data['_id'],
				'campaign_id': widget_data['campaign_id'],
				'website_id': website_data['_id'],
				'reference_url': reference_url,
				'is_available': true,
				'is_redeemed': false
			});
			
			if (user_data) {
				var sponsor_data = db.sponsor_sponsor.findOne(
					{'_id': campaign_data['sponsor_id']}, 
					{'logo': 1, 'name': 1}
				);
				var publisher_data = db.publisher_publisher.findOne(
					{'_id': campaign_data['publisher_id']}, 
					{'logo': 1, 'name': 1}
				);

				var date = new Date();
				//setting the last current date
				current_date = new Date(
					date.getFullYear(), 
					date.getMonth(), 
					date.getDate()
				);

				var campaign_date = campaign_data['end_date'];
				var campaign_last_day = new Date(
					campaign_date.getFullYear(), 
					campaign_date.getMonth(), 
					campaign_date.getDate()
				);

				//if campaign is over meaning the end date is less then the current date.
				if (current_date.getTime() > campaign_last_day.getTime()) {
					response = {
						'status': true,
						'day': user_data['dollar_saved'] + 1,
						'user_token': user_data['token'],
						'campaign_image': campaign_data['image'],
						'coupon_left': campaign_data['coupons_available'],
						'sponsor_logo': sponsor_data['logo'],
						'sponsor_name': sponsor_data['name'],
						'publisher_logo': website_data['website_logo'],
						'publisher_name': publisher_data['name'],
						'money_box_color': campaign_data['color'],
						'message_class': "main7",
						'coupons_available': campaign_data['coupons_available'],
						'is_redeemed': '',
						'is_available': false
					};
				} else {
					db.client_usertoken.update({
						'_id': user_data['_id']
					}, {
						$set: {
							'last_saved': current_date,
							'is_redeemed': true,
							'is_available': false,
							"email": email,
                            "first_name": fname,
                            "last_name": lname,
							"location": location,
							"age": age,
							"sex": sex,
							"notify_me": notify_me,
							"agreed": agreed
						},
						$inc: {'dollar_saved': 1}
					}, false, false);

					db.client_savereward.insert({
						'usertoken_id': user_data['_id'],
						'widget_id': widget_data['_id'],
						'campaign_id': campaign_data['_id'],
						'publisher_id': publisher_data['_id'],
						'sponsor_id': sponsor_data['_id'],
						'coupon_part': user_data['dollar_saved'] + 1,
						'saved_on': date
					});

					db.client_redeemcoupon.insert({
						'usertoken_id': user_data['_id'],
						'widget_id': widget_data['_id'],
						'campaign_id': campaign_data['_id'],
						'publisher_id': publisher_data['_id'],
						'sponsor_id': sponsor_data['_id'],
						'redeem_on': date
					});

					db.campaign_campaign.update({
						'_id':  widget_data['campaign_id'] },
						{ $inc: {'coupons_available': -1} },
					 false, false);

					response = {
						'status': true,
						'day': user_data['dollar_saved'] + 1,
						'user_token': user_data['token'],
						'campaign_image': campaign_data['image'],
						'coupon_left': campaign_data['coupons_available'],
						'sponsor_logo': sponsor_data['logo'],
						'sponsor_name': sponsor_data['name'],
						'publisher_logo': website_data['website_logo'],
						'publisher_name': publisher_data['name'],
						'money_box_color': campaign_data['color'],
						'message_class': "main6",
						'coupons_available': campaign_data['coupons_available'],
						'is_redeemed': true,
						'is_available': false,
						'widget_id': widget_data['_id'],
						'campaign_id': campaign_data['_id'],
						'publisher_id': publisher_data['_id'],
						'sponsor_id': sponsor_data['_id'],
						'reference_url': reference_url,
						'website_id': website_data['_id']
					};
				}

				//enter to track widget clicked(cd)
				db.campaign_campaigntracker.insert({
					'widget_id': widget_data['_id'],
					'campaign_id': campaign_data['_id'],
					'publisher_id': publisher_data['_id'],
					'sponsor_id': sponsor_data['_id'],
					'reference_url': reference_url,
					'day': NumberInt(5),
					'reference_token': user_token,
					'clicked_on' : new Date(),
					'action': 'cd',
					'website_id': website_data['_id']
				});
			} else {
				//invalid user token for day5
				response = {
					'status': false,
					'msg': "Unable to redeem coupon."
				};
			}
		} else {
			//invalid user token for day5
			response = {
				'status': false,
				'msg': "Website not allowed."
			};
		}
		return response;
	}
});

db.system.js.save({
 	_id: "social_save", 
 	value: function(widget_token, user_token, ref_url, social_type) {
 		var reference_url = ref_url + "/";
 		var widget_data = db.campaign_widget.findOne({'token': widget_token});
 		var response = {
 			'status': false
 		};

 		if (widget_data) {
 			var campaign_data = db.campaign_campaign.findOne({
				'_id': widget_data['campaign_id']
			});

 			if (campaign_data) {
	 			var website_data = db.publisher_website.findOne({
					'_id': campaign_data['website_id'],
					'website_domain': reference_url
				});

		 		if (website_data) {
		 			var user_data = db.client_usertoken.findOne({
						'token': user_token, 
						'widget_id': widget_data['_id'],
						'campaign_id': widget_data['campaign_id'],
						'website_id': website_data['_id'],
						'reference_url': reference_url
					});

					if (user_data) {
						db.client_socialshare.insert({
							"usertoken_id": user_data['_id'],
							"widget_id": widget_data['_id'],
							"campaign_id": campaign_data['_id'],
							"publisher_id":  campaign_data['publisher_id'],
							"sponsor_id":  campaign_data['sponsor_id'],
							"social_type": social_type,
							"website_id": website_data['_id'],
							"reference_url": reference_url,
							"date_created": new Date()
						});

						response = {
				 			'status': true
				 		};
					}
		 		}
		 	}
 		}
 		return response;
 	}
});

db.system.js.save({
 	_id: "save_notifications", 
 	value: function (widget_token, user_token, ref_url, email, notify_type, day) { 
 		var reference_url = ref_url + "/";
 		var response;
 		var widget_data = db.campaign_widget.findOne({'token': widget_token});

 		if (widget_data) {
 			var campaign_data = db.campaign_campaign.findOne({
				'_id': widget_data['campaign_id']
			});

 			if (campaign_data) {
	 			var website_data = db.publisher_website.findOne({
					'_id': campaign_data['website_id'],
					'website_domain': reference_url
				});

	 			if(website_data) {
					var user_data = db.client_usertoken.findOne({
						'token': user_token, 
						'widget_id': widget_data['_id'],
						'campaign_id': widget_data['campaign_id'],
						'website_id': website_data['_id'],
						'reference_url': reference_url
					});

					if (user_data) {

						var notify_data = db.client_notifications.findOne({
							'usertoken_id': user_data['_id'],
							'notify_type': notify_type,
						})

						if (!notify_data){
							db.client_notifications.insert({
								'usertoken_id': user_data['_id'],
								'widget_id': widget_data['_id'],
								'campaign_id': widget_data['campaign_id'],
								'website_id': website_data['_id'],
								'publisher_id': campaign_data['publisher_id'],
								'sponsor_id':  campaign_data['sponsor_id'],
								'notify_type': notify_type,
								'email': email,
								'date_created': new Date(),
								'day': day
							});

							db.client_usertoken.update({
								'_id': user_data['_id']
							}, {
								$set: {'email': email} 
							}, false, false);
						}
						response = {
							'status': true,
							'msg': 'Saved.'
						};
					} else {
						response = {
							'status': false,
							'msg': 'Invalid token.'
						};
					}
				} else {
					response = {
						'status': false,
						'msg': 'Website not allowed.'
					};
				}
			} else {
				response = {
					'status': false,
					'msg': 'Campaign not available.'
				};
			}
	 	} else {
	 		response = {
				'status': false,
				'msg': 'Widget not available.'
			};
	 	}
	return response;
 	}
}); 
