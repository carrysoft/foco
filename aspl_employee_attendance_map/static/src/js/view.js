odoo.define('aspl_employee_attendance_map.view', function (require) {
"use strict";

	var core = require('web.core');
	var data = require('web.data');
	var ViewManager = require('web.ViewManager');
	var pyeval = require('web.pyeval');
	var Context = require('web.Context');
	var rpc = require('web.rpc');
	var data_manager = require('web.data_manager');
	var ajax = require('web.ajax');
	var form_widget = require('web.Widget');
	var _t = core._t;


	ViewManager.include({
		do_execute_action: function (action_data, env, on_closed) {
	        var self = this;
	        var result_handler = on_closed || function () {};
	        var context = new Context(env.context, action_data.context || {});
	        // OR NULL hereunder: pyeval waits specifically for a null value, different from undefined
	        var recordID = env.currentID || null;

	        // response handler
	        var handler = function (action) {
	            // show effect if button have effect attribute
	            // Rainbowman can be displayed from two places : from attribute on a button, or from python.
	            // Code below handles the first case i.e 'effect' attribute on button.
	            var effect = false;
	            if (action_data.effect) {
	                effect = pyeval.py_eval(action_data.effect);
	            };

	            if (action && action.constructor === Object) {
	                // filter out context keys that are specific to the current action.
	                // Wrong default_* and search_default_* values will no give the expected result
	                // Wrong group_by values will simply fail and forbid rendering of the destination view
	                var ncontext = new Context(
	                    _.object(_.reject(_.pairs(self.env.context), function(pair) {
	                      return pair[0].match('^(?:(?:default_|search_default_|show_).+|.+_view_ref|group_by|group_by_no_leaf|active_id|active_ids)$') !== null;
	                    }))
	                );
	                ncontext.add(action_data.context || {});
	                ncontext.add({active_model: env.model});
	                if (recordID) {
	                    ncontext.add({
	                        active_id: recordID,
	                        active_ids: [recordID],
	                    });
	                }
	                ncontext.add(action.context || {});
	                action.context = ncontext;
	                // In case effect data is returned from python and also there is rainbow
	                // attribute on button, priority is given to button attribute
	                action.effect = effect || action.effect;
	                return self.do_action(action, {
	                    on_close: result_handler,
	                });
	            } else {
	                // If action doesn't return anything, but have effect
	                // attribute on button, display rainbowman
	                self.do_action({"type":"ir.actions.act_window_close", 'effect': effect});
	                return result_handler();
	            }
	        };

	        if (action_data.special === 'cancel') {
	            return handler({"type":"ir.actions.act_window_close"});
	        } else if (action_data.type === "object") {
	            var args = recordID ? [[recordID]] : [env.resIDs];
	            if (action_data.args) {
	                try {
	                    // Warning: quotes and double quotes problem due to json and xml clash
	                    // Maybe we should force escaping in xml or do a better parse of the args array
	                    var additional_args = JSON.parse(action_data.args.replace(/'/g, '"'));
	                    args = args.concat(additional_args);
	                } catch(e) {
	                    console.error("Could not JSON.parse arguments", action_data.args);
	                }
	            }
	            args.push(context);
	            if(action_data && action_data.name === "show_map"){
	            	return rpc.query({
		                model: 'employee.attendance.map',
		                method: 'show_map',
		                args: [recordID],
		            }, {
		            	async: false
		            }).then(function (result) {
		            	if(result && result[0]){
	                		if(!result[0].connection){
	                			alert("No inernet connection.");
	                			return false;
	                		}
	                		var lat_long = [];
		                    var str = "";
		                    for(var i=0; i<result.length; i++){
		                    	
			                    	var exit = true;
				                   	if(result[i].latitude && result[i].longitude){
				                   		if(lat_long.length > 0){
				                   			_.each(lat_long, function(item){						              
				                   				if($.inArray(result[i].latitude, item) !== -1 && $.inArray(result[i].longitude,item) !== -1){
							                   		item[1] = item[1] + 1;
							                   		exit = false;
							                   		return;
				                   				}
				                   			});
				                   		}
				                   		if(exit){
					                   		if(result[i].image)
					                   		{
					                   		 str = "<img class='img-circle' src='data:image/png;base64,"+ result[i].image +"' width='50' height='50'> "
					                   		}
					                   		str += result[i].name
					                   		str += "<button style='margin-left:15px;' title='Attendance Detail' class='btnpopup btn btn-icon fa fa-lg fa-list-ul o_cp_switch_list' data-job_position="+result[i].job_position+" data-dept_id="+result[i].dept_id+" data-date="+result[i].date+" data-cust-id="+result[i].emp_id+" data-btn='30'></button>"
                                            lat_long.push([str,result[i].latitude,result[i].longitude, 0]);
				                   		}
				                   	}
			            		}
		                    if(lat_long.length > 0){
		                    	initialize_gmap(lat_long);
		                    	return true
		                    }else{
		                    	alert("No Record Found")
	                        	if(result && result[0].connection){
	                        		initialize_gmap([]);
		                		}
	                        	return false;
	                        }
	                	}
		            }).fail(function (error, event){
	                	initialize_gmap([]);
	                    if(error.code === -32098) {
	                        alert("Server closed...");
	                        event.preventDefault();
	                   }
	               });
	            }else{
	            	var dataset = new data.DataSet(self, env.model, env.context);
		            return dataset.call_button(action_data.name, args).then(handler);
	            }
	        } else if (action_data.type === "action") {
	            return data_manager.load_action(action_data.name, _.extend(pyeval.eval('context', context), {
	                active_model: env.model,
	                active_ids: env.resIDs,
	                active_id: recordID,
	            })).then(handler);
	        }
	    },
	});
	form_widget.include({
        start:function(){
            var res = this._super();
            var self = this;
            $(document).on('click','.btnpopup',function(event){
            if(event.handled !== true) // This will prevent event triggering more then once
        	{
            	event.handled = true;
                var id = $(this).attr('data-cust-id');
                var at_date = $(this).attr('data-date');
                var btn = $(this).attr('data-btn');
                var job_position = $(this).attr('data-job_position');
                var dept_id = $(this).attr('data-dept_id');
                if (id && btn){
                    $.ajax({
                        type: "GET",
                        dataType: 'json',
                        url: '/employee_attendance',
                        data: {'employee_id' : id,'date':at_date, 'dept_id':dept_id,'job_position':job_position},
                        success: function(success) {
                            if (success && success.filter_domain){
                                self.do_action({
                                    type: 'ir.actions.act_window',
                                    res_model: "hr.attendance",
                                    name: _t('Employee Attendance'),
                                    views: [[false,"list"]],
                                    domain: success.filter_domain,
                                    target: 'new',
                                });
                            }
                            else{
                                alert("No Employee Found");
                            }
                        },
                    });
				}                
			}
        });
            return res
        }
    });
});
