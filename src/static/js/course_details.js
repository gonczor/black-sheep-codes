const CourseDetailsApp = {
    el: '#app',
    data() {
        return {
            courseId: null,
            sections: [
                {
                    "name": "Introduction",
                    "id": 123,
                    "lessons": [
                        {"name": "Section Intro", "id": 1},
                        {"name": "Environment Setup", "id": 2}
                    ]
                },
                {
                    "name": "Basics",
                    "id": 321,
                    "lessons": [
                        {"name": "Running code", "id": 3},
                        {"name": "Reading user input", "id": 4},
                        {"name": "Data types", "id": 5}
                    ]
                }
            ]
        }
    },
    mounted() {
        this.courseId = window.location.pathname.split('/').slice(-2)[0];
    }
};

const app = Vue.createApp(CourseDetailsApp);
app.config.errorHandler = (error, vm, info) => {
    console.log(error);
};
app.mount('#app');
