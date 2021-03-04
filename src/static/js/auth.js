window.addEventListener( "load", function () {
  function performAccountCreation() {
    const XHR = new XMLHttpRequest();
    const FD = new FormData( accountCreationForm );

    XHR.addEventListener( "load", function(event) {
      if (event.target.status !== 201){
        const responseData = JSON.parse(event.target.responseText);
        let message = 'Following errors occurred:\n';
        for (const key in responseData) {
          message += `${key}: ${responseData[key]}\n`;
        }
        alert( message );
      } else {
        window.location = '/login/'
      }
    });

    XHR.addEventListener( "error", function( event ) {
      alert( 'Oops! Something went wrong.' );
    });

    XHR.open( "POST", "/api/v1/auth/users/" );
    XHR.setRequestHeader('Content-Type', 'application/json;');
    const data = Object.fromEntries(FD.entries());
    XHR.send(JSON.stringify(data));
  }

  function performLogin() {
    const XHR = new XMLHttpRequest();
    const FD = new FormData( loginForm );

    XHR.addEventListener( "load", function(event) {
      if (event.target.status !== 200){
        const responseData = JSON.parse(event.target.responseText);
        let message = 'Following errors occurred:\n';
        for (const key in responseData) {
          message += `${key}: ${responseData[key]}\n`;
        }
        alert( message );
      } else {
        const response = JSON.parse(event.target.response);
        window.localStorage.setItem('token', response.authToken);
        window.location = '/courses/'
      }
    });

    XHR.addEventListener( "error", function( event ) {
      alert( 'Oops! Something went wrong.' );
    });

    XHR.open( "POST", "/api/v1/auth/token/login/" );
    XHR.setRequestHeader('Content-Type', 'application/json;');
    const data = Object.fromEntries(FD.entries());
    XHR.send(JSON.stringify(data));
  }

  function redirectIfLoggedIn(){
    let token = localStorage.getItem("token");
    if (token === null){
      // No token, no redirect.
      return;
    }
    const XHR = new XMLHttpRequest();
    XHR.open( "GET", "/api/v1/auth/users/me/" );
    XHR.setRequestHeader('Content-Type', 'application/json;');
    XHR.setRequestHeader('Authorization', 'Token ' + token);
    XHR.addEventListener("load", (event) => {
      if (event.target.status === 200){
        window.location = "/courses/";
      } else {
        // Token is invalid, we can remove it.
        localStorage.removeItem("token");
      }
    });
    XHR.send();
  }
  redirectIfLoggedIn();

  const accountCreationForm = document.getElementById( "accountCreationForm" );
  if (accountCreationForm !== null){
    accountCreationForm.addEventListener( "submit", function ( event ) {
      event.preventDefault();
      performAccountCreation();
    });
  }
  const loginForm = document.getElementById( "loginForm" );
  if (loginForm !== null) {
    loginForm.addEventListener( "submit", function ( event ) {
      event.preventDefault();
      performLogin();
    });
  }
});
