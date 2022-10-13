
$(document).ready(function () {
    function registerServiceWorker() {
        return navigator.serviceWorker.register('/user_base_firebase/static/src/js/sw.js')
            .then(function (registration) {
                return registration;
            })
            .catch(function (err) {
                $('#register_notification').prop('checked', false);
                toastr.error(err, 'Unable to register service worker.');
            });
    }
    function sendTokenToServer(token) {
        if (token) {
            $.cookie("user_base_firebase", token);
            $.ajax({
                url: "/user_base_firebase/set_firebase_data",
                type: 'GET',
                data: { 'token': token },
            });
        }
    }
    var messaging;
    function handleTokenRefresh(permission) {
        return messaging.getToken().then((token) => {
            return token
        });
    }
    function subscribeToNotifications() {
        $.ajax({
            url: "/user_base_firebase/get_firebase_data",
            type: 'GET',
            data: {},
            success: function (res) {
                try {
                    var firebase_config = JSON.parse(res);
                    firebase.initializeApp(firebase_config);
                    messaging = firebase.messaging();
                    if (messaging) {
                        return registerServiceWorker().then((registration) => {
                            messaging.useServiceWorker(registration);
                            return Notification.requestPermission()
                                .then((permission) => handleTokenRefresh(permission))
                                .then((token) => sendTokenToServer(token))
                                .catch((err) => {
                                    $('#register_notification').prop('checked', false);
                                    toastr.error(err, "error getting permission :(");
                                });
                        });
                    }
                    if (messaging)
                        messaging.onTokenRefresh(() => {
                            messaging.getToken().then((refreshedToken) => {
                                setTokenSentToServer(false);
                                sendTokenToServer(refreshedToken);
                            }).catch((err) => {
                                $('#register_notification').prop('checked', false);
                                toastr.error(err, 'Unable to retrieve refreshed token ');
                            });
                        });
                } catch (err) {
                    $('#register_notification').prop('checked', false);
                    toastr.error(err);
                }
            },
            Error: function (x, e) {
                $('#register_notification').prop('checked', false);
                toastr.error("error getting firebase data");
            }
        });
    }
    if (messaging) {
        messaging.onMessage(function (payload) {
            console.log("receiving message from onMessage", payload)
            var notificationTitle = payload['notification']['title']
            var notificationOptions = payload['notification']
            navigator.serviceWorker.ready.then(function (registration) {
                registration.showNotification(notificationTitle, notificationOptions);
            });
        });
    }
    var tocken = $.cookie("user_base_firebase");
    if(tocken)
        sendTokenToServer(tocken)
    else
        subscribeToNotifications();
});