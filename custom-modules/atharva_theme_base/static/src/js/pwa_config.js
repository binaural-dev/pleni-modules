
odoo.define('atharva_theme_base.pwa_config_js', function (require) {
'use strict';
var publicWidget = require('web.public.widget');
let swRegistration = null;

publicWidget.registry.pwa = publicWidget.Widget.extend({
    selector: '#wrapwrap',
    start: function() {
        this._super.apply(this, arguments);
        this._rpc({
            route: '/pwa/is_active',
            params: {}
        }).then(function (result) {
            if(result == true){
                if('serviceWorker' in navigator){
                    navigator.serviceWorker.register('/service-worker-js').then(swReg => {
                        console.log('Service Worker is registered', swReg);
                        // We are storing the service worker, globally
                        swRegistration = swReg;
                        //displayNotification()
                      })
                      .catch(error => {
                        console.error('Service Worker Error', error);
                    });

                    console.log('Service Worker Registered');
                }

                if ('serviceWorker' in navigator && 'PushManager' in window) {
                    console.log('Service Worker and Push is supported');
                }
            }
            else{
                if(navigator.serviceWorker) {
                    navigator.serviceWorker.getRegistrations().then(function(reg) {
                        _.each(reg, function(sw) {
                            sw.unregister();
                        });
                    });
                } else {
                    console.warn('Push messaging is not supported');
                    ///notificationButton.textContent = 'Push Not Supported';
                }
            }
        });
    },
});
  
function displayNotification() {
    if (window.Notification && Notification.permission === "granted") {
      notification();
    }
    // If the user hasn't told if he wants to be notified or not
    // Note: because of Chrome, we are not sure the permission property
    // is set, therefore it's unsafe to check for the "default" value.
    else if (window.Notification && Notification.permission !== "denied") {
      Notification.requestPermission(status => {
        if (status === "granted") {
          notification();
        } else {
          alert("You denied or dismissed permissions to notifications.");
        }
      });
    } else {
      // If the user refuses to get notified
      alert(
        "You denied permissions to notifications. Please go to your browser or phone setting to allow notifications."
      );
    }
  }
function notification() {
    const options = {
        body: "Testing Our Notification",
    };

    if (swRegistration == null) return;
    swRegistration.showNotification("PWA Notification!", options);
}
});