self.addEventListener('push', function (event) {
    var res_data = event.data.json().data;
    
    const title = res_data.title;
    const options = {
        body: res_data.body,
        icon: res_data.icon,
        image: res_data.image,
        actions: [{
            action: res_data.action,
            title: res_data.button_name
        }],
    };
    event.waitUntil(self.registration.showNotification(title, options));
});

self.addEventListener('notificationclick', function (event) {
    var url = event.notification.actions[0].action;
    if (event.action === 'close') {
        event.notification.close();
    } else {
        if (url) {
            event.notification.close();
            event.waitUntil(
                clients.matchAll({
                    type: 'window'
                }).then(function (windowClients) {
                    for (var i = 0; i < windowClients.length; i++) {
                        var client = windowClientss[i];
                        if (client.url == url && 'focus' in client)
                            return client.focus();
                    }
                    if (clients.openWindow) {
                        return clients.openWindow(url);
                    }
                })
            );
        }
    }
});
