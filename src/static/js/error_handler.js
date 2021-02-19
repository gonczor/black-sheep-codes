window.addEventListener("unhandledrejection", function(promiseRejectionEvent) {
    const status = promiseRejectionEvent.reason.request.status;
    if(status === 401) {
        alert('You\'ve been logged out.');
        window.location = '/';
    } else if (status === 403) {
        alert('Insufficient permissions.');
    }
    else {
        throw promiseRejectionEvent;
    }
});
