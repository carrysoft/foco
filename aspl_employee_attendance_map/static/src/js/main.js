 odoo.define('aspl_employee_attendance_map.main', function (require) {
"use strict";
    
    var hr_attendance = require('hr_attendance.my_attendances');
    var KioskMode = require('hr_attendance.kiosk_confirm');

    hr_attendance.include({
           update_attendance: function () {
            var self = this;

            if ("geolocation" in navigator){
                navigator.geolocation.getCurrentPosition(function(position) {
                    self.latitude =  position.coords.latitude;
                    self.longitude = position.coords.longitude;
                });
            }
            setTimeout(function(){
                self._rpc({
                    model: 'hr.employee',
                    method: 'attendance_manual',
                    args: [[self.employee.id], 'hr_attendance.hr_attendance_action_my_attendances','',self.latitude,self.longitude],
                })
                .then(function(result) {
                    if (result.action) {
                        self.do_action(result.action);
                    } else if (result.warning) {
                        self.do_warn(result.warning);
                    }
                });
            },1000);
        },    
    });
    KioskMode.include({
        events: _.extend({}, KioskMode.prototype.events, {
            "click .o_hr_attendance_sign_in_out_icon": function () {
                var self = this;
                 if ("geolocation" in navigator){
                    navigator.geolocation.getCurrentPosition(function(position) {
                        self.latitude =  position.coords.latitude;
                        self.longitude = position.coords.longitude;   
                    });
                }
                this.$('.o_hr_attendance_sign_in_out_icon').attr("disabled", "disabled");
                setTimeout(function(){
                    self._rpc({
                        model: 'hr.employee',
                        method: 'attendance_manual',
                        args: [[self.employee_id], self.next_action,'',self.latitude,self.longitude],
                    })
                    .then(function(result) {
                        if (result.action) {
                            self.do_action(result.action);
                        } else if (result.warning) {
                            self.do_warn(result.warning);
                            self.$('.o_hr_attendance_sign_in_out_icon').removeAttr("disabled");
                        }
                    });
            },1000);
            },
        }),
    });
});