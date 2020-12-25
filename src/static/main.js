function main() {
    const request = new Request('/api/v1/courses/');
    fetch(request).then((response) => {
       console.log(response);
    });
}
