const CourseDetailsApp = {
    el: '#app',
    data() {
        return {

        }
    },
    mounted() {

    }
}

const app = Vue.createApp(CourseDetailsApp)
app.config.errorHandler = (error, vm, info) => {
    console.log(error);
};
app.mount();
