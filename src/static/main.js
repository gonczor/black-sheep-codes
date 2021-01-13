function main() {
    const request = new Request('/api/v1/courses/');
    fetch(request)
        .then(response => response.json())
        .then(data => {
            console.log(data);
        });
}

window.addEventListener( "load", function () {
  function sendData() {
    const XHR = new XMLHttpRequest();
    const FD = new FormData( form );

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

  const form = document.getElementById( "signInForm" );
  form.addEventListener( "submit", function ( event ) {
    event.preventDefault();

    sendData();
  });
});
